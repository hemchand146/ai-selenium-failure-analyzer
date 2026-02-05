# Prompt templates for AI analysis
# These are pure string builders used by the failure analyzer

from __future__ import annotations

# --------------------------------------------------
# Prompts
# --------------------------------------------------


def failure_analysis_prompt(test_name: str, log_text: str) -> str:
    return (
        "You are a Senior SDET analyzing a Selenium WebDriver test failure.\n\n"
        
        "INSTRUCTIONS:\n"
        "1. Read the ENTIRE log from beginning to end\n"
        "2. Identify the exact error type and message\n"
        "3. Determine at which test phase it occurred (setup, run, teardown)\n"
        "4. Understand what was being executed when the error happened\n"
        "5. Provide specific, actionable insights\n\n"
        
        "KEY ERROR INDICATORS TO LOOK FOR:\n"
        "- 'ERROR:' or '✗ ERROR' markers in the log\n"
        "- 'Error Type:' field (e.g., AttributeError, TimeoutException, NoSuchElementException)\n"
        "- 'Error Message:' field (the actual error description)\n"
        "- Which phase failed: setup (login), run (test execution), or teardown\n"
        "- Stack trace information if available\n\n"
        
        "COMMON SELENIUM ERRORS AND MEANINGS:\n"
        "- 'NoneType' object has no attribute 'is_displayed' = Element is None/null, not found or not accessible\n"
        "- TimeoutException = Element did not appear within the wait time\n"
        "- NoSuchElementException = Locator didn't match any element on page\n"
        "- StaleElementReferenceException = Element no longer attached to DOM\n"
        "- NoSuchWindowException = Browser window was closed unexpectedly\n"
        "- 'already exists' error = Duplicate data or duplicate record in system\n\n"
        
        "RESPONSE REQUIREMENTS:\n"
        "- You MUST respond with ONLY a valid JSON object\n"
        "- Do NOT include any explanations, markdown, or extra text\n"
        "- Do NOT use code blocks or backticks\n"
        "- The JSON MUST be valid and parseable\n\n"
        
        "JSON FORMAT (exactly these keys):\n"
        "{\n"
        '  "failure_reason": "Concise description of what failed and why (be specific)",\n'
        '  "possible_issues": ["root cause 1", "root cause 2", "root cause 3"],\n'
        '  "what_to_check_first": ["priority check 1", "priority check 2", "priority check 3"],\n'
        '  "possible_fixes": ["specific fix 1", "specific fix 2", "specific fix 3"]\n'
        "}\n\n"
        
        f"Test Name: {test_name}\n"
        "Analyze this log carefully:\n\n"
        f"{log_text}"
    )
