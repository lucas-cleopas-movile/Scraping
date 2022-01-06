from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import os
import time



BASE_URL = "https://globoplay.globo.com"


class SliderWebScraper:

    def __init__(self, driver, url):

        self.url = url
        self.driver = driver

        self.load_html(self.url)


    def load_html(self, url):

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


class GridWebScraper:

    def __init__(self, driver, name, link):

        self.name = name.lower()
        self.url = link
        self.driver = driver
        self.df_out = pd.DataFrame(columns=['question', 'answer', 'document'])

        self.load_html(self.url)


    def load_html(self, url):

        self.driver.get(url)

    
    def extend_page(self):

        print("[LOG] Extending the page.")

        soup = BeautifulSoup(self.driver.page_source).findAll("div", class_="action-button action-button--hidden")
        
        while len(soup) == 0:

            try:

                time.sleep(2)

                button = self.driver.find_element_by_id("action-button-Veja mais")

                button.click()

                time.sleep(2)

                soup = BeautifulSoup(self.driver.page_source).findAll("div", class_="action-button action-button--hidden")
                
            except NoSuchElementException:
                print("[ERROR] Button 'See more' not found.")
                break
        
        print("[LOG] Page extended.")


    def get_contents(self):
        
        soup = BeautifulSoup(self.driver.page_source).findAll("li", class_="playkit-offers__list-li playkit-offers__list-li--poster")

        contents = []

        for item in soup:

            has_child = len(item.find_all()) != 0
            
            if has_child:
            
                title = item.find("span", class_="playkit-thumb__thumb-under-poster").get_text()
                
                href = item.find("span", class_="playkit-thumb__thumb-link-wrapper").div.a["href"]
                link = BASE_URL + href
                
                contents.append({"title": title, "link": link})
                        
        return contents
    

    def export_faq_csv(self):

        path = f'data/'

        if not os.path.isdir(path):
            os.makedirs(path)

        self.df_out.to_csv(f'{path}/{self.name}_faq.csv')


    
    def run(self, extend_page=True):

        if extend_page:
            self.extend_page()

        try:
            
            contents = self.get_contents()

            for content in contents:

                row = {"question": content["title"], "answer": content["link"], 'document': self.url}

                self.df_out = self.df_out.append(row, ignore_index=True)
            
            self.export_faq_csv()
            
        except Exception as e:

            print(f'[ERROR] An error occurred with this url: "{self.url}"')
            print(str(e))



if __name__ == "__main__":

    # Instantiate options
    opts = Options()
    opts.add_argument("-headless") # Uncomment if the headless version needed

    # Set the location of the webdriver
    chrome_driver = os.getcwd() + "/chromedriver"

    # Instantiate a webdriver
    driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)

    url = BASE_URL + "/categorias/filmes/"
    slider = SliderWebScraper(driver, url)
    genders = slider.get_slider_items()
    # gender = {"name": "Biografia", "link": "https://globoplay.globo.com/categorias/biografias/"}

    print(genders)

    for gender in genders:

        print("[LOG] Scraping ", gender["name"])
        grid = GridWebScraper(driver, gender["name"], gender["link"])
        grid.run()