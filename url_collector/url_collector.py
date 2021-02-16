import json
import os
import pathlib
from zipfile import ZipFile

import requests

from form_filler.form_filler import fill_form_by_url
from scraper.scraper import extract_element_by_element_tag_from_page_source
from utilities.constants import MIN_INPUT_ELEMENTS


def should_collect_url(url: str) -> bool:
    try:
        input_elements = extract_element_by_element_tag_from_page_source(url, 'input')
        if input_elements is not None and len(input_elements) > MIN_INPUT_ELEMENTS:
            print(url)
            return True
    except requests.exceptions.ConnectionError:
        return False


if __name__ == "__main__":

    path = pathlib.Path(__file__).parent.absolute()
    parent_path, tail = os.path.split(path)
    sso_dataset_zip_path = os.path.join(parent_path, 'sso_dataset', 'sso-study-data.zip')
    sso_dataset_zip_file = ZipFile(sso_dataset_zip_path, 'r')
    sso_dataset_zip_file.extract('sso-study-data.json')

    sso_dataset_path = os.path.join(parent_path, 'url_collector', 'sso-study-data.json')
    url_list_file_path = os.path.join(parent_path, 'url_collector', 'url_list.txt')

    with open(sso_dataset_path, 'r') as sso_dataset_file, open(url_list_file_path, 'w') as url_list_file:
        for line in sso_dataset_file:
            sso_record_dict = json.loads(line)
            for url in sso_record_dict['url']:
                try:
                    fill_form_by_url(url)
                except Exception:
                    pass
