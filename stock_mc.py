import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf
	
# gets the closing prices for all stocks from start_date to end_date
def stock_mc(stocks, start_date, end_date):
	prices = yf.download(stocks, start_date, end_date)
	prices_close = prices['Close']

	return prices_close

end_date = dt.datetime.now()
start_date = end_date - dt.timedelta(days=100)

stocks = ['SPY', 'AAPL', 'MSFT']

test = stock_mc(stocks, start_date, end_date)

print(test)