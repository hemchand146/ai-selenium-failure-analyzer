# Logging and screenshot helpers
# This module centralizes logging configuration for test and automation logs,
# and provides a screenshot helper for failures

# --------------------------------------------------
# Imports
# --------------------------------------------------

from datetime import datetime
import logging
import os


# --------------------------------------------------
# Formatters
# --------------------------------------------------

class DetailedFormatter(logging.Formatter):
    # Custom formatter for simple logging - just the message

    def format(self, record):
        message = record.getMessage()
        return message


class StructuredFormatter(logging.Formatter):
    # Structured formatter with timestamps and context

    def format(self, record):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        level = record.levelname
        message = record.getMessage()

        if level == "INFO":
            return f"[{timestamp}] ✓ {message}"
        elif level == "ERROR":
            return f"[{timestamp}] ✗ ERROR: {message}"
        elif level == "DEBUG":
            return f"[{timestamp}] → {message}"
        elif level == "WARNING":
            return f"[{timestamp}] ⚠ WARNING: {message}"
        else:
            return f"[{timestamp}] {level}: {message}"


# --------------------------------------------------
# Logger Factories
# --------------------------------------------------

class LoggerManager:

    @staticmethod
    def get_test_logger(test_name):
        logger_name = f"TestLogger_{test_name}"
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False

        # Clear existing handlers to prevent duplicate logs
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

        os.makedirs("Logs", exist_ok=True)
        log_file = os.path.join("Logs", f"{test_name}.log")

        # Use structured formatter for test logs
        formatter = StructuredFormatter()

        handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger

    @staticmethod
    def get_automation_logger():
        logger = logging.getLogger("AutomationLogger")
        logger.setLevel(logging.INFO)
        logger.propagate = False

        # Clear existing handlers to prevent duplicate logs
        for handler in logger.handlers[:]:
            handler.close()
            logger.removeHandler(handler)

        os.makedirs("Logs", exist_ok=True)
        log_file = os.path.join("Logs", "Suite.log")

        # Use structured formatter for suite logs
        formatter = StructuredFormatter()

        handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        handler.setFormatter(formatter)

        logger.addHandler(handler)
        return logger


# --------------------------------------------------
# Screenshots
# --------------------------------------------------

class ScreenshotManager:

    @staticmethod
    def capture(driver, test_name, step_name="failure"):
        if not driver:
            return None

        path = os.path.join("Logs", "screenshots")
        os.makedirs(path, exist_ok=True)

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_{step_name}_{ts}.png"
        full_path = os.path.join(path, filename)

        driver.save_screenshot(full_path)
        return full_path

