from selenium import webdriver
from contextlib import contextmanager
import os
import json


class KenpomScraper:
    def __init__(self):
        self.email = os.getenv('KENPOM_EMAIL')
        self.password = os.getenv("KENPOM_PASSWORD")
        self.home_address = 'http://kenpom.com'
        self.tournament_name = "Men's 2021 NCAA Tournament"
        self.year = 2021

    @contextmanager
    def browser(self):
        browser = webdriver.Chrome()
        try:
            yield browser
        finally:
            browser.close()


    def sign_in(self, browser):
        browser.get(self.home_address)
        browser.find_element('name', 'email').send_keys(self.email)
        browser.find_element('name', 'password').send_keys(self.password)
        browser.find_element('name', 'submit').click()

    def write_to_file(self, file_dir, file_name, data):
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)

        file_path = (file_dir / file_name).resolve()
        data_file = open(file_path, 'w')
        file_data = {
            "tournament_name": self.tournament_name,
            "year": self.year,
            "data": data
        }
        json.dump(file_data, data_file)
        data_file.close()

