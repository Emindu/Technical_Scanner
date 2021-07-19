# starting python file, which is used to test the libraries

from os import close
import ccxt
import pandas as pd
import numpy  as np
import talib

exchange = ccxt.binance()
bars = exchange.fetch_ohlcv("YOYOBTC", timeframe='4h', limit=1000)

df = pd.DataFrame(bars ,columns=['time', 'open', 'high','low' ,'close', 'volume'])
df['time'] = pd.to_datetime(df['time'], unit='ms')
df.set_index('time' , inplace=True, drop=True )
print(df)
evening_stars = talib.CDLEVENINGSTAR(df["open"], df["high"], df["low"], df["close"])
engulfing = talib.CDLENGULFING(df["open"], df["high"], df["low"], df["close"])
threeInside = talib.CDL3INSIDE(df["open"], df["high"], df["low"], df["close"])
doji = talib.CDLDOJI(df["open"], df["high"], df["low"], df["close"])

df['evening_stars'] = evening_stars
df['Engulfing'] = engulfing
df['threeInside'] = threeInside
df['doji'] = doji

engulfing_data = df[df['Engulfing'] != 0]
print(engulfing_data)

evening_stars = df[df['evening_stars'] != 0]
print(evening_stars)

threeInside = df[df['threeInside'] != 0]
print(threeInside)

doji = df[df['doji'] != 0]
print(doji)
