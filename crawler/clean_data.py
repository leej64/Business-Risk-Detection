import pandas as pd
import csv

def read_from_csv(filename):
    df = pd.read_csv(filename, sep = "`")
    return df

if __name__ == "__main__":
    file_name = "./newsdata/historicalNews - 2024-02-11 03-56-14.csv"
    df = read_from_csv(file_name)
    print(df)