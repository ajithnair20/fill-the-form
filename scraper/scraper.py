# Importing Libraries
import os
import pathlib

import requests
import requests as req
from bs4 import BeautifulSoup as bs
# Set urls and header
from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from schema.schema import build_schema

app = Flask(__name__)

headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X)'}
path = pathlib.Path(__file__).parent.absolute()
parent, tail = os.path.split(path)
chromedriver_folder_path = os.path.join(parent, 'chromedriver_directory', 'chromedriver')

chromedriver = chromedriver_folder_path


def extract_element_by_element_tag(url: str, element_tag: str):
    try:
        res = req.get(url, headers=headers)
        if 200 <= res.status_code < 300:
            soup = bs(res.content, 'lxml')

            elements = soup.find_all(element_tag)
            elements = [build_schema(element, element_tag) for element in elements]
            return elements
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError


def extract_element_by_element_tag_from_page_source(url: str, element_tag: str):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--start-maximized')

    driver = webdriver.Chrome(chromedriver, options=chrome_options)

    try:
        res = req.get(url, headers=headers)
        if 200 <= res.status_code < 300:
            driver.get(url)
            driver.set_window_size(1920, 4000)
            driver.implicitly_wait(300)
            page_source = driver.page_source
            soup = bs(page_source, 'html.parser')
            elements = soup.find_all(element_tag)
            elements_metadata = [build_schema(element, element_tag) for element in elements]
            return elements_metadata
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError
