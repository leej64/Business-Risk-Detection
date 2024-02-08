import pandas as pd
import yfinance as yf


if __name__ == "__main__":
    symbol_list = [
        "AMZN",
        "META",
        "APPL",
        "GOOG",
        "ARM",
        "NVDA"
    ]
    for symbol in symbol_list:
        tick = yf.Ticker(symbol)
        hist = tick.history(period="1mo")
        print(hist)
        print(tick.news)
        break
