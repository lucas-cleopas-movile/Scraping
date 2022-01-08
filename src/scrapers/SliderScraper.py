from bs4 import BeautifulSoup
from src.config import BASE_URL


class SliderScraper:

    def __init__(self, driver, url):

        self.url = url
        self.driver = driver

        self.load_url(self.url)


    def load_url(self, url):

        self.driver.get(url)


    def get_slider_items(self):

        # Parse processed webpage with BeautifulSoup
        soup = BeautifulSoup(self.driver.page_source)

        soup2 = soup.find("div", class_="playkit-slider__track")

        items = []

        for item in soup2.findAll("div", class_="playkit-slider__item"):
            items.append({"name": item.a["title"], "link": BASE_URL + item.a["href"]})
            print(item.a["title"], item.a["href"])
        
        return items

