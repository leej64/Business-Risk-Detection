from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime
import requests
import json
import urllib
from article_content_crawler import fetch_article_content_and_publish_time_and_title
import yfinance as yf
from sp500_symbols import sp500_symbols
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


# Scroll to the end of page for given count of times
# https://stackoverflow.com/questions/48850974/selenium-scroll-to-end-of-page-in-dynamically-loading-webpage
def scroll_down(driver, scroll_cnt):
    """A method for scrolling the page."""
    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")
    # Scroll the page
    while scroll_cnt > 0:
        # Scroll down to the bottom.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load the page.
        time.sleep(0.5)
        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")
        # Break if reaching end of page
        if new_height == last_height:
            break
        # Update with new page state
        last_height = new_height
        scroll_cnt -= 1


# Create the url for searching given keyword from given site within given timeframe
def create_google_search_url(keyword, site, min_m, min_d, min_y, max_m, max_d, max_y):
    search_url_start = "https://www.google.com/search?"
    search_url_end = "q=intitle:{}+site%3A{}&".format(keyword, site)\
        + "cd_min%3A{}%2F{}%2F{}%2Ccd_max%3A{}%2F{}%2F{}".format(min_m, min_d, min_y, max_m, max_d, max_y)
    return search_url_start + search_url_end


# Read dataframe from local csv
def read_from_csv(filename):
    df = pd.read_csv(filename)
    return df

# Write dataframe to local csv
def write_to_local_csv(filename, df, has_header):
    df.to_csv(filename, sep = "`", mode = "a", index = False, header = has_header)


# Fetch and return the page source of given google search url
def fetch_google_search_content(url):
    # Start session
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    driver.get(url)
    time.sleep(5)
    scroll_down(driver, 5)
    # Return given page's source html
    return driver.page_source


# Gather all links and titles in given page
def parse_page_link_and_title(page_source, site):
    all_urls = []
    all_titles = []
    # Use beautiful soup to find all urls in search results
    soup = BeautifulSoup(page_source, "html.parser")        
    all_search_divs = soup.find_all("a", href = True)
    for div in all_search_divs:
        url = div["href"]
        title = None
        # Add to list if it's yahoo finance website
        if url.startswith(site):
            # Get title
            h3 = div.find("h3")
            if h3 != None:
                title = h3.text
            all_urls.append(url)
            all_titles.append(title)
    return all_urls, all_titles
    

# Get full name of given symbol's company
def get_company_full_name(symbol):
    try:
        ticker = yf.Ticker(symbol)
        return ticker.info["longName"]
    except Exception as e:
        print("Failure of getting long name of {}".format(symbol))
        return None

if __name__ == "__main__":
    # List of companies to look into
    symbol_list = [
        "AAPL",
        "GOOG",
        "MSFT",
        "AMZN",
        "JPM",
        "BRK-B",
        "XOM",
        "PFE",
        "UNH",
        "V",
        "T",
        "CSCO",
        "PEP",
        "MMM",
        "LLY",
        "IBM",
        "CRM",
        "UNP",
        "PYPL",
        "HON",
        "NKE"
    ]

    # Number of articles to crawl for each company
    article_limit = 50
    #url = create_google_search_url("amazon", "https://finance.yahoo.com/news/", 1, 1, 2018, 12, 31, 2018)
    #url = "https://www.google.com/search?q=inurl:3M+site%3Ahttps%3A%2F%2Ffinance.yahoo.com%2Fnews%2F&sca_esv=00a8d62a2b12d55d&rlz=1C1ONGR_enUS1070US1070&tbs=cdr%3A1%2Ccd_min%3A1%2F1%2F2018%2Ccd_max%3A12%2F31%2F2018"
    #print(url)
    
    
    # Columns of dataset
    columns = ["title", "link", "timestamp", "content", "publish_time", "related_tickers", "risk_type"]
    current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    file_name = "./newsdata/historicalNews - " + current_datetime + ".csv"
    need_header = True
    # Go through each symbol
    for symbol in sp500_symbols:
        df = pd.DataFrame(columns = columns)
        # Fetch urls and titles for given company within timeframe
        company_full_name = get_company_full_name(symbol)
        # Skip if can't get company long name
        if company_full_name == None:
            continue
        url = create_google_search_url(company_full_name, \
                                       "https://finance.yahoo.com/news/", \
                                        1, 1, 2018, 12, 31, 2018)
        page_source = fetch_google_search_content(url)
        url_list, title_list = parse_page_link_and_title(page_source, "https://finance.yahoo.com/news/")

        # Fetch article contents and append to dataframe
        for i in range(len(url_list)):
            if i >= article_limit:
                break
            url = url_list[i]
            title = title_list[i]
            content, publish_time, news_title = fetch_article_content_and_publish_time_and_title(url)
            if news_title != None:
                title = news_title
            df.loc[len(df)] = [title, url, current_datetime, content, publish_time, symbol, ""]
        
        # Write to local csv files
        write_to_local_csv(file_name, df, need_header)
        if need_header == True:
            need_header = False
