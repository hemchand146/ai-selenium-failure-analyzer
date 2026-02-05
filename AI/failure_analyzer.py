# AI failure analyzer
# Uses an OpenAI-compatible client (OpenRouter) to convert raw Selenium logs
# into a structured JSON diagnosis

from __future__ import annotations

# --------------------------------------------------
# Imports
# --------------------------------------------------

import json
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI

from AI.prompt_templates import failure_analysis_prompt


# --------------------------------------------------
# Constants & Types
# --------------------------------------------------

_REQUIRED_KEYS: tuple[str, ...] = (
    "failure_reason",
    "possible_issues",
    "what_to_check_first",
    "possible_fixes",
)


@dataclass(frozen=True)
class OpenRouterConfig:
    # Configuration required to call OpenRouter via the OpenAI SDK

    api_key: str
    model: str = "openai/gpt-4o-mini"
    base_url: str = "https://openrouter.ai/api/v1"


# --------------------------------------------------
# Config Helpers
# --------------------------------------------------

def _load_openrouter_config() -> OpenRouterConfig:
    # Load OpenRouter config from `AI/ai_config.json`
    # Expected JSON shape:
    # {
    #   "openrouter": {
    #     "api_key": "...",
    #     "model": "openai/gpt-4o-mini"  // optional
    #   }
    # }
    # Note: We intentionally do *not* read environment variables here to keep the
    # configuration source simple and predictable
    path = os.path.join(os.path.dirname(__file__), "ai_config.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except FileNotFoundError as e:
        raise RuntimeError("Missing AI/ai_config.json (OpenRouter config)") from e

    or_cfg = cfg.get("openrouter") if isinstance(cfg, dict) else None
    if not isinstance(or_cfg, dict):
        raise RuntimeError("Missing 'openrouter' object in AI/ai_config.json")

    api_key = (or_cfg.get("api_key") or "").strip()
    model = (or_cfg.get("model") or "").strip() or "openai/gpt-4o-mini"

    if not api_key:
        raise RuntimeError("Missing openrouter.api_key in AI/ai_config.json")

    return OpenRouterConfig(api_key=api_key, model=model)


# --------------------------------------------------
# Parsing Helpers
# --------------------------------------------------

def _as_list(value: Any) -> list[str]:
    # Normalize a potentially-scalar field into a list of strings
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    return [str(value)]


def _strip_code_fences(text: str) -> str:
    # Remove common markdown code fences if the model ignores instructions

    cleaned = text.strip()
    cleaned = re.sub(r"^```[a-zA-Z0-9_-]*\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip()


def _extract_first_json_object(text: str) -> Dict[str, Any]:
    # Extract and parse the first JSON object found in the text
    cleaned = _strip_code_fences(text)

    # Prefer strict parse first.
    try:
        parsed = json.loads(cleaned)
        if isinstance(parsed, dict):
            return parsed
    except json.JSONDecodeError:
        pass

    # Fallback: find the first {...} block.
    match = re.search(r"\{.*}", cleaned, re.DOTALL)
    if not match:
        raise ValueError("AI response does not contain a JSON object")

    parsed = json.loads(match.group(0))
    if not isinstance(parsed, dict):
        raise ValueError("AI JSON response must be an object")
    return parsed


def _ensure_contract(parsed: Dict[str, Any], *, test_name: str, model: str) -> Dict[str, Any]:
    # Enforce our expected output shape so report writers stay simple
    for key in _REQUIRED_KEYS:
        if key not in parsed:
            raise ValueError(f"Missing key in AI response: {key}")

    result: Dict[str, Any] = {
        "failure_reason": str(parsed.get("failure_reason", "")),
        "possible_issues": _as_list(parsed.get("possible_issues")),
        "what_to_check_first": _as_list(parsed.get("what_to_check_first")),
        "possible_fixes": _as_list(parsed.get("possible_fixes")),
        "_meta": {
            "source": "openrouter",
            "model": model,
            "test_name": test_name,
        },
    }

    return result


# --------------------------------------------------
# Public Analyzer
# --------------------------------------------------

class FailureAnalyzer:
    # Calls an LLM to turn a raw Selenium log into a structured JSON diagnosis
    # Public contract:
    # - Input: test_name + raw log text (string)
    # - Output: dict with the required keys + optional _meta
    # Any network/config failures should be handled by the caller (we raise)

    def __init__(self, config: Optional[OpenRouterConfig] = None):
        self._config = config or _load_openrouter_config()

        # OpenRouter uses an OpenAI-compatible API.
        self._client = OpenAI(
            api_key=self._config.api_key,
            base_url=self._config.base_url,
            default_headers={
                "HTTP-Referer": "http://localhost",
                "X-Title": "AI Selenium Failure Analyzer",
            },
        )

    def analyze(self, test_name: str, log_text: str) -> Dict[str, Any]:
        prompt = failure_analysis_prompt(test_name, log_text)

        # The SDK's type hints are strict; at runtime it accepts dict messages.
        messages: Any = [
            {"role": "system", "content": "You are a Senior SDET."},
            {"role": "user", "content": prompt},
        ]

        response = self._client.chat.completions.create(
            model=self._config.model,
            temperature=0.2,
            messages=messages,
        )

        raw_text = response.choices[0].message.content or ""
        parsed = _extract_first_json_object(raw_text)
        return _ensure_contract(parsed, test_name=test_name, model=self._config.model)
