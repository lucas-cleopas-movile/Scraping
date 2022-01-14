import os
import json
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from src.scrapers.GridScraper import GridScraper
from src.config import WEBDRIVER_PATH
from src.utils import upload_faq_files


def start_scraper(driver):

    with open("genders.json", "r") as f:
        genders = json.loads(f.read())

    for gender in genders:

        # Scraping the gender
        print(f"[LOG] Scraping {gender['name']}")
        grid = GridScraper(driver, gender["name"], gender["link"])
        grid.run(extend_page=True)
        print(f"[LOG] {gender['name']} scraped")

        # Upload the new content
        print(f"[LOG] Uploading new documents for {gender['name']}.")
        try:
            status, content = upload_faq_files(gender)
            if status == 200:
                print(f"[LOG] New documents was uploaded with success.")
            else:
                print(f"[ERROR] {content}")
        except Exception as e:
            print(f"[ERROR] An error occurred because: {str(e)}")


if __name__ == "__main__":

    # Instantiate options
    opts = webdriver.FirefoxOptions()

    # opts.add_argument("--no-sandbox") 
    opts.add_argument("--headless") 
    # opts.add_argument('--disable-dev-shm-usage')


    # Set the location of the webdriver
    chrome_driver = WEBDRIVER_PATH
    # service = Service(WEBDRIVER_PATH)

    print(chrome_driver)

    # Instantiate a webdriver
    driver = webdriver.Firefox(executable_path=WEBDRIVER_PATH, options=opts)

    start_scraper(driver)