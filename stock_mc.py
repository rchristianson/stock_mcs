import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf

import stock_strats as strats

# gets the closing prices for all stocks from start_date to end_date
def get_prices(stocks, start_date, end_date):
	prices = yf.download(stocks, start_date, end_date)
	prices_close = prices['Close']

	return prices_close

def buy_stock(hist_stock_df, new_day, strat):
	decision = strat(hist_stock_df)
	profit = 0
	for stock, weight in decision.items():
		profit += weight * (hist_stock_df[stock].iloc[-1] - new_day[stock])
	return(pd.Series(profit, index = new_day.index))

def single_mc(stock_prices, mc_reps, strat):
	stock_mcs = pd.DataFrame(index = stock_prices.index[1:], columns = range(mc_reps))

	for i in range(0, mc_reps):
		profits = [buy_stock(stock_prices[0:j], stock_prices[j:(j+1)], strat) for j in range(1, stock_prices.shape[0])]
		stock_mcs[i] = pd.concat(profits)
	
	return(stock_mcs)

# set parameters about the stocks and get closing prices
end_date = dt.datetime.now()
start_date = end_date - dt.timedelta(days=100)
stocks = ['SPY', 'AAPL', 'MSFT']
stock_prices = get_prices(stocks, start_date, end_date)

mc_reps = 100

stock_mcs_rand = single_mc(stock_prices, mc_reps, strats.rand_strat)
stock_mcs_equal = single_mc(stock_prices, mc_reps, strats.equal_strat)

stock_means_rand = stock_mcs_rand.mean(axis = 1)
stock_means_equal = stock_mcs_equal.mean(axis = 1)

stock_means = pd.concat([stock_means_rand, stock_means_equal], axis = 1)

plt.plot(stock_means)
plt.show()
