import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from src.scrapers.SliderScraper import SliderScraper
from src.scrapers.GridScraper import GridScraper
from src.config import WEBDRIVER_PATH

# Instantiate options
opts = webdriver.ChromeOptions()

opts.add_argument("--no-sandbox") 
opts.add_argument("--headless") 
# opts.add_argument('--disable-dev-shm-usage')


# Set the location of the webdriver
chrome_driver = WEBDRIVER_PATH
service = Service(WEBDRIVER_PATH)


print(chrome_driver)

# Instantiate a webdriver
driver = webdriver.Chrome(options=opts, service=service)

with open("genders.json", "r") as f:
    genders = json.loads(f.read())

for gender in genders:

    print(f"[LOG] Scraping {gender['name']}")
    
    driver = webdriver.Chrome(options=opts, service=service)
    grid = GridScraper(driver, gender["name"], gender["link"])

    grid.run(extend_page=True)

    print(f"[LOG] {gender['name']} scraped")