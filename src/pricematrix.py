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
