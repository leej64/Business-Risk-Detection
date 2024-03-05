import pandas as pd
import yfinance as yf
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
import time
from datetime import datetime
from bs4 import BeautifulSoup

from sp500_symbols import sp500_symbols
from article_content_crawler import fetch_article_content_and_publish_time_and_title



# Write dataframe to local csv.

def write_to_local_csv(filename, df, has_header):
    df.to_csv(filename, sep = "`", mode = "a", index = False, header = has_header)


# Get full name of given symbol's company
def get_company_full_name(symbol):
    try:
        ticker = yf.Ticker(symbol)
        return ticker.info["longName"]
    except Exception as e:
        print("Failure of getting long name of {}".format(symbol))
        return None


# date must be in format of YYYY-mm-dd
def create_ddg_search_url(keyword, site, start_date, end_date):
    url_start = "https://html.duckduckgo.com/html/"
    keyword.replace(" ", "+")
    url_end = "?q={}+site%3A{}&va=c&t=hb&df={}..{}&ia=web".format(keyword, site, start_date, end_date)
    return url_start + url_end


# Fetch and return the page source of given google search url
def fetch_ddg_search_content(url):
    # Start session
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    driver.get(url)
    time.sleep(5)
    # Return given page's source html
    return driver.page_source


# Gather all links and titles in given page
def parse_ddg_page_links(page_source, site):
    all_urls = []
    # Use beautiful soup to find all urls in search results
    soup = BeautifulSoup(page_source, "html.parser")        
    all_search_divs = soup.find_all("a", class_ = "result__url")
    for div in all_search_divs:
        url = (div.text).strip()

        # Add to list if it's yahoo finance website
        if url.startswith(site):
            all_urls.append(url)
            
    return all_urls
    


if __name__ == "__main__":
    # Columns of dataset
    columns = ["title", "link", "timestamp", "content", "publish_time", "related_tickers", "risk_type"]
    current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    file_name = "./newsdata/historicalNews - ddg - " + current_datetime + ".csv"
    need_header = True

    article_limit = 50

    for symbol in sp500_symbols:
        df = pd.DataFrame(columns = columns)
        # Fetch urls and titles for given company within timeframe
        company_full_name = get_company_full_name(symbol)
        # Skip if can't get company long name
        if company_full_name == None:
            continue
        url = create_ddg_search_url(company_full_name, "https://finance.yahoo.com/news/",\
                                    "2018-01-01", "2018-12-31")
        html = fetch_ddg_search_content(url)
        url_list = parse_ddg_page_links(html, "finance.yahoo.com/news/")
        print(url_list)

        # Fetch article contents and append to dataframe
        for i in range(len(url_list)):
            if i >= article_limit:
                break
            url = url_list[i]
            print(url)
            content, publish_time, news_title = fetch_article_content_and_publish_time_and_title("https://" + url)
            title = news_title
            df.loc[len(df)] = [title, url, current_datetime, content, publish_time, symbol, ""]
            time.sleep(1)
        # Write to local csv files
        write_to_local_csv(file_name, df, need_header)
        if need_header == True:
            need_header = False

        

        