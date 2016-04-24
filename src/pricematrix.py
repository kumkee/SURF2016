from coinlist import CoinList
import pandas as pd
from time import time


class PriceMatrix(CoinList):

    FIVE_MINUTES = 60*5
    FIFTEEN_MINUTES = FIVE_MINUTES * 3
    HALF_HOUR = FIFTEEN_MINUTES * 2
    HOUR = HALF_HOUR * 2
    TWO_HOUR = HOUR * 2
    FOUR_HOUR = HOUR * 4
    DAY = HOUR * 24

    def __init__(self, start = time() - DAY, end = time(), period = HALF_HOUR):
	super(PriceMatrix, self).__init__()
	self._start = start
	self._end = end
	self._period = period
	self.__coinFilter()

	it = iter(self._coins)
	coin = it.next()
	chart = self.__getChart(coin)
	self._chart = chart ######
	cols = [d['date'] for d in chart]
	self._pm = pd.DataFrame(index = self._coins, columns = cols)
	self.__fillPriceRow(coin, chart)

	print start, end, period


    def __fillPriceRow(self, coin, chart):
	self._pm.loc[coin] = [d['close'] for d in chart]


    def __getChart(self, coin):
	chart = self.polo.marketChart( \
			pair = self._df.loc[coin]['pair'], \
			start = self._start, \
			end = self._end, \
			period = self._period )
	return chart

    def __coinFilter(self):
        self._coins = self.topNVolume( n = len(self.allActiveCoins()) / 3).index

