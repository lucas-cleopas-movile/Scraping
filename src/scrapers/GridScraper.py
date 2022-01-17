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

        time.sleep(5)

    
    def avoid_cookie_banner(self):

        print(f"[LOG] Clicking cookie banner.")

        try:

            button = self.driver.find_element_by_class_name("cookie-banner-lgpd_accept-button")

            button.click()

            print(f"[LOG] Cookie banner clicked.")

            time.sleep(5)

            return True
        
        except Exception as e:

            print(f"[ERROR] Cookie banner not found.")

            return False
    

    def extend_page(self):

        print("[LOG] Extending the page.")

        soup = []
                
        while len(soup) == 0:
            
            try:

                button = self.driver.find_element_by_id("action-button-Veja mais")

                button.click()

                time.sleep(5)

                soup = BeautifulSoup(self.driver.page_source, features="lxml").findAll("div", class_="action-button action-button--hidden")
                
            except Exception as e:

                print(f"[ERROR] {str(e)}")

                print(f"[LOG] Trying avoid cookie banner.")
                
                is_cookie = self.avoid_cookie_banner()
                        
                if not is_cookie:

                    break
        
        print("[LOG] Page extended.")


    def get_contents(self):

        self.avoid_cookie_banner()
        
        soup = BeautifulSoup(self.driver.page_source, features="lxml").findAll("li", class_="playkit-offers__list-li playkit-offers__list-li--poster")

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
            
        except Exception as e:

            print(f'[ERROR] An error occurred with this url: "{self.url}"')
            print(str(e))

            return
        
        for content in contents:
                
            answer = f"Veja o vídeo '{content['title']}' clicando em: {content['link']}"

            row = {"question": content["title"], "answer": answer, 'document': self.url}

            self.df_out = self.df_out.append(row, ignore_index=True)

        if len(self.df_out) == 0:

            raise Exception("No item was scraped!")
        
        export_faq_csv(self.df_out, self.name)

