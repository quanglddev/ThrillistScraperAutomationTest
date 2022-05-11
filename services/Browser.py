from dataclasses import dataclass

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager


@dataclass
class Browser:
    driver: WebDriver

    def __init__(self) -> None:
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        self.driver = driver

    def navigateTo(self, url) -> BeautifulSoup:
        self.driver.get(url)
        html = self.driver.page_source
        parser = BeautifulSoup(html, "html.parser")
        return parser
