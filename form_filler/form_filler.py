import os
import pathlib
import random
import re
import sys
import time
import tldextract

from bs4 import BeautifulSoup as bs, NavigableString
from fuzzywuzzy import fuzz
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException, \
    NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select

from FirstProgram import get_screenshot_difference
from mongo_client.mongoClient import MongoRepository
from rule_generator.element_rule_generator import ElementRuleGenerator
from rules.type_detect_rule import TypeFromErrorMessageRule
from schema.schema import build_schema

path = pathlib.Path(__file__).parent.absolute()
parent, tail = os.path.split(path)
chromedriver_folder_path = os.path.join(parent, 'chromedriver_directory', 'chromedriver')
chromedriver = chromedriver_folder_path

falsify_options = [False, True]

def take_screenshot(driver, path):
    driver.save_screenshot(path)


def resolve_element_from_attributes(driver, element_dict, element_tag) -> WebElement:
    page_source = driver.page_source
    soup = bs(page_source, 'html.parser')
    if 'id' in element_dict[element_tag + '_attributes']:
        if soup.find(id=element_dict[element_tag + '_attributes']['id']):
            return driver.find_element_by_id(element_dict[element_tag + '_attributes']['id'])

    if 'name' in element_dict[element_tag + '_attributes']:
        if soup.find(element_tag, attrs={'name': element_dict[element_tag + '_attributes']['name']}):
            return driver.find_element_by_name(element_dict[element_tag + '_attributes']['name'])

    return None


def determine_best_fit_text(texts, difference):
    _max = -sys.maxsize
    determined_text = ''
    for text in texts:
        if fuzz.ratio(difference, text) > _max:
            _max = fuzz.ratio(difference, text)
            determined_text = text
    return difference, determined_text


def persist_url_fill_metadata(url: str, screenshot_differences, inferred_affected_tuples):
    mongo_repository = MongoRepository()
    mongo_repository.add_url_fill_metadata_schema({
        'url': url,
        'screenshot_differences': screenshot_differences,
        'inferred_affected_tuples': inferred_affected_tuples
    })

def make_string_xpath_compatible(string: str):
    string = string.replace("&", "&amp;")
    string = string.replace("'", "&apos;")
    string = string.replace("<", "&lt;")
    string = string.replace(">", "&gt")

    return string

def fill_input_element(driver, input_element_dict, error_message='', falsify_input=True):
    rule_generator = ElementRuleGenerator()

    if 'type' in input_element_dict['input_attributes'].keys():
        if input_element_dict['input_attributes']['type'] != 'hidden' and input_element_dict['input_attributes']['type'] != 'submit' and input_element_dict['input_attributes']['type'] != 'button':
            label_element_dicts = list(map(lambda element: build_schema(element, 'label'),
                                            input_element_dict['element'].find_all_previous(name='label')))
            label_element_dict = {} if len(label_element_dicts) == 0 else label_element_dicts[0]
            resolved_element = resolve_element_from_attributes(driver, input_element_dict, 'input')
            if input_element_dict['input_attributes']['type'] == 'checkbox':
                if resolved_element and not resolved_element.is_selected() and resolved_element.is_displayed():
                    try:
                        resolved_element.click()
                    except ElementClickInterceptedException:
                        pass
            elif input_element_dict['input_attributes']['type'] == 'radio' and resolved_element.is_displayed():
                driver.execute_script('arguments[0].checked = true;', resolved_element)
            else:
                input_rule = rule_generator.generate_rule('input')
                if resolved_element and resolved_element.is_displayed():
                    try:
                        resolved_element.click()
                        for i in range(0, 100):
                            resolved_element.send_keys(Keys.BACK_SPACE)
                        resolved_element.send_keys(input_rule.compute_text(input_element_dict, label_element_dict, error_message, falsify_input))
                    except ElementClickInterceptedException:
                        pass
                    except ElementNotInteractableException:
                        pass

