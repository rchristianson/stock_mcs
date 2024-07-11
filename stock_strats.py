import pandas as pd
import numpy as np
import datetime as dt
import random
import sklearn.linear_model as lm

# randomly select 1 stock to buy
def random_single_strat(stock_df):
	rand_ind = random.randint(0, stock_df.shape[1] - 1)
	return({stock_df.columns[rand_ind]: 1})

# split equally between all
# on average, prices go up
def equal_distribution_strat(stock_df):
	equal_weight = 1 / len(stock_df.columns)
	return({stock: equal_weight for stock in stock_df.columns})

# buy the stock with the biggest gain yesterday
# winners keep winning
def best_yesterday_strat(stock_df):
	if stock_df.shape[0] == 1:
		# randomly select a stock if you only have 1 row
		rand_ind = random.randint(0, stock_df.shape[1] - 1)
		return({stock_df.columns[rand_ind]: 1})
	
	row_diff = stock_df.iloc[-2] - stock_df.iloc[-1]
	best_stock = row_diff.idxmax()
	return({best_stock: 1})

# buy the stock with the biggest loss yesterday
# losers bounce back
def worst_yesterday_strat(stock_df):
	if stock_df.shape[0] == 1:
		# randomly select a stock if you only have 1 row
		rand_ind = random.randint(0, stock_df.shape[1] - 1)
		return({stock_df.columns[rand_ind]: 1})
	
	row_diff = stock_df.iloc[-1] - stock_df.iloc[-2]
	best_stock = row_diff.idxmax()
	return({best_stock: 1})

# buy the stock with the highest volatility
def highest_volatility_strat(stock_df):
	if stock_df.shape[0] < 3:
		# randomly select a stock if you only have 1 row
		rand_ind = random.randint(0, stock_df.shape[1] - 1)
		return({stock_df.columns[rand_ind]: 1})
	
	stock_df_last = stock_df.iloc[:-1, :].values
	stock_df_first = stock_df.iloc[1:, :].values
	stock_returns = pd.DataFrame((stock_df_last - stock_df_first) / stock_df_first)
	
	volatility = stock_returns.std() * np.sqrt(252)
	volatility.index = stock_df.columns
	best_stock = volatility.idxmax()
	return({best_stock: 1})

# buy the stock with the lowest volatility
def lowest_volatility_strat(stock_df):
	if stock_df.shape[0] < 3:
		# randomly select a stock if you only have 1 row
		rand_ind = random.randint(0, stock_df.shape[1] - 1)
		return({stock_df.columns[rand_ind]: 1})
	
	stock_df_last = stock_df.iloc[:-1, :].values
	stock_df_first = stock_df.iloc[1:, :].values
	stock_returns = pd.DataFrame((stock_df_last - stock_df_first) / stock_df_first)
	
	volatility = stock_returns.std() * np.sqrt(252)
	volatility.index = stock_df.columns
	best_stock = volatility.idxmin()
	return({best_stock: 1})

# buy stock trending up
def lin_reg_strat(stock_df):
	if stock_df.shape[0] < 2:
		# randomly select a stock if you only have 1 row
		rand_ind = random.randint(0, stock_df.shape[1] - 1)
		return({stock_df.columns[rand_ind]: 1})
	
	X = np.arange(1, stock_df.shape[0] + 1).reshape(-1, 1)
	reg_results = pd.Series()
	for i in range(stock_df.shape[1]):
		Y = stock_df.iloc[:, i].values.reshape(-1, 1)

		model = lm.LinearRegression()
		model.fit(X, Y)

		reg_results[stock_df.columns[i]] = model.coef_[0][0]
	best_stock = reg_results.idxmax()
	return({best_stock: 1})


