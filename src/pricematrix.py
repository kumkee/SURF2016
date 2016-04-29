from coinlist import CoinList
import pandas as pd
from time import time
from time import sleep
import numpy as np

NOW = 0
FIVE_MINUTES = 60*5
FIFTEEN_MINUTES = FIVE_MINUTES * 3
HALF_HOUR = FIFTEEN_MINUTES * 2
HOUR = HALF_HOUR * 2
TWO_HOUR = HOUR * 2
FOUR_HOUR = HOUR * 4
DAY = HOUR * 24


class PriceMatrix(CoinList):

    def __init__(self, start = DAY, end = NOW, period = HALF_HOUR):
	super(PriceMatrix, self).__init__()
	t = time()
	self._start = t - start
	self._end = t - end + 10*period
	self._period = period
	self.__coinFilter()

	coin = 'LTC'#iter_coin.next()
	chart = self.getChart(coin, start = self._start, end = self._end)
	cols = [d['date'] for d in chart]
	self._pm = pd.DataFrame(index = self._coins, columns = cols)
	self.__fillPriceRow(coin, start = self._start, end = self._end)

	for c in self._coins:
	    if c == 'LTC':
		continue
	    self.__fillPriceRow(c, start = self._start, end = self._end)

	#self.__completeLastColumns()

	print start, end, period


    def __fillPriceRow(self, coin, start, end):
	chart = self.getChart(coin=coin, start=start, end=end)
	for c in chart:
	    self._pm.loc[coin, c['date']] = c['close']


    '''
    def completeLastColumns(self):
	for c in range(-1, -6, -1):
	    b = self.anyNaNinColumn(c) 
	    if not b.any():
		break
	    coins = self._df.index[b]
	    i = c
	t0 = self._pm.columns[i]
	t1 = self._pm.columns[-1]
	for coin in coins:
	    self.__fillPriceRow(coin=coin, start=t0, end=t1)


    def anyNaNinColumn(self, c):
	return self._pm.iloc[:, -c].isnull()
    '''


    def getChart(self, coin, start, end):
	chart = self.polo.marketChart( \
			pair = self._df.loc[coin]['pair'], \
			start = start, \
			end = end, \
			period = self._period )
	return chart

    def __coinFilter(self):
        self._coins = self.topNVolume( n = len(self.allActiveCoins()) / 5).index

