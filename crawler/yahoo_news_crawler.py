from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime
import requests


def scroll_down(driver):
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
        time.sleep(5)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:

            break

        last_height = new_height
        print("111")
    return driver

def find_all_press_release_links(url, type_tag, symbol):
    all_news_link = []
    while len(all_news_link) == 0:
        print("Start trying")
        # Start session
        chrome_options = webdriver.ChromeOptions()
        #chrome_options.add_argument('headless')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url + symbol + "/" + type_tag + "?p=" + symbol)
        driver = scroll_down(driver)
        with open('aa.html', 'w') as f:
            f.write(driver.page_source)
        
        driver.implicitly_wait(10)

        # Use BS to fetch HTML
        soup = BeautifulSoup(driver.page_source, "html.parser")

        li = soup.find_all("li", {"class": "js-stream-content Pos(r)"})
        # Find the urls to the articles
        for article in li:
            div1 = article.find("div")
            div2 = div1.find("div")
            div3 = div2.find_all("div")
            for d in div3:
                a = d.find("a")
                if a != None:
                    url = a["href"]
                    if url[0:5] == "/news":
                        all_news_link.append("https://finance.yahoo.com" + url)
        
    return all_news_link
    

def fetch_title(url):
    title = ""
    while len(title) == 0:
        # Start session
        r = requests.get(url)
        # Use BS to fetch HTML
        soup = BeautifulSoup(r.text, "html.parser")
        
        headers = soup.find_all("div", {"class": "caas-title-wrapper"})
        # Find title
        for h in headers:
            h1 = h.find("h1")
            if len(title) == 0:
                title = h1.text
        
    return title




def fetch_article_content(url): 
    article_text = ""
    while len(article_text) == 0:
        # Start session
        r = requests.get(url)
        # Use BS to fetch HTML
        soup = BeautifulSoup(r.text, "html.parser")
        
        paragraphs = soup.find_all("p")
        # Find article
        for p in paragraphs:
            article_text += p.text
        
    return article_text
        

def write_to_local_csv(filename, df):
    df.to_csv(filename, sep = "`", mode = "a", index = False)

if __name__ == "__main__":
    symbol_list = [
        "AMZN",
        #"META",
        #"APPL",
        #"GOOG",
        #"ARM",
        #"NVDA"
    ]
    tag_list = [
        "news",
        "press-releases"
    ]
    for tag in tag_list:
        for symbol in symbol_list:
            start_time = datetime.now()
            now = datetime.now()

            url = "https://finance.yahoo.com/quote/"
            all_press_release_link = find_all_press_release_links(url, tag, symbol)
            print(all_press_release_link)
            dict = {
                "title": [],
                "content": [],
                "timestamp": [],
                "symbol": []
            }
            for url in all_press_release_link:
                title = fetch_title(url)
                article_text = fetch_article_content(url)
                #print(title, article_text)
                dict["title"].append(title)
                dict["content"].append(article_text)
                dict["timestamp"].append(now)
                dict["symbol"].append(symbol)
            write_to_local_csv(tag + " - out.csv", pd.DataFrame(data = dict))
            end_time = datetime.now()
            print("Time elapsed:", end_time - start_time)
        
    

