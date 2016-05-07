import globalpricematrix as gpm
import numpy as np

FAKE_DEFLATION_FACTOR = 1.5

MIN_NUM_PERIOD = 3


class PriceMatrices(gpm.GlobalPriceMatrix):

    def __init__(self, start = gpm.YEAR, end = gpm.NOW, period = gpm.HALF_HOUR, csv = None, coin_filter = 0.2, \
			 window_size = 30, train_portion = 0.7, validation_portion = 0.15, test_portion = 0.15):
	assert window_size >= MIN_NUM_PERIOD
	super(PriceMatrices, self).__init__(start, end, period, csv, coin_filter)
	self._window_size = window_size
	self.__removeLastNaNs()
	self.__divide_data(train_portion, \
				  validation_portion, \
				  test_portion)
	self.__permutation()
	self.__make_fake_prices()
	self._index_in_epoch = 0
	self._completed_epochs = 0


    @property
    def index_in_epoch(self):
	return self._index_in_epoch


    @property
    def completed_epochs(self):
	return self._completed_epochs


    @property
    def num_train_samples(self):
	return self._num_train_samples


    @property
    def num_validation_samples(self):
	return self._num_validation_samples


    @property
    def validation_indices(self):
	return self._val_ind[:-self._window_size]


    @property
    def test_indices(self):
	return self._test_ind[:-self._window_size]


    @property
    def num_test_samples(self):
	return self._num_test_samples


    def __make_fake_prices(self):
	self._fake_prices = np.array( \
				[ FAKE_DEFLATION_FACTOR**(self._window_size - i - 1) \
				for i in xrange(self._window_size + 1) ] )


    def next_batch(self, batch_size = 1):
	#based on: https://goo.gl/bv7hp7
	batch = []
	start = self._index_in_epoch
	self._index_in_epoch += batch_size

	if self._index_in_epoch > self._num_train_samples:
	    #complete one epoch, start new epoch
	    self._completed_epochs += 1
	    np.random.shuffle(self._perm)
	    start = 0
	    self._index_in_epoch = batch_size
	    assert batch_size <= self._num_train_samples

	end = self._index_in_epoch

	for i in xrange(start, end):
	     batch.append(self.getSubMatrix(self._perm[i]))

        return np.array(batch)


    def getSubMatrix(self, ind):
	mc = self.pricematrix[:, ind:ind+self._window_size+1]
	m = mc.copy() 
	self.__fillNaN_pricenorm(m)
	return m


    def __permutation(self):
	self._perm = \
		self._train_ind[:-self._window_size]
	np.random.shuffle(self._perm)
	

    def __price_normalization(self, m, i):
	row = m[i]
	m[i] = row / row[-2]


    def __fillNaN_pricenorm(self, m):
	#refer to 'Working with missing data' on pandas doc
	for i in xrange(m.shape[0]):
	    row = m[i,:-1]
	    isnull = np.isnan(row)

	    #check if there are any NaN's
	    if(isnull.any()):
		#check number of valid prices in the row
		if(sum(~isnull) < MIN_NUM_PERIOD):
		    m[i] = self._fake_prices
		else:
		    nulls = np.where(isnull)[0]
		    not_nulls = np.where(~isnull)[0]
		    assert (nulls < not_nulls[0]).all()
		    m[i,nulls] = row[not_nulls[0]]

		    self.__price_normalization(m, i)
	    else:
		self.__price_normalization(m, i)


    def __removeLastNaNs(self):
	i = -1
	while( np.isnan(self.pricematrix[:, i]).any() ):
	    i -= 1
	i += 1
	self._num_periods = self.pricematrix.shape[1] + i


    def __divide_data(self, train_portion, validation_portion, test_portion):
	if( test_portion <= 0 or \
		validation_portion <= 0 or \
		train_portion <=0):
	    raise ValueError('Portions must be positive')
	else:
	    s = float(train_portion + validation_portion + test_portion)
	    portions = np.array([train_portion, train_portion + validation_portion]) / s
	    portion_split = (portions * self._num_periods).astype(int)
	    indices = np.arange(self._num_periods)
	    self._train_ind, self._val_ind, self._test_ind = np.split(indices, portion_split)

	    self._num_train_samples = self._val_ind[0] \
					 - self._window_size
	    self._num_validation_samples = \
		self._test_ind[0] - self._num_train_samples \
					 - self._window_size
	    self._num_test_samples = \
		self._num_periods\
		 - self._num_train_samples \
		 - self._num_validation_samples \
		 - self._window_size