def fill_form_by_url_by_template(url: str, iterations, template: str):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 [FBAN/FBIOS;FBDV/iPhone11,8;FBMD/iPhone;FBSN/iOS;FBSV/13.3.1;FBSS/2;FBID/phone;FBLC/en_US;FBOP/5;FBCR/]')

    screenshots_folder_path = os.path.join(parent, 'screenshots')

    domain_name = tldextract.extract(url).domain

    driver = webdriver.Chrome(chromedriver, options=chrome_options)
    driver.get(url)
    driver.set_window_size(1920, 5000)
    driver.implicitly_wait(30)
    time.sleep(2)
    take_screenshot(driver, os.path.join(screenshots_folder_path, domain_name + '_sc_1.png'))

    soup_before = bs(driver.page_source, 'html.parser')
    input_element_dicts = list(map(lambda element: build_schema(element, 'input'), soup_before.find_all('input')))
    select_element_dicts = list(map(lambda element: build_schema(element, 'select'), soup_before.find_all('select')))


    for select_element_dict in select_element_dicts:
        try:
            select_element = resolve_element_from_attributes(driver, select_element_dict, 'select')
            if select_element:
                select = Select(resolve_element_from_attributes(driver, select_element_dict, 'select'))
                num_options = len(select.options)
                if num_options > 0:
                    select.select_by_index(random.choice(range(0, num_options)))
        except ElementNotInteractableException:
            pass


    for input_element_dict in input_element_dicts:
        fill_input_element(driver, input_element_dict, error_message='', falsify_input=True)

    for input_element_dict in input_element_dicts:
        if 'type' in input_element_dict['input_attributes'].keys():
            if input_element_dict['input_attributes']['type'] == 'button':
                resolved_element = resolve_element_from_attributes(driver, input_element_dict, 'input')
                resolved_element.click()
                break

    inferred_affected_tuples = list()

    for i in range(0, iterations):
        time.sleep(2)
        take_screenshot(driver, os.path.join(screenshots_folder_path, domain_name + '_sc_' + str(i + 2) + '.png'))
        difference_list = get_screenshot_difference(screenshots_folder_path, domain_name + '_sc_1.png', domain_name + '_sc_' + str(i + 2) + '.png')
        error_elements = set()
        error_texts = set()
        input_to_refill_elements = set()
        label_to_refill_elements = set()
        ordered_error_tuple = set()

        soup_after = bs(driver.page_source, 'html.parser')

        all_text = soup_after.find_all(text=True, recursive=True)

        for difference in difference_list:
            if len(difference.split()) >= 2:
                error_texts.add(determine_best_fit_text(all_text, difference)[1])

        for error_text in error_texts:
            error_element = soup_after.find(text=re.compile(re.escape(error_text)))
            error_element_before = soup_before.find(text=re.compile(re.escape(error_text)))
            if type(error_element_before) is not NavigableString and type(error_element) is NavigableString:
                error_elements.add(error_element)
                ordered_error_tuple.add((soup_after.find(text=re.compile(re.escape(error_text))).parent, error_text))


        type_from_error_message_rule = TypeFromErrorMessageRule()


        for error_element, error_text in ordered_error_tuple:
            affected_input_element, affected_label_element = type_from_error_message_rule.determine_type(error_element, error_text)

            if affected_input_element:
                if affected_input_element not in input_to_refill_elements:
                    input_to_refill_elements.add(affected_input_element)
                    fill_input_element(driver, build_schema(affected_input_element, 'input'), error_message=error_text, falsify_input=False)
                inferred_affected_tuples.append({
                    'affected_input': str(affected_input_element),
                    'affected_label': str(affected_label_element),
                    'error_message_element': str(error_element),
                    'error_text': error_text
                })

        time.sleep(2)
        take_screenshot(driver, os.path.join(screenshots_folder_path, domain_name + '_sc_' + str(i + 3) + '.png'))
    driver.quit()


def fill_form_by_url(url: str, iterations: int):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 [FBAN/FBIOS;FBDV/iPhone11,8;FBMD/iPhone;FBSN/iOS;FBSV/13.3.1;FBSS/2;FBID/phone;FBLC/en_US;FBOP/5;FBCR/]')

    screenshots_folder_path = os.path.join(parent, 'screenshots')

    if 'greenhouse' in url:
        fill_form_by_url_by_template(url, iterations, 'greenhouse')
        return

    domain_name = tldextract.extract(url).domain

    driver = webdriver.Chrome(chromedriver, options=chrome_options)
    driver.get(url)
    driver.set_window_size(1920, 5000)
    driver.implicitly_wait(30)
    time.sleep(2)
    take_screenshot(driver, os.path.join(screenshots_folder_path, domain_name + '_sc_1.png'))

    soup_before = bs(driver.page_source, 'html.parser')
    input_element_dicts = list(map(lambda element: build_schema(element, 'input'), soup_before.find_all('input')))
    select_element_dicts = list(map(lambda element: build_schema(element, 'select'), soup_before.find_all('select')))


    for select_element_dict in select_element_dicts:
        try:
            select_element = resolve_element_from_attributes(driver, select_element_dict, 'select')
            if select_element:
                select = Select(resolve_element_from_attributes(driver, select_element_dict, 'select'))
                num_options = len(select.options)
                if num_options > 0:
                    select.select_by_index(random.choice(range(0, num_options)))
        except ElementNotInteractableException:
            pass


    for input_element_dict in input_element_dicts:
        fill_input_element(driver, input_element_dict, error_message='', falsify_input=True)

    inferred_affected_tuples = list()

    for i in range(0, iterations):
        time.sleep(2)
        take_screenshot(driver, os.path.join(screenshots_folder_path, domain_name + '_sc_' + str(i + 2) + '.png'))
        difference_list = get_screenshot_difference(screenshots_folder_path, domain_name + '_sc_1.png', domain_name + '_sc_' + str(i + 2) + '.png')
        error_elements = set()
        error_texts = set()
        input_to_refill_elements = set()
        label_to_refill_elements = set()
        ordered_error_tuple = set()

        soup_after = bs(driver.page_source, 'html.parser')

        all_text = soup_after.find_all(text=True, recursive=True)

        for difference in difference_list:
            if len(difference.split()) >= 2:
                error_texts.add(determine_best_fit_text(all_text, difference)[1])

        for error_text in error_texts:
            error_element = soup_after.find(text=re.compile(re.escape(error_text)))
            error_element_before = soup_before.find(text=re.compile(re.escape(error_text)))
            if type(error_element_before) is not NavigableString and type(error_element) is NavigableString:
                error_elements.add(error_element)
                ordered_error_tuple.add((soup_after.find(text=re.compile(re.escape(error_text))).parent, error_text))


        type_from_error_message_rule = TypeFromErrorMessageRule()


        for error_element, error_text in ordered_error_tuple:
            affected_input_element, affected_label_element = type_from_error_message_rule.determine_type(error_element, error_text)

            if affected_input_element:
                if affected_input_element not in input_to_refill_elements:
                    input_to_refill_elements.add(affected_input_element)
                    fill_input_element(driver, build_schema(affected_input_element, 'input'), error_message=error_text, falsify_input=False)
                inferred_affected_tuples.append({
                    'affected_input': str(affected_input_element),
                    'affected_label': str(affected_label_element),
                    'error_message_element': str(error_element),
                    'error_text': error_text
                })

        time.sleep(2)
        take_screenshot(driver, os.path.join(screenshots_folder_path, domain_name + '_sc_' + str(i + 3) + '.png'))
    driver.quit()
