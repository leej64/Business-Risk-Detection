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

import yfinance as yf
from sp500_symbols import sp500_symbols 
from article_content_crawler import fetch_article_content_and_publish_time
import os


def parse_news(news):
    try:
        title = news["title"]
        link = news["link"]
        ts = news["providerPublishTime"]
        formatted_timestamp = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        content, publish_time = fetch_article_content_and_publish_time(link)
        related_tickers = news.get("relatedTickers", [])
        risk_type = ""
        return [title, link, formatted_timestamp, content, publish_time, related_tickers, risk_type]
    except Exception as e:
        print(str(e))


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
    '''
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
    '''

    # Columns of dataset
    columns = ["title", "link", "timestamp", "content", "publish_time", "related_tickers", "risk_type"]
    current_datetime = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
    file_name = "./newsdata/latestNews - " + current_datetime + ".csv"
    for symbol in sp500_symbols:
        df = pd.DataFrame(columns = columns)
        tick = yf.Ticker(symbol)
        # Get all recent news
        all_news = tick.news
        # Parse data of each news article
        for news in all_news:
            df.loc[len(df)] = parse_news(news)
        # Write to local csv file
        write_to_local_csv(file_name, df)
        time.sleep(1)

    

