import tensorflow as tf

#2D convolutional neural network which can mixed with fully-connected layers
class ConvNet:
    #input_shape [rows columns]
    def __init__(self, input_shape, layer_list):
        self.session = tf.InteractiveSession()
        self.input_shape = input_shape
        for layer in layer_list:
            assert isinstance(layer, Layer), "the item in the layer list is not layer"
        self.layer_list = layer_list
        self.input_tensor = tf.placeholder(tf.float32, shape=[None, self.input_shape[0]*self.input_shape[1]])
        self.output = self.forward_computation()

    #grenrate the operation, the forward computaion
    def forward_computation(self):
        forward_tensor = self.input_tensor
        if len(forward_tensor.get_shape())!=4:
            assert len(forward_tensor.get_shape())==2, 'the input data dimension is wrong'
            forward_tensor = tf.reshape(forward_tensor, [-1,self.input_shape[0],self.input_shape[1],1])
        for layer in self.layer_list:
            if isinstance(layer, FullyLayer):
                forward_tensor = tf.reshape(forward_tensor, [-1, layer.get_weight_shape()[0].value])
            forward_tensor = layer.process(forward_tensor)
        return forward_tensor

    #the next_batch: is a function which will return a feed_dict including a batch of trainning set,
    #   a 2d matrix ,each row is a input vector
    #loss_function: is a function which create the operation that producing loss value
    #logging: the fuction whcih may be called every 100 steps, the loss valus will be feed in
    def train(self, loss_function, steps ,next_batch , logging):
        loss_value = loss_function(self)
        train_step = tf.train.AdamOptimizer(1e-4).minimize(loss_value)
        self.session.run(tf.initialize_all_variables())
        for i in range(steps):
            batch = next_batch(self)
            train_step.run(batch)
            if i%100==0:
                logging(self, loss_value.eval(batch))
        print 'train has finished'

#the super class, representing a conv layer or fully-connected layer
class Layer:
    def __init__(self):
        pass

    #initialize the weight randomly
    def weight_variable(self,shape):
        initial = tf.truncated_normal(shape, stddev = 0.1)
        return tf.Variable(initial)

    #initialize the bias randomly
    def bias_variable(self,shape):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)

    #process the output from last layer and output it
    def process(self,x):
        pass


#the convolutional layer
class ConvLayer(Layer):
    # weight_shape[rows columns input_feature_number output_feature_number]
    # pooling_strides[1 rows columns 1]
    def __init__(self, weight_shape, pooling_strides, activation_func=tf.nn.relu):
        self.__weight=Layer.weight_variable(self,weight_shape)
        self.__bias=Layer.bias_variable(self,[weight_shape[3]])
        self.__pooling_strides = pooling_strides
        self.__activation_func = activation_func

    #convolute the x by W
    #x: is a 4d input tenser
    #W: is the weights
    def conv2d(self, x, W, strides=[1, 1, 1, 1]):
        return tf.nn.conv2d(x, W, strides, padding='SAME')

    #pooling the feature map, the knums and pooling strides depends on the  __pooling_strides member
    #x: is a 4d input tensor, the feature maps
    def pooling(self, x, pooling_type='MAX'):
        if pooling_type=='MAX':
            return tf.nn.max_pool(x, self.__pooling_strides, self.__pooling_strides, padding='SAME')

    def process(self,x):
        assert len(x.get_shape())==4, "the input shape dimension %s do not fit the requirements of the 2d convlayer"% len(x.get_shape())
        assert x.get_shape()[3]==self.__weight.get_shape()[2], "the input feature dimension %s do not fit the features of the 2d convlayer"% x.get_shape()[3]
        feature_map = self.__activation_func(self.conv2d(x,self.__weight)+self.__bias)
        return self.pooling(feature_map)


#the fully-connected layer
class FullyLayer(Layer):
    def __init__(self, weight_shape, activation_func=tf.nn.sigmoid):
        self.__weight=Layer.weight_variable(self,weight_shape)
        self.__bias=Layer.bias_variable(self,[weight_shape[1]])
        self.__activation_func=activation_func

    def get_weight_shape(self):
        return self.__weight.get_shape()

    def process(self, x):
        assert len(x.get_shape())==2, "the input shape dimension %s do not fit the requirements of the fully-connected layer"%len(x.get_shape())
        assert x.get_shape()[1]==self.__weight.get_shape()[0], "the input feature dimension %s do not fit the weight number of the fully-connected layer"%x.get_shape()[1]
        return self.__activation_func(tf.matmul(x, self.__weight) + self.__bias)
