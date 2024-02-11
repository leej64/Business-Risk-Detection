from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime
import requests

'''
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
        
'''


def parse_article_htmp(soup):
    # Find article
    article_text = ""
    paragraphs = soup.find_all("p")
    for p in paragraphs:
        article_text += p.text
        
    # Find time
    publish_time = None
    time_div = soup.find_all("time")
    for t in time_div:
        if t.has_attr("datetime"):
            publish_time = t["datetime"]
            
    return article_text, publish_time


def fetch_article_content_and_publish_time(url): 
    try:
        print(url)
        
        # Try requests first and selenium next
        r = requests.get(url)
        #print(r.text)
        soup = BeautifulSoup(r.text, "html.parser")
        content, publish_time = parse_article_htmp(soup)

        if publish_time != None:
            return content, publish_time
        
        # Try selenium next
        # Start session
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        driver.close()
        driver.quit()

        content, publish_time = parse_article_htmp(soup)
        return content, publish_time
        
        # Use BS to fetch HTML
        
            
        
    except Exception as e:
        raise e

def read_from_csv(filename):
    df = pd.read_csv(filename)
    return df

def write_to_local_csv(filename, df):
    df.to_csv(filename, sep = "`", mode = "a", index = False)

    
