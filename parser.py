from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import lxml
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException
from bs4 import BeautifulSoup
"""
Fragments, Oils, Incubators, Scarabs, Fossils, Resonators, Essences, Divination Cards, 
Prophecies, Unique Maps, Maps, Unique Jewels, Unique Flasks, Unique weapons, Unique Armours, Unique Accessories, Beasts
.item-overview>table>tbody
"""
PARSE_TEMPLATE = [
    {
        'category': 'Fragments',
        'link': 'https://poe.ninja/standard/fragments',
    },
    {
        'category': 'Oils',
        'link': 'https://poe.ninja/standard/oils',
    },
    {
        'category': 'Incubators',
        'link': 'https://poe.ninja/standard/incubators',
    },
    {
        'category': 'Scarabs',
        'link': 'https://poe.ninja/standard/scarabs',
    },
    {
        'category': 'Fossils',
        'link': 'https://poe.ninja/standard/fossils',
    },
    {
        'category': 'Resonators',
        'link': 'https://poe.ninja/standard/resonators',
    },
    {
        'category': 'Essences',
        'link': 'https://poe.ninja/standard/essences',
    },
    {
        'category': 'Divination Cards',
        'link': 'https://poe.ninja/standard/divinationcards',
    },
    {
        'category': 'Prophecies',
        'link': 'https://poe.ninja/standard/prophecies',
    },
    {
        'category': 'Unique Maps',
        'link': 'https://poe.ninja/standard/unique-maps',
    },
    {
        'category': 'Maps',
        'link': 'https://poe.ninja/standard/maps',
    },
    {
        'category': 'Unique Jewels',
        'link': 'https://poe.ninja/standard/unique-jewels',
    },
    {
        'category': 'Unique Flasks',
        'link': 'https://poe.ninja/standard/unique-flasks',
    },
    {
        'category': 'Unique Weapons',
        'link': 'https://poe.ninja/standard/unique-weapons',
    },
    {
        'category': 'Unique Armours',
        'link': 'https://poe.ninja/standard/unique-armours',
    },
    {
        'category': 'Unique Accessories',
        'link': 'https://poe.ninja/standard/unique-accessories',
    },
    {
        'category': 'Beasts',
        'link': 'https://poe.ninja/standard/beasts',
    },
    {
        'category': 'Currency',
        'link': 'https://poe.ninja/standard/currency',
    }
]


def parse_page(category, link):
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    driver.get(link)
    category_list = ['Currency', 'Fragments']
    do_it = True
    waiting_element_selector = '.currency-overview' if category in category_list else '.item-overview'
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
        uncleaned_list = soup.select_one(waiting_element_selector+'>table>tbody')
        result = []
        if category in category_list:
            name_selector = 'td>div>span'
            for item in uncleaned_list.select('tr'):
                name = item.select_one(name_selector).attrs["title"]
                price = item.select("tr>td")[2].select(".currency-amount")[0].attrs["title"]
                result.append({
                    'item_name': name,
                    'price': price
                })
            driver.quit()
            print(f'len(result) = {len(result)}')
            return result
        else:
            name_selector = 'td>div>span'
            for item in uncleaned_list.select('tr'):
                name = item.select_one(name_selector).attrs["title"]
                price = item.select("td")[-2].select("span")[-2].text[:-1]
                result.append({
                    'item_name': name,
                    'price': price
                })
            driver.quit()
            print(f'len(result) = {len(result)}')
            return result
    finally:
        driver.quit()


def main():
    full_cats = {}
    for cat in PARSE_TEMPLATE:
        print(cat['category'])
        full_cats[cat['category']] = parse_page(**cat)
    with open('parse.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(full_cats))


if __name__ == '__main__':
    main()
