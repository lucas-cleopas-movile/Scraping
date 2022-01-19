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

        items = []

        for item in soup.findAll("li", class_="article-item selfServiceArticleListItem"):
            print({"topic": item.article.a.h2.get_text(), "link": item.article.a["href"]})
            items.append({"topic": item.article.a.h2.get_text(), "link": item.article.a["href"]})
            
            break
        
        return items

