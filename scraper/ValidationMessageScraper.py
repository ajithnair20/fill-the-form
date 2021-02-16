# Importing Libraries
import logging

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC

# Crawl URLs 
urls = ['/course-project-team_nair_mohanty/utilities/test.html']
logging.basicConfig(filename='example.log', level=logging.DEBUG)

error_messages = []


def extractErrorMessages(url):
    isError = True
    logging.info(f'Crawling URL: {url}')
    driver = webdriver.Chrome()
    driver.maximize_window()
    try:
        driver.get(url)
        before = driver.page_source
        elem = driver.find_element_by_name("alert")

        while isError:
            elem.click()
            logging.info('Clicked Submit Button')

            # Check if an alert message was triggered
            if EC.alert_is_present():
                logging.info('Alert Message')
                obj = driver.switch_to.alert
                msg = obj.text
                logging.info(f'Alert Message: {text}')
                error_messages.append(text)
                obj.accept()
                logging.info('Clicked OK')

            # Else check validation message
            else:
                after = driver.page_source
                if before != after:
                    isError = False

        logging.info('-------------------------------------')
        driver.close()
    except Exception:
        print('Error')
        driver.close()


for url in urls:
    extractErrorMessages(url)
