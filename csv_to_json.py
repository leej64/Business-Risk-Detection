import pandas as pd
import json

#df1 = pd.read_csv("newsdata/processedNews.csv", sep = "`")
df1 = pd.read_csv("stockdata/tradeData - 2018-01-01 - 2018-12-31.csv", sep = "`")



df = df1[df1["Symbol"] == "AMZN"]
print(df)

df.to_json("stock_amzn_2018.json", orient = "index")



