import pandas as pd
import csv

def read_from_csv(filename):
    df = pd.read_csv(filename, sep = "`")
    return df

# Write dataframe to local csv
def write_to_local_csv(filename, df, has_header):
    df.to_csv(filename, sep = "`", mode = "w", index = False, header = has_header)

if __name__ == "__main__":
    file_name = "./newsdata/historicalNews.csv"
    columns = ["title", "link", "timestamp", "content", "publish_time", "related_tickers", "risk_type"]
    df = pd.read_excel('./newsdata/news.xlsx')
    df.columns = columns
    print(df)
    #write_to_local_csv(file_name, df, True)