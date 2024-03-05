'''
Retrieves the historical data of given company and time range
and dump it into csv
'''

import pandas as pd
import yfinance as yf
import time
import json


def get_historical_data(company_symbol):
    # Start and end date of historical data
    start_date = "2018-01-01"
    end_date = "2018-12-31"
    tick = yf.Ticker(company_symbol)
    # Get historical data
    hist = tick.history(start = start_date, end = end_date)
    hist = hist.reset_index()

    data = hist[["Date", "Close"]]
    data["Date"] = data["Date"].dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    print(data)

    dict = data.to_dict("records")
    print(dict)
    with open("./" + company_symbol + ".json", "w") as outfile:
        json.dump(dict, outfile)
    return hist

get_historical_data("NVDA")
