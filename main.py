import os
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from src.scrapers.SliderScraper import SliderScraper
from src.scrapers.GridScraper import GridScraper
from src.config import WEBDRIVER_PATH

# Instantiate options
opts = Options()
opts.add_argument("-headless") # Uncomment if the headless version needed

# Set the location of the webdriver
chrome_driver = WEBDRIVER_PATH

print(chrome_driver)

# Instantiate a webdriver
driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)

with open("genders.json", "r") as f:
    genders = json.loads(f.read())

for gender in genders:

    print(f"[LOG] Scraping {gender['name']}")

    grid = GridScraper(driver, gender["name"], gender["link"])
    grid.run()