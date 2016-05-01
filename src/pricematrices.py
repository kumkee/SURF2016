import globalpricematrix as gpm


class PriceMatrices(gpm.GlobalPriceMatrix):

    def __init__(self, start = gpm.YEAR, end = gpm.NOW, period = gpm.HALF_HOUR, csv = None, coin_filter = 0.2, window_size = 30):
	super(PriceMatrices, self).__init__(start, end, period, csv, coin_filter)


    def next_batch(self, batch_size):
	pass


    def __fillNaN(self):
	#refer to 'Working with missing data' on pandas doc
	pass



