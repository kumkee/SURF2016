import unittest
import network as nw
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data', one_hot = True)

def logging(net, loss_value):
    print 'trainning loss is %s'% loss_value

def next_batch(net):
    batch = mnist.train.next_batch(50)
    return {net.input_tensor:batch[0], net.y_:batch[1]}

def loss_function(net):
    return tf.reduce_mean(-tf.reduce_sum(net.y_ * tf.log(net.output), reduction_indices=[1]))

class TestDict(unittest.TestCase):
    def test_using_MNIST(self):
        net1 = nw.ConvNet(input_shape = [28,28], layer_list = [\
                      nw.ConvLayer(weight_shape=[5, 5, 1, 32], pooling_strides=[1, 2, 2, 1]),\
                      nw.ConvLayer(weight_shape=[5, 5, 32, 64], pooling_strides=[1, 2, 2, 1]),\
                      nw.FullyLayer(weight_shape=[7*7*64, 1024]),\
                      nw.FullyLayer(weight_shape=[1024, 10])\
                      ])

        #add input dynamically
        net1.y_ = tf.placeholder(tf.float32, shape=[None, 10])
        net1.train(steps = 1000,\
                loss_function = loss_function,\
                logging = logging,\
                next_batch = next_batch)
