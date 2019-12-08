from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = r'https://poe.ninja/challenge/oils'

driver = webdriver.Firefox()
driver.get(URL)
assert "Oils" in driver.title
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'item-overview'))
    )
    mylist = driver.find_element_by_css_selector('.item-overview>table>tbody')
    # mylist = driver.find_element_by_class_name('item-overview')
    print(mylist.text)
finally:
    driver.quit()
