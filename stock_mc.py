import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import yfinance as yf
import importlib
import random
import warnings

strats = importlib.import_module('stock_strats')
strats_names = [name for name in dir(strats) if callable(getattr(strats, name))]
strats_short_names = [name[:-6] for name in strats_names]

# gets the closing prices for all stocks from start_date to end_date
def get_prices(stocks, start_date, end_date):
	prices = yf.download(stocks, start_date, end_date)
	prices_close = prices['Close']

	return prices_close

def buy_stock(hist_stock_df, new_day, strat, portfolio_start):
	decision = strat(hist_stock_df)
	portfolio_value = 0
	for stock, weight in decision.items():
		portfolio_value += portfolio_start * weight * (new_day[stock] / hist_stock_df[stock].iloc[-1])
	return(pd.Series(portfolio_value, index = new_day.index))

def single_mc(stock_prices, strat, portfolio_start):
	portfolio_values = pd.Series(portfolio_start, index = [stock_prices.index[0]])
	for i in range(1, stock_prices.shape[0]):
		temp_value = buy_stock(stock_prices.iloc[0:i, :], stock_prices.iloc[i:(i+1), :], strat, portfolio_values.iloc[-1])
		portfolio_values = pd.concat([portfolio_values, temp_value])
	
	return(portfolio_values)

def mult_mc(stock_prices, mc_reps, strat, portfolio_start, sim_len):
	if stock_prices.shape[0] <= sim_len:
		raise valueError("Need to have more dates than simulation length.")
	if stock_prices.shape[0] - sim_len < mc_reps:
		warnings.warn("Less unique starting days than mc_reps. Some dates will be repeated.")
	
	stock_mcs = pd.DataFrame(index = range(0, sim_len), columns = range(mc_reps))

	for i in range(0, mc_reps):
		sim_start = random.randint(0, stock_prices.shape[0] - sim_len)
		sim = single_mc(stock_prices.iloc[sim_start:(sim_start + sim_len), :], strat, portfolio_start)
		stock_mcs.iloc[:, i] = sim

	return(stock_mcs)

# set parameters about the stocks and get closing prices
end_date = dt.datetime.now()

# 252 trading days in a year
start_date = end_date - dt.timedelta(days = 252 * 2)

# random assortment of tech stocks
stocks = [
    'AAPL',   # Apple Inc.
    'GOOGL',  # Alphabet Inc. (Class A)
    'GOOG',   # Alphabet Inc. (Class C)
    'AMZN',   # Amazon.com Inc.
    'MSFT',   # Microsoft Corporation
    'META',   # Meta Platforms Inc.
    'TSLA',   # Tesla, Inc.
    'NVDA',   # NVIDIA Corporation
    'INTC',   # Intel Corporation
    'NFLX',   # Netflix, Inc.
    'ADBE',   # Adobe Inc.
    'CRM',    # Salesforce.com, Inc.
    'PYPL',   # PayPal Holdings, Inc.
    'CSCO',   # Cisco Systems, Inc.
    'IBM',    # IBM (International Business Machines Corporation)
    'SNAP',   # Snap Inc.
    'SQ',     # Square, Inc.
    'ZM',     # Zoom Video Communications, Inc.
    'UBER',   # Uber Technologies, Inc.
    'PINS'    # Pinterest, Inc.
]
stock_prices = get_prices(stocks, start_date, end_date)

mc_reps = 100
portfolio_start = 100000

profits = pd.DataFrame()
for strat_name in strats_short_names:
	test_strat = getattr(strats, f'{strat_name}_strat')
	strat_profit = mult_mc(stock_prices, mc_reps, test_strat, portfolio_start, 30)
	start_profit = profit.mean(axis = 1)
	profits = pd.concat([profits, strat_profit], axis = 1)

profits.columns = strats_short_names

plt.plot(profits)
plt.xlabel('Days')
plt.ylabel('Portfolio Value')
plt.title('Portfolio Value Over Time')
plt.legend(profits.columns)
plt.show()
