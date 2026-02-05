# Build AI-powered failure summaries
# Reads automation results + logs and writes Reports/failure_summary.json and .log

from __future__ import annotations

# --------------------------------------------------
# Imports
# --------------------------------------------------

import json
import os
from typing import Any, Dict, List

from AI.failure_analyzer import FailureAnalyzer


# --------------------------------------------------
# File Helpers
# --------------------------------------------------

def _load_json(path: str) -> Any:
    # Load JSON from disk (handles UTF-8 with BOM)

    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def _read_log_text(testcase_id: str, max_chars: int = 200_000) -> str:
    # Read a test log from `Logs/{test_name}.log`
    # We cap size so prompts stay small and predictable
    # If the log doesn't exist, we return an empty string
    path = os.path.join("Logs", f"{testcase_id}.log")
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
    except FileNotFoundError:
        return ""

    return text[-max_chars:] if len(text) > max_chars else text


def _write_json(path: str, payload: Any) -> None:
    # Write JSON to disk creating the parent folder if needed
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)


def write_human_readable_log(
    items: List[Dict[str, Any]],
    output_path: str = os.path.join("Reports", "failure_summary.log"),
) -> None:
    # Create a readable text report in addition to the JSON summary
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("=============== AI FAILURE SUMMARY ===============\n\n")
        f.write(f"Total Failed Tests: {len(items)}\n\n")

        for idx, item in enumerate(items, start=1):
            f.write("-" * 55 + "\n")
            f.write(f"[{idx}] TEST_NAME : {item.get('test_name')}\n")
            f.write(f"FAILURE       : {item.get('failure_reason')}\n\n")

            f.write("POSSIBLE ISSUES:\n")
            for i in item.get("possible_issues", []):
                f.write(f" - {i}\n")

            f.write("\nWHAT TO CHECK FIRST:\n")
            for i in item.get("what_to_check_first", []):
                f.write(f" - {i}\n")

            f.write("\nPOSSIBLE FIXES:\n")
            for i in item.get("possible_fixes", []):
                f.write(f" - {i}\n")

            f.write("\n")

        f.write("=" * 55 + "\n")


def build_failure_summary(
    results_path: str = os.path.join("Reports", "automation_results.json"),
    json_output: str = os.path.join("Reports", "failure_summary.json"),
) -> List[Dict[str, Any]]:
    # Analyze failed tests and write `Reports/failure_summary.json` + `.log`
    # Input:
    # - `Reports/automation_results.json` (created by the runner with test_name)
    # - `Logs/{test_name}.log`
    # Output:
    # - `Reports/failure_summary.json` (machine readable)
    # - `Reports/failure_summary.log`  (human readable)
    # If AI isn't configured or the LLM call fails for a testcase, we still write
    # a placeholder entry so the report is complete

    suite = _load_json(results_path)
    tests = suite.get("tests", []) if isinstance(suite, dict) else suite

    failed = [t for t in tests if str(t.get("status")).upper() == "FAIL"]

    analyzer = FailureAnalyzer()
    items: List[Dict[str, Any]] = []

    for t in failed:
        # Get test name from automation results (test_name, not test_case_id)
        test_name = str(t.get("test_name", "unknown"))
        log_text = _read_log_text(test_name)

        try:
            analysis = analyzer.analyze(test_name, log_text)
        except Exception as e:
            analysis = {
                "failure_reason": "AI analysis unavailable",
                "possible_issues": [],
                "what_to_check_first": [],
                "possible_fixes": [],
                "_meta": {
                    "source": "openrouter",
                    "error": str(e),
                    "test_name": test_name,
                },
            }

        items.append({"test_name": test_name, **analysis})

    _write_json(json_output, items)
    write_human_readable_log(items)

    return items


def main() -> None:
    # CLI entrypoint: `python -m AI.summarize_failures`

    build_failure_summary()


if __name__ == "__main__":
    main()
