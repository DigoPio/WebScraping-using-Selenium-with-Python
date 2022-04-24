from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import json



def scrape_data_from_website():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    webscraper_url = 'https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops'
    driver.get(webscraper_url)
    time.sleep(2)
    laptops= driver.find_elements(By.CLASS_NAME, 'caption')
    laptops_list = [element.text.split('\n') for element in laptops if 'Lenovo' in element.text or 'ThinkPad' in element.text]
    titles = driver.find_elements(By.CLASS_NAME, 'title')
    laptops_titles = [title.get_attribute('title') for title in titles if 'Lenovo' in title.text or 'ThinkPad' in title.text]
    return laptops_list, laptops_titles

def save_data(index, title, price, description):
    new_data = {
        index:{
        'Model': title,
        'Price': price,
        'Description': description,
        }
    }
    try:
        with open('data.json', mode='r') as json_data:
            data = json.load(json_data)
    except FileNotFoundError:
        with open('data.json', mode='w') as json_data:
            json.dump(new_data, json_data, indent=4)
    else:
        data.update(new_data)
        with open('data.json', mode='w') as json_data:
            json.dump(data, json_data, indent=4)

def get_scraped_data_and_save():
    index = 0
    laptops_list, laptops_titles = scrape_data_from_website()
    for item in laptops_list:
        price = item[0]
        title = laptops_titles[index]
        description = item[2]
        save_data(index, title, price, description)
        index += 1



get_scraped_data_and_save()