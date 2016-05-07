# coding: utf-8
import tensorflow as tf

window_size = 5

a = tf.placeholder(tf.float32, shape=[1])

A = tf.tile(1-a, [window_size])

p = tf.linspace(0., window_size-1., window_size)

Sa = tf.mul(a, tf.pow(A, p))

with tf.Session() as sess:
    a0 = [0.5]
    print sess.run(A, feed_dict={a: a0})
    print sess.run(Sa, feed_dict={a: a0})
