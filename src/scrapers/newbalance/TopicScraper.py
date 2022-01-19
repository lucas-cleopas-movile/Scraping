import os
import pandas as pd
from bs4 import BeautifulSoup
import time
import pandas as pd

BASE_URL = "https://newbalance.force.com"


class TopicScraper:

    def __init__(self, driver, url):

        self.url = url
        self.base_url = self.get_base_url(url)
        self.driver = driver

        self.load_url(self.url)
    
    def get_base_url(self, url):

        splitted_url = url.split("/")

        return splitted_url[0] + "//" + splitted_url[2]


    def load_url(self, url):

        print(f"[LOG] Loading {url}")

        self.driver.get(url)

        time.sleep(5)


    def extend_page(self):

        print("[LOG] Extending the page.")

        soup = BeautifulSoup(self.driver.page_source, features="lxml").findAll("button", class_="slds-button slds-button_brand slds-align_absolute-center loadmore")
        
        while len(soup) != 0:
            
            try:

                button = self.driver.find_element_by_xpath('//button[text()="Load more"]')

                button.click()

                time.sleep(5)

                soup = BeautifulSoup(self.driver.page_source, features="lxml").findAll("button", class_="slds-button slds-button_brand slds-align_absolute-center loadmore")
                                
            except Exception as e:

                print(f"[ERROR] {str(e)}")

                break
        
        print("[LOG] Page extended.")


    
    def get_topics(self, extend_page=True):


        print("[LOG] Getting topics.")

        if extend_page:
            self.extend_page()

        soup = BeautifulSoup(self.driver.page_source)

        topics = []

        for topic in soup.findAll("li", class_="article-item selfServiceArticleListItem"):

            topics.append({"topic": topic.article.a.h2.get_text(), "link": self.base_url + topic.article.a["href"]})
        
        print("[LOG] Topics was found.")

        return topics

    
    def get_topic_content(self, topic_link):

        print(f"[LOG] Getting content from {topic_link}")

        self.load_url(topic_link)

        topic_title = BeautifulSoup(self.driver.page_source, features="lxml").find("h1", class_="article-head selfServiceArticleHeaderDetail").get_text()

        summary = BeautifulSoup(self.driver.page_source, features="lxml").find("p", class_="article-summary selfServiceArticleHeaderDetail").get_text()
        
        # try:
        #     details = BeautifulSoup(self.driver.page_source, features="lxml").find("div", class_="slds-rich-text-editor__output uiOutputRichText forceOutputRichText").get_text()
        # except:
        #     print("Details not found")
        details = ""

        content = summary + "\n" + details

        print(f"[LOG] Content from {topic_link} was scraped.")

        return topic_title, content
    

