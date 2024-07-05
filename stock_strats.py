import pandas as pd
import numpy as np
import datetime as dt
import random

# randomly select 1 stock to buy
def rand_strat(stock_df):
	rand_ind = random.randint(0, stock_df.shape[1] - 1)
	return({stock_df.columns[rand_ind]: 1})

# split equally between all
def equal_strat(stock_df):
	equal_weight = 1 / len(stock_df.columns)
	return({stock: equal_weight for stock in stock_df.columns})