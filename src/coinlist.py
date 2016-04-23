from poloniex import Poloniex
#import numpy as np
import pandas as pd


class CoinList(object):

    def __init__(self):
        self.polo = Poloniex()
        vol = self.polo.marketVolume()
        pairs = []
        coins = []
        volumes = []

        for k, v in vol.iteritems():
            if k.startswith("BTC_") or k.endswith("_BTC"):
        	pairs.append(k)
                for c, val in v.iteritems():
                    if c != 'BTC':
    		        coins.append(c) 
	            else:
		        volumes.append(float(val))

        self._df = pd.DataFrame({'coin': coins, 'pair': pairs, 'volume': volumes})
	self._df = self._df.set_index('coin')

    def allActiveCoins(self):
        return self._df

    def allCoins(self):
	return self.polo.marketStatus().keys()	

    def topNVolume(self, n = 5, order = False, minVolume = 0):
	if minVolume == 0:
	    r = self._df.sort_values(by='volume', ascending=False)[:n]
            if order:
		return r
            else:
		return r.sort_index()
	else:
	    return self._df[self._df.volume >= minVolume]

    #def volumeAtLeast(self, minvolume = 100):
	#return self._df[self._df.volume >= minvolume]
