import sys
import json
import importlib
import traceback
import os
from datetime import datetime, timezone

from utils.logger import LoggerManager, ScreenshotManager



# --------------------------------------------------
# Utility Functions
# --------------------------------------------------

def load_test_data(json_path):
    # Load JSON test data from file
    with open(json_path, "r") as f:
        return json.load(f)


def log_execution_separator(logger):
    now = datetime.now()
    logger.info("=" * 80)
    logger.info("TEST EXECUTION STARTED")
    logger.info("=" * 80)
    logger.info("Date: %s", now.strftime("%Y-%m-%d"))
    logger.info("Time: %s", now.strftime("%H:%M:%S"))
    logger.info("=" * 80)


def ensure_dirs():
    os.makedirs("Logs/screenshots", exist_ok=True)
    os.makedirs("Reports", exist_ok=True)


def write_automation_results(results_list, input_json_path, suite_id):
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "input_json": input_json_path,
        "suite_id": str(suite_id),
        "tests": results_list
    }

    with open(os.path.join("Reports", "automation_results.json"), "w") as f:
        json.dump(payload, f, indent=2)


# --------------------------------------------------
# Test Execution
# --------------------------------------------------

def execute_test(test_name, test_data, test_logger, automation_logger):
    # Execute a single test case using test name
    test_logger.info("-" * 80)
    test_logger.info("TEST: %s", test_name.upper())
    test_logger.info("-" * 80)

    automation_logger.info("→ Executing Test: %s", test_name)

    status = "PASS"
    screenshot = None
    test = None

    try:
        test_logger.info("Loading test module: Testcases.%s", test_name)
        module = importlib.import_module(f"Testcases.{test_name}")
        test_class = getattr(module, "TestCase")
        test = test_class(test_data, test_logger)
        test_logger.info("✓ Test class loaded successfully")

        test_logger.info("Executing setup phase...")
        test.setup()
        test_logger.info("✓ Setup completed successfully")

        test_logger.info("Executing test phase...")
        test.run()
        test_logger.info("✓ Test phase completed successfully")

        test.result["status"] = "PASS"
        test_logger.info("=" * 80)
        test_logger.info("TEST RESULT: PASSED ✓")
        test_logger.info("=" * 80)

    except Exception as e:
        status = "FAIL"
        if test:
            test.result["status"] = "FAIL"
            test.result["error"] = str(e)

        test_logger.error("=" * 80)
        test_logger.error("TEST FAILED ✗")
        test_logger.error("=" * 80)
        test_logger.error("Error Type: %s", type(e).__name__)
        test_logger.error("Error Message: %s", str(e))

        screenshot = ScreenshotManager.capture(
            test.driver if test and hasattr(test, "driver") else None,
            test_name,
            "failure"
        )

        if screenshot:
            test_logger.error("Screenshot captured: %s", screenshot)

        test_logger.error("Stack Trace:")
        test_logger.error(traceback.format_exc())

    finally:
        if test and hasattr(test, "teardown"):
            try:
                test_logger.info("Executing teardown phase...")
                test.teardown()
                test_logger.info("✓ Teardown completed")
            except Exception as e:
                test_logger.error("✗ Teardown failed: %s", str(e))
                test_logger.error(traceback.format_exc())

    automation_logger.info("✓ Test '%s' completed with status: %s", test_name, status)

    if screenshot and test:
        test.result["screenshot"] = screenshot

    return status


# --------------------------------------------------
# Suite Execution
# --------------------------------------------------

def execute_suite(suite_data, automation_logger, suite_json_path):
    # Execute multiple test cases listed as JSON files
    test_files = suite_data.get("test_cases", [])
    suite_id = os.path.basename(suite_json_path).replace(".json", "")

    results_list = []

    for test_file in test_files:
        # Handle both .json and non-.json formats
        if not test_file.endswith(".json"):
            test_file = f"{test_file}.json"

        test_json_path = os.path.join("TestData", test_file)

        if not os.path.exists(test_json_path):
            automation_logger.error("Test JSON not found: %s", test_file)
            continue

        test_data = load_test_data(test_json_path)
        # Extract test name from filename (e.g., test_login.json -> test_login)
        test_name = os.path.basename(test_file).replace(".json", "")

        test_logger = LoggerManager.get_test_logger(test_name)
        log_execution_separator(test_logger)

        automation_logger.info(
            "Running Test: %s using %s", test_name, test_file
        )

        status = execute_test(
            test_name,
            test_data,
            test_logger,
            automation_logger
        )

        results_list.append({
            "test_name": test_name,
            "status": status,
            "log_file": os.path.join("Logs", f"{test_name}.log")
        })

    write_automation_results(results_list, suite_json_path, suite_id)

    # Report results without exiting - allow reporting to happen
    passed = len([r for r in results_list if r["status"] == "PASS"])
    failed = len([r for r in results_list if r["status"] == "FAIL"])

    automation_logger.info("=" * 80)
    automation_logger.info("SUITE EXECUTION COMPLETE")
    automation_logger.info("=" * 80)
    automation_logger.info("Total Tests: %d | Passed: %d | Failed: %d", len(results_list), passed, failed)
    automation_logger.info("=" * 80)


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():
    ensure_dirs()

    if len(sys.argv) < 2:
        print("Usage: python run.py <test_json_path>")
        sys.exit(1)

    input_json_path = sys.argv[1]
    test_data = load_test_data(input_json_path)

    automation_logger = LoggerManager.get_automation_logger()
    log_execution_separator(automation_logger)

    is_suite = (
        isinstance(test_data, dict)
        and "test_cases" in test_data
        and isinstance(test_data["test_cases"], list)
    )

    # -------- SUITE --------
    if is_suite:
        automation_logger.info("Executing Test Suite")
        execute_suite(test_data, automation_logger, input_json_path)

    # -------- SINGLE TEST --------
    else:
        # Extract test name from filename (e.g., test_login.json -> test_login)
        test_name = os.path.basename(input_json_path).replace(".json", "")

        test_logger = LoggerManager.get_test_logger(test_name)
        log_execution_separator(test_logger)

        status = execute_test(
            test_name,
            test_data,
            test_logger,
            automation_logger
        )

        write_automation_results(
            [{
                "test_name": test_name,
                "status": status,
                "log_file": os.path.join("Logs", f"{test_name}.log")
            }],
            input_json_path,
            test_name
        )


if __name__ == "__main__":
    main()
