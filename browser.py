# Browser factory and WebDriver lifecycle
# Module provides a small wrapper around Selenium WebDriver creation
# based on the configured browser name

# --------------------------------------------------
# Imports
# --------------------------------------------------

from selenium import webdriver


# --------------------------------------------------
# Browser
# --------------------------------------------------

class Browser:
    def __init__(self, browser_name, config=None):
        self.browser_name = str(browser_name).lower()
        self.config = config or {}
        self.driver = None

    def start(self):
        headless = bool(self.config.get("headless", False))

        if self.browser_name == "chrome":
            options = webdriver.ChromeOptions()

            options.add_experimental_option("detach", True)
            options.add_experimental_option("excludeSwitches", ["enable-logging"])

            options.add_argument("--disable-background-networking")
            options.add_argument("--disable-sync")
            options.add_argument("--disable-notifications")
            options.add_argument("--disable-extensions")

            if headless:
                # Use new headless mode when available
                options.add_argument("--headless=new")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")

            self.driver = webdriver.Chrome(options=options)

        elif self.browser_name == "firefox":
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("-headless")
            self.driver = webdriver.Firefox(options=options)

        else:
            raise Exception(f"Unsupported browser: {self.browser_name}")

        implicit_wait = float(self.config.get("implicit_wait", 1.5))
        self.driver.implicitly_wait(implicit_wait)

        # Maximize only when not headless
        if not headless:
            self.driver.maximize_window()
        return self.driver

    def open_url(self, url):
        self.driver.get(url)

    def quit(self):
        if self.driver:
            self.driver.quit()
            self.driver = None
