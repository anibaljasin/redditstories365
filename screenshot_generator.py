import os
import logging
from functools import lru_cache

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class ScreenshotGenerator:
    def __init__(self, url: str, base_folder: str):
        self.driver = self.init_driver()
        self.url = url
        self.base_folder = base_folder

    @lru_cache(maxsize=1)
    def init_driver(self):
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", {'protocol_handler.excluded_schemes.tel': False})
        chrome = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        return chrome

    def take_submission_title_screenshot(self, html_element_title_id: str):
        self.driver.get(self.url)
        self.driver.find_element(By.ID, html_element_title_id).screenshot(os.path.join(self.base_folder, f"title.png"))

    def take_submission_comment_screenshot(self, comments):
        self.driver.get(self.url)

        for i, comment in enumerate(comments):
            try:
                html_element_id = f"t1_{comment}"
                logger.info(f"Taking screenshot of comment: {html_element_id}")
                self.driver.find_element(By.ID, html_element_id).screenshot(
                    os.path.join(self.base_folder, f"comment-{i}.png"))
            except Exception as ex:
                logger.exception(ex)

    def quit_driver(self):
        self.driver.quit()


@lru_cache(maxsize=1)
def get_driver():
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", {'protocol_handler.excluded_schemes.tel': False})
    chrome = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    return chrome


def take_submission_title_screenshot(url: str, html_element_id: str, base_folder: str = "./"):
    chrome = get_driver()
    chrome.get(url)
    chrome.find_element(By.ID, html_element_id).screenshot(os.path.join(base_folder, f"title.png"))


def take_submission_comment_screenshot(url: str, comments: str, base_folder: str = "./"):
    chrome = get_driver()
    chrome.get(url)

    for i, comment in enumerate(comments):
        try:
            html_element_id = f"t1_{comment.id}"
            logger.info(f"Taking screenshot of comment: {html_element_id}")

            chrome.find_element(By.ID, html_element_id).screenshot(os.path.join(base_folder, f"comment-{i}.png"))
        except Exception as ex:
            logger.exception(ex)
