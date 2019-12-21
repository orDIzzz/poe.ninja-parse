'''
'Класс для парсинга сайта poe-parser.ninja
'''

import lxml
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import os
import pprint

class POEParser:
    def __init__(self):
        self.main_link = 'https://poe.ninja/'
        self.PARSE_TEMPLATE = [
            {
                'category': 'Fragments',
                'link': 'fragments',
            },
            {
                'category': 'Oils',
                'link': 'oils',
            },
            {
                'category': 'Incubators',
                'link': 'incubators',
            },
            {
                'category': 'Scarabs',
                'link': 'scarabs',
            },
            {
                'category': 'Fossils',
                'link': 'fossils',
            },
            {
                'category': 'Resonators',
                'link': 'resonators',
            },
            {
                'category': 'Essences',
                'link': 'essences',
            },
            {
                'category': 'Divination Cards',
                'link': 'divinationcards',
            },
            {
                'category': 'Prophecies',
                'link': 'prophecies',
            },
            {
                'category': 'Unique Maps',
                'link': 'unique-maps',
            },
            {
                'category': 'Maps',
                'link': 'maps',
            },
            {
                'category': 'Unique Jewels',
                'link': 'unique-jewels',
            },
            {
                'category': 'Unique Flasks',
                'link': 'unique-flasks',
            },
            {
                'category': 'Unique Weapons',
                'link': 'unique-weapons',
            },
            {
                'category': 'Unique Armours',
                'link': 'unique-armours',
            },
            {
                'category': 'Unique Accessories',
                'link': 'unique-accessories',
            },
            {
                'category': 'Beasts',
                'link': 'beasts',
            },
            {
                'category': 'Currency',
                'link': 'currency',
            }
        ]
        self.LEAGUE = {'current': 'challenge', 'current_hc': 'challengehc', 'standard': 'standard',
                       'standard_hc': 'hardcore'}
        self.CATEGORIES = ['Fragments', 'Oils', 'Incubators', 'Scarabs', 'Fossils', 'Resonators', 'Essences',
                              'Divination Cards', 'Prophecies', 'Unique Maps', 'Maps', 'Unique Jewels', 'Unique Flasks',
                              'Unique Weapons', 'Unique Armours', 'Unique Accessories', 'Beasts', 'Currency']

    def __get_category_link(self, category):
        for category_name in self.PARSE_TEMPLATE:
            if category == category_name['category']:
                return category_name['link']

    def get_prices(self, category: list, league='challenge'):
        print(f'Works with: {[cat_name for cat_name in category]}')
        """
        Отправляет запрос на сайт poe-parser.ninja и возвращает словарь с ценами на предмет по запрошенным категориям
        Формат словаря:
        {
            'Fragments':
            {
                'Tul's Pure Breachstone': '40.0'
            }
        }
        """
        if len(category) == 0:
            category = self.CATEGORIES
        options = Options()
        options.headless = True
        other_format_category = ['Currency', 'Fragments']
        result = {}
        for category_name in category:
            category_result = []
            driver = webdriver.Firefox(options=options, service_log_path=os.path.devnull)
            league_url = self.main_link + league + '/' + self.__get_category_link(category_name)
            driver.get(league_url)
            do_it = True
            waiting_element_selector = '.currency-overview' if category_name in other_format_category else '.item-overview'
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, waiting_element_selector))
                )
                while do_it:
                    try:
                        btn_show_more = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '.show-more'))
                        )
                        driver.execute_script("arguments[0].click();", btn_show_more)
                    except TimeoutException:
                        break
                    except NoSuchElementException:
                        break
                soup = BeautifulSoup(driver.page_source, "lxml")
                uncleaned_list = soup.select_one(waiting_element_selector + '>table>tbody')
                if category in other_format_category:
                    name_selector = 'td>div>span'
                    for item in uncleaned_list.select('tr'):
                        name = item.select_one(name_selector).attrs["title"]
                        price = item.select("tr>td")[2].select(".currency-amount")[0].attrs["title"]
                        category_result.append({
                            name: price
                        })
                    driver.quit()
                    result[category_name] = category_result
                else:
                    name_selector = 'td>div>span'
                    for item in uncleaned_list.select('tr'):
                        name = item.select_one(name_selector).attrs["title"]
                        price = item.select("td")[2].select("span")[-2].text[:-1]
                        category_result.append({
                            name: price
                        })
                    driver.quit()
                    result[category_name] = category_result
            finally:
                driver.quit()
        return result
