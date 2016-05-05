import globalpricematrix as gpm
import numpy as np


class PriceMatrices(gpm.GlobalPriceMatrix):

    def __init__(self, start = gpm.YEAR, end = gpm.NOW, period = gpm.HALF_HOUR, csv = None, coin_filter = 0.2, window_size = 30, train_portion = 0.7, validation_portion = 0.15, test_portion = 0.15):
	super(PriceMatrices, self).__init__(start, end, period, csv, coin_filter)
	self.__removeLastNaNs()
	self.__normalize_portions(train_portion, \
				  validation_portion, \
				  test_portion)
	self.__permutation(window_size)
	self._index_in_epoch = 0
	self._completed_epochs = 0


    def next_batch(self, batch_size):
	#based on: https://goo.gl/bv7hp7
	batch = []
	num_train_periods = len(self._perm)
	start = self._index_in_epoch
	self._index_in_epoch += batch_size

	if self._index_in_epoch > num_train_periods:
	    #complete one epoch, start new epoch
	    self._completed_epochs += 1
	    np.randow.shuffle(self._perm)
	    start = 0
	    self._index_in_epoch = batch_size

	end = self._index_in_epoch

	for i in xrange(start, end):
	     batch.append(self.getSubMatrix(self._perm[i]))

        return batch


    def getSubMatrix(ind):
	#TODO: normalized price submatrix
	return None


    def __permutation(self, window_size):
	self._window_size = window_size
	self._perm = self._train_ind[:-window_size]
	np.random.shuffle(self._perm)
	

    def __fillNaN(self):
	#refer to 'Working with missing data' on pandas doc
	#TODO
	pass


    def __removeLastNaNs(self):
	i = -1
	while( self.pricematrix.iloc[:, i].isnull().any() ):
	    i -= 1
	i += 1
	self._num_periods = self.pricematrix.shape[1] + i


    def __normalize_portions(self, train_portion, validation_portion, test_portion):
	if( test_portion <= 0 or \
		validation_portion <= 0 or \
		train_portion <=0):
	    raise ValueError('Portions must be positive')
	else:
	    s = float(train_portion + validation_portion + test_portion)
	    portions = np.array([train_portion, train_portion + validation_portion]) / s
	    portion_split = (portions * self._num_periods).astype(int)
	    indices = range(self._num_periods)
	    self._train_ind, self._val_ind, self._test_ind = np.split(indices, portion_split)
