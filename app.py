from flask import Flask, render_template, request
from patterns import patterns
import ccxt
import sys
import pandas as pd
import os
import talib
import csv

app = Flask(__name__)
exchange = ccxt.binance()

@app.route('/')
def index():
    current_pattern = request.args.get('pattern', None)
    tokens = {}

    with open('data/dataset.csv') as f:
        headers = next(f) 
        for  row in csv.reader(f):
            tokens[row[0]] = {'symbol': row[1]}
    
    print(tokens)




    # print(pattern)
    if(current_pattern):
        datafiles = os.listdir('data/candledata/4h')
        for filename in datafiles:
            # print(filename)
            df = pd.read_csv('data/candledata/4h/{}'.format(filename))
            # print(df)
            pattern_function = getattr(talib, current_pattern)
            symbol = filename.split('.')[0]
            print(symbol)
            result = pattern_function(df["open"], df["high"], df["low"], df["close"])
            # print(result)
            lastResult = result.tail(1).values[0]
            # print(lastResult)
            if(lastResult > 0 ):
                tokens[symbol][current_pattern] = 'Bullish'
            elif(lastResult<0):
                tokens[symbol][current_pattern] = 'Bearish'
            else:
                tokens[symbol][current_pattern] = None

    print(tokens)
    return render_template('index.html', patterns=patterns, tokens=tokens, current_pattern=current_pattern)

@app.route('/snapshot')
def snapshot():
    with open('data/dataset.csv') as f:
        symbols = f.read().splitlines()
        del symbols[0]
        print(symbols)
        for symbol in symbols:
            splitSymbol = symbol.split(',')
            ticker = splitSymbol[1] +"/"+splitSymbol[2]
            try:
                bars = exchange.fetch_ohlcv(ticker, timeframe='4h', limit=1000)
                # print(ticker)
                df = pd.DataFrame(bars ,columns=['time', 'open', 'high','low' ,'close', 'volume'])
                df['time'] = pd.to_datetime(df['time'], unit='ms')
                df.set_index('time' , inplace=True, drop=True )
                df.to_csv('data/candledata/4h/{}.csv'.format(splitSymbol[0]))
                # print(df)
            except:
                print("Symbol error" , ticker)
                print("Oops!", sys.exc_info()[0], "occurred.")
                continue
            # print(ticker)
        return "done"

