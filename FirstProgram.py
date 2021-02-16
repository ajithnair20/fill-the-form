from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import VisionAI.VisionAI as vi

# This example requires Selenium WebDriver 3.13 or newer
urls = ['https://www.facebook.com/login/']


def get_screenshot_difference(base_folder_path, before, after):
    try:
        vision = vi.VisionAI()
        before_resp = vision.extractTextFromImage(base_folder_path, before)
        after_resp = vision.extractTextFromImage(base_folder_path, after)
        before_lines = before_resp.splitlines()
        after_lines = after_resp.splitlines()
        return list(set(after_lines) - set(before_lines))
    except Exception as e:
        print(e)
        return []


def isAlert(driver):
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        print("alert Exists in page")
        return True, alert_text
    except TimeoutException:
        print("alert does not Exist in page")
        return False, ''

