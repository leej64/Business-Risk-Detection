from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from bs4 import BeautifulSoup
import time
import pandas as pd
from datetime import datetime
import requests

def fetch_article_content(url): 
    print(url)
    article_text = ""
    # Start session
    r = requests.get(url)
    #print(r.text)
    # Use BS to fetch HTML
    soup = BeautifulSoup(r.text, "html.parser")
        
    paragraphs = soup.find_all("p")
    # Find article
    for p in paragraphs:
        article_text += p.text
        
        
    return article_text

def read_from_csv(filename):
    df = pd.read_csv(filename)
    return df

def write_to_local_csv(filename, df):
    df.to_csv(filename, sep = "`", mode = "a", index = False)

if __name__ == "__main__":
    # Read df from article list
    df = read_from_csv("raw_partner_headlines.csv")
    symbol_list = [
        "A",
        "META",
        "APPL",
        "GOOG",
        "ARM",
        "NVDA"
    ]
    
    
    for symbol in symbol_list:
        cur_df = df.loc[df["stock"] == symbol]
        cur_df["article_content"] = ""
        for index, row in cur_df.iterrows():
            cur_url = row["url"]
            cur_df.loc[index, "article_content"] = fetch_article_content(cur_url)
            time.sleep(1)
        write_to_local_csv(symbol + " - past content.csv", cur_df)
        print(cur_df)
        
        
    

