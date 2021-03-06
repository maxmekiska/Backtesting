import pandas as pd
import pandas_datareader as web
import numpy as np
import matplotlib.pyplot as plt

class Data():
    def __init__(self, ticker, start, end, ratio):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.ratio = ratio

    def original_data(self):
        stock = web.get_data_yahoo(self.ticker, start = self.start, end = self.end)
        return stock

    def load_data(self):
        stock = web.get_data_yahoo(self.ticker, start = self.start, end = self.end)

        price = stock["Adj Close"]

        d_returns = price.pct_change()
        d_returns = d_returns.to_frame()

        # preparation for prophet intake
        d_returns["ds"] = d_returns.index # create ds column from index
        d_returns["y"] = d_returns["Adj Close"] # create y column from adj close price
        d_returns.drop('Adj Close', axis=1, inplace=True) # drop original adj close price column
        d_returns = d_returns.reset_index(drop=True)
        d_returns = d_returns.set_index('ds')
        self.d_returns = d_returns

        self.all_returns = d_returns
        row_len = d_returns.shape[0]
        cut_off = round(self.ratio * row_len)
        self.period_forecast = row_len - cut_off

        train = d_returns['y'][0:cut_off]
        train = train.to_frame()
        train.insert(0, 'ds', train.index)
        train = train.reset_index(drop=True)

        return train

    def get_periods(self):
        return self.period_forecast

    def get_all_returns(self):
        all_returns = self.all_returns.reset_index(drop=True)
        return all_returns
    
    def get_prepared_data(self):
        d_returns = self.d_returns
        d_returns.insert(0, 'ds', d_returns.index)
        d_returns = d_returns.reset_index(drop=True)
        return d_returns
