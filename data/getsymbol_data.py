import sqlite3
import pandas as pd
from binance.client import Client
import csv

connection = sqlite3.connect('app.db');

client = Client()
#Get exchage information
exchangeInfo = (client.get_exchange_info())  # type =dict
symbols = exchangeInfo.get("symbols")  # liss
mylist = []
for symbol in symbols:


    print(symbol.get("quoteAsset"))
    if(symbol.get("quoteAsset") == 'BTC'):    #or symbol.get("quoteAsset") == 'ETH' or symbol.get("BNB")): #Filter only BTC, ETH, BNB based
        symbol_name = symbol.get("symbol")
        mylist.append([symbol.get("symbol"), symbol.get("baseAsset"),symbol.get("quoteAsset")])
 



        print(symbol)

print(mylist)
df = pd.DataFrame(mylist ,columns=['ticker', 'symbol', 'base_symbol'])
df.set_index('ticker' , inplace=True, drop=True )
df.to_csv("dataset.csv")
