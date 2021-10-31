import os
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def take_submission_title_screenshot(url: str, html_element_id: str, base_folder: str = "./"):
    chrome = webdriver.Chrome(ChromeDriverManager().install())
    chrome.get(url)
    chrome.find_element(By.ID, html_element_id).screenshot(os.path.join(base_folder, f"title.png"))


def take_submission_comment_screenshot(url: str, comments: str, base_folder: str = "./"):
    chrome = webdriver.Chrome(ChromeDriverManager().install())
    chrome.get(url)

    for i, comment in enumerate(comments):
        html_element_id = f"t1_{comment.id}"
        logger.info(f"Taking screenshot of comment: {html_element_id}")

        chrome.find_element(By.ID, html_element_id).screenshot(os.path.join(base_folder, f"comment-{i}.png"))
