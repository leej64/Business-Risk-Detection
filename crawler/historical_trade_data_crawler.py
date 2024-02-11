'''
Retrieves the historical data of given company and time range
and dump it into csv
'''

import pandas as pd
import yfinance as yf
from sp500_symbols import sp500_symbols 
import time

def write_to_local_csv(filename, df):
    df.to_csv(filename, mode = "w", index = True)

if __name__ == "__main__":
    # List of companies to get info for
    symbol_list = [
        "AMZN",
        "META",
        "APPL",
        "GOOG",
        "ARM",
        "NVDA"
    ]

    # Start and end date of historical data
    start_date = "2018-01-01"
    end_date = "2018-12-31"

    for symbol in sp500_symbols:
        tick = yf.Ticker(symbol)
        # Get historical data
        hist = tick.history(start = start_date, end = end_date)
        #print(hist.columns)
        # Write to local csv files
        file_name = symbol + " - " + start_date + " - " + end_date + ".csv"
        write_to_local_csv("./stockdata/" + file_name, hist)
        time.sleep(1)

