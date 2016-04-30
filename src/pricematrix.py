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

CSV_DEFAULT = 'pm.csv'


class PriceMatrix(CoinList):

    def __init__(self, start = DAY, end = NOW, period = HALF_HOUR, csv = None):
	super(PriceMatrix, self).__init__()
	if csv:
	    self.__getPriceFromFile(csv)
	else:
	    self.__getPriceFromExchange(start, end, period)


    def __getPriceFromExchange(self, start, end, period):
	t = time()
	self._start = t - start
	self._end = t - end + 10*period
	self._period = period
	self.__coinFilter()

	coin = 'LTC'
	chart = self.getChart(coin, start = self._start, end = self._end)
	cols = [d['date'] for d in chart]
	self._pm = pd.DataFrame(index = self._coins, columns = cols)
	self.__fillPriceRow(coin, start = self._start, end = self._end)

	for c in self._coins:
	    if c == 'LTC':
		continue
	    self.__fillPriceRow(c, start = self._start, end = self._end)


    def __fillPriceRow(self, coin, start, end):
	chart = self.getChart(coin=coin, start=start, end=end)
	for c in chart:
	    self._pm.loc[coin, c['date']] = c['close']


    def getChart(self, coin, start, end):
	chart = self.polo.marketChart( \
			pair = self._df.loc[coin]['pair'], \
			start = start, \
			end = end, \
			period = self._period )
	return chart


    def __coinFilter(self):
        self._coins = self.topNVolume( n = len(self.allActiveCoins()) / 5).index


    def to_csv(self, filepath = CSV_DEFAULT):
	#Save the database into csv file
	pm = self._pm.transpose()
	pm.index = pd.to_datetime(pm.index, unit = 's')
	pm.to_csv(filepath)


    def __getPriceFromFile(self, csv = CSV_DEFAULT):
	pm = pd.DataFrame.from_csv(csv)
	pm.index = pm.index.astype(np.int64)/10**9
	self._pm = pm.transpose()
	self._start = self._pm.columns[0]
	self._end = self._pm.columns[-1]
	self._period = self._pm.columns[1] - self._start
