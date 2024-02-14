'''
Retrieves the historical data of given company and time range
and dump it into csv
'''

import pandas as pd
import yfinance as yf
from sp500_symbols import sp500_symbols 
import time

# Write dataframe to local csv
def write_to_local_csv(filename, df, has_header):
    df.to_csv(filename, sep = "`", mode = "a", index = True, header = has_header)


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
    
    need_header = True

    for symbol in sp500_symbols:
        tick = yf.Ticker(symbol)
        # Get historical data
        hist = tick.history(start = start_date, end = end_date)
        hist["Symbol"] = symbol
        print(hist.columns)
        # Write to local csv files
        file_name = "./stockdata/tradeData - " + start_date + " - " + end_date + ".csv"
        # Write to local csv files
        write_to_local_csv(file_name, hist, need_header)
        time.sleep(1)
        if need_header == True:
            need_header = False

