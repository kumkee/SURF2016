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
YEAR = DAY * 365

CSV_DEFAULT = 'pm.csv'

COIN_REF = 'LTC'

class GlobalPriceMatrix(CoinList):

    def __init__(self, start = DAY, end = NOW, period = HALF_HOUR, csv = None, coin_filter = 0.2):
	super(GlobalPriceMatrix, self).__init__()
	self._coin_filter = coin_filter
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

	self.__checkperiod()

	coin = COIN_REF
	chart = self.getChart(coin, start = self._start, end = self._end)
	cols = [d['date'] for d in chart]
	self._pm = pd.DataFrame(index = self._coins, columns = cols).astype('float32')
	self.__fillPriceRow(coin, start = self._start, end = self._end)

	for c in self._coins:
	    if c == COIN_REF:
		continue
	    self.__fillPriceRow(c, start = self._start, end = self._end)


    def __fillPriceRow(self, coin, start, end):
	chart = self.getChart(coin=coin, start=start, end=end)
	for c in chart:
	    self._pm.at[coin, c['date']] = c['close']


    @property
    def pricedata(self):
	return self._pm


    @property
    def pricematrix(self):
	return self._pm.as_matrix()


    def getChart(self, coin, start, end):
	chart = self.polo.marketChart( \
			pair = self.allActiveCoins.at[coin, 'pair'], \
			start = start, \
			end = end, \
			period = self._period )
	return chart


    def __coinFilter(self):
	if(self._coin_filter):
            self._coins = self.topNVolume(
		n = int(len(self.allActiveCoins) * self._coin_filter)).index


    def to_csv(self, filepath = CSV_DEFAULT):
	#Save the database into csv file
	pm = self._pm.transpose()
	pm.index = pd.to_datetime(pm.index, unit = 's')
	pm.to_csv(filepath)


    def __getPriceFromFile(self, csv = CSV_DEFAULT):
	pm = pd.DataFrame.from_csv(csv).astype('float32')
	pm.index = pm.index.astype(np.int64)/10**9
	self._pm = pm.transpose()
	self._start = self._pm.columns[0]
	self._end = self._pm.columns[-1]
	self._period = self._pm.columns[1] - self._start


    def __checkperiod(self):
	if self._period == FIVE_MINUTES:
	    return
	elif self._period == FIFTEEN_MINUTES:
	    return
	elif self._period == HALF_HOUR:
	    return
	elif self._period == TWO_HOUR:
	    return
	elif self._period == FOUR_HOUR:
	    return
	elif self._period == DAY:
	    return
	else:
	    raise ValueError('peroid has to be 5min, 15min, 30min, 2hr, 4hr, or a day')

FIVE_MINUTES = 60*5
FIFTEEN_MINUTES = FIVE_MINUTES * 3
HALF_HOUR = FIFTEEN_MINUTES * 2
#HOUR = HALF_HOUR * 2
TWO_HOUR = HALF_HOUR * 4
FOUR_HOUR = HALF_HOUR * 8
DAY = HALF_HOUR * 48
