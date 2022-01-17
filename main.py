import os
import json
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from src.scrapers.GridScraper import GridScraper
from src.config import WEBDRIVER_PATH, BASE_URL
from src.utils import upload_faq_files, get_indexes_files


def start_scraper(driver, indexes):

    for index in indexes:

        # Scraping the index
        try:
            print(f"[LOG] Scraping {index['name']}")
            grid = GridScraper(driver, index["name"], index["link"])
            grid.run(extend_page=False)
            print(f"[LOG] {index['name']} scraped")
        except Exception as e:
            print(f"[ERROR] An error occurred because: {str(e)}")
            continue

        # Upload the new content
        print(f"[LOG] Uploading new documents for {index['name']}.")
        try:
            status, content = upload_faq_files(index)
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

    # Start driver
    driver.get(BASE_URL)

    indexes_files = get_indexes_files()
    
    for indexes_file in indexes_files:

        print(f"[LOG] Scraping {indexes_file.split('/')[-1]}")

        with open(indexes_file, "r") as f:

            indexes = json.loads(f.read())

        start_scraper(driver, indexes)