import pandas as pd
from selenium import webdriver
from src.scrapers.newbalance.TopicScraper import TopicScraper
from src.utils import export_faq_csv

urls = [
    "https://support.newbalance.com/s/topic/0TO1L000000ETPvWAO/fit-and-activity-guide",
    "https://newbalance.force.com/nbusa/s/topic/0TO1L000000ETPbWAO/general",
    "https://newbalance.force.com/nbusa/s/topic/0TO1L000000ETPgWAO/my-order",
    "https://newbalance.force.com/nbusa/s/topic/0TO1L000000ETPlWAO/buy-online-pick-up-instore",
    "https://newbalance.force.com/nbusa/s/topic/0TO1L000000ETQ0WAO/products",
    "https://newbalance.force.com/nbusa/s/topic/0TO1L000000MQFWWA4/returns"
]


# Instantiate options
opts = webdriver.FirefoxOptions()

# opts.add_argument("--no-sandbox") 
opts.add_argument("--headless") 
# opts.add_argument('--disable-dev-shm-usage')


# Set the location of the webdriver
WEBDRIVER_PATH = "src/webdriver/geckodriver"
# service = Service(WEBDRIVER_PATH)

print(WEBDRIVER_PATH)

# Instantiate a webdriver
driver = webdriver.Firefox(executable_path=WEBDRIVER_PATH, options=opts)
driver.get("https://support.newbalance.com")

df_out = pd.DataFrame(columns=['question', 'answer', 'document'])

for url in urls:

    print(f"[LOG] Scraping {url}")

    try:

        tc = TopicScraper(driver, url)

        topics = tc.get_topics()

        n_topics = len(topics)

        count = 1

        for topic in topics:

            print(f"[LOG] Getting content {count}/{n_topics}")

            question, answer = tc.get_topic_content(topic["link"])

            if len(question) != 0 and len(answer) != 0:

                row = {"question": question, "answer": answer, 'document': topic["link"]}

                df_out = df_out.append(row, ignore_index=True)

                count += 1
            
            else:

                print(f"[LOG] Topic {count}/{n_topics} was not scraped.")

        print(f"[LOG] Scraping {url} was finished.")
    
    except Exception as e:

        print(f"[ERROR] An error occurred because: {str(e)}")
        
        continue

export_faq_csv(df_out, "newbalance")

# question, answer = tc.get_topic_content("https://support.newbalance.com/s/article/How-Can-I-Apply-for-a-Job-at-New-Balance")
# print(question, answer)