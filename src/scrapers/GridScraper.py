import os
import pandas as pd
from bs4 import BeautifulSoup
import time
from src.config import BASE_URL
from src.utils import export_faq_csv


class GridScraper:

    def __init__(self, driver, name, link):

        self.name = name.lower()
        self.url = link
        self.driver = driver
        self.df_out = pd.DataFrame(columns=['question', 'answer', 'document'])

        self.load_url(self.url)


    def load_url(self, url):

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
                
            except Exception as e:
                print(f"[ERROR] {str(e)}")
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

    
    def run(self, extend_page=True):

        if extend_page:
            self.extend_page()

        try:
            
            contents = self.get_contents()

            for content in contents:
                
                answer = f"Veja o vídeo '{content['title']}' clicando em: {content['link']}"

                row = {"question": content["title"], "answer": answer, 'document': self.url}

                self.df_out = self.df_out.append(row, ignore_index=True)
            
            export_faq_csv(self.df_out, self.name)
            
        except Exception as e:

            print(f'[ERROR] An error occurred with this url: "{self.url}"')
            print(str(e))
