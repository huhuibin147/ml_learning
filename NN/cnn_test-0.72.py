# -*- coding: utf-8 -*-
#################
#使用ckpt_cnn模型  以及去光影0.8得到72正确率的代码
#cnn第一层用的7*7卷积
#  0   18
#  1   128
#  3   3
#  4   78
#  6   135
#  7   216
#  8   75
#  9   41
#  2和5全正确
##################

import tensorflow as tf
#from tensorflow.examples.tutorials.mnist import input_data
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

import os
os.chdir("D:/machinelearning/codes/ml_learning/NN/")
os.getcwd()

#MNIST_DATA_DIR = "D:/machinelearning/MNIST/MNIST_data/"

#mnist = input_data.read_data_sets(MNIST_DATA_DIR, one_hot=True)


#sess = tf.InteractiveSession()

tf.reset_default_graph()


def init_weight(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)

def init_bias(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)

def conv2d(x, W):
    # SAME算法 new_height = new_width = W / S （结果向上取整）
    return tf.nn.conv2d(x, W, strides=[1,1,1,1], padding='SAME')

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1,2,2,1], strides=[1,2,2,1], padding='SAME')


x = tf.placeholder(tf.float32, [None, 784])
x_image = tf.reshape(x, [-1,28,28,1])

w_conv1 = init_weight([7,7,1,32])
b_conv1 = init_bias([32])

h_conv1 = tf.nn.relu(conv2d(x_image, w_conv1)+b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

# 第一层设置的32个核
w_conv2 = init_weight([5,5,32,64])
b_conv2 = init_bias([64])

h_conv2 = tf.nn.relu(conv2d(h_pool1, w_conv2)+b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

w_fc1 = init_weight([7*7*64, 1024])
b_fc1 = init_bias([1024])

h_pool2_flag = tf.reshape(h_pool2, [-1, 7*7*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flag, w_fc1)+b_fc1)

keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

w_fc2 = init_weight([1024, 10])
b_fc2 = init_bias([10])

y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, w_fc2)+b_fc2)
#y_ = tf.placeholder(tf.float32, [None, 10])


#cross_entropy = -tf.reduce_mean(y_*tf.log(y_conv))
#optimizer = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
#
#
#correct_prediction = tf.equal(tf.arg_max(y_conv,1), tf.arg_max(y_,1))
#accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

#sess.run(tf.global_variables_initializer())

#epoches = 15
#batch_size = 512
#n_batch = mnist.train.num_examples // batch_size
#
#
#init = tf.global_variables_initializer()
#saver = tf.train.Saver()

#with tf.Session() as sess:
#    sess.run(init)
#    print('init suc...')
#    for i in range(epoches):
#        for batch in range(n_batch):
#            print('train batch:', batch)
#            batch_xs, batch_ys = mnist.train.next_batch(batch_size)
#            optimizer.run(feed_dict={x:batch_xs,y_:batch_ys,keep_prob:0.5})
#        if i % 1 == 0:
#            train_accuacy = accuracy.eval(feed_dict={x:mnist.test.images,
#                                          y_:mnist.test.labels,keep_prob:1.0})
#            print("epoch:%s,acc:%s"%(i, train_accuacy))
#    saver.save(sess, './ckpt_cnn/cnn_mnist.ckpt')

#    print("test accuracy %g"%(accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0})))


def show_img(image, label=''):
    image_reshape = image.reshape(28,28)
    img_0 = Image.fromarray(image_reshape*255)
    if label:
        print('label:%s' % np.argmax(label))
    plt.imshow(img_0)

#def prediction(sess, n=0):
#    test_img = mnist.test.images[n]
#    test_label = mnist.test.labels[n]
#    show_img(test_img, test_label)
#    y_r = sess.run(y_conv, feed_dict={x: [test_img], keep_prob: 1.0})
#    print('prediction:%s' % (np.argmax(y_r,1)[0]))

def prediction2(sess, im_arr):
#    show_img(im_arr)
    y_r = sess.run(y_conv, feed_dict={x: im_arr, keep_prob: 1.0})
    r = np.argmax(y_r,1)[0]
#    print('y_r:%s' % y_r)
#    print('prediction:%s' % r)
    return r

    
    
#mnist.test.images[344]

#show_img(mnist.train.images[7])

saver = tf.train.Saver()

#with tf.Session() as sess: 
##    model = tf.train.latest_checkpoint('./ckpt_cnn')
##    saver.restore(sess, model)
#    saver.restore(sess, './ckpt_cnn/cnn_mnist.ckpt')
##    prediction2(sess, mnist.train.images[7].reshape(1,784))
#    
##    ns = ['l1c1','l1c2','l2c1','l2c2','l3c1','l3c2','l3c3',
##              'l3c4','l3c5','l3c6']
##    ns = ['pls168','pls239','pls315','plw168','plw239','plw315',
##          'plw387','plw461']
#    f = 2
#    s = 10
#    ns = ['%s.%s' % (f, i+s) for i in range(20)]
#    plt.figure(figsize=(10,7))
#    for i, n in enumerate(ns):
#        image = Image.open('./numdata/data/%s.jpg' % n)
##        image = Image.open('./cv/test/%s.jpg' % n)
#        image_arr = np.array(image.resize((28,28)))
#        #image_arr.shape
#        #image_arr / 255
#        im_arr = image_arr.reshape((1,784)) / 255
#        im_arr[im_arr<0.8] = 0
#        
#        plt.subplot(4,5,i+1)
#        image_reshape = im_arr.reshape(28,28)
#        img_0 = Image.fromarray(image_reshape*255)
#        plt.xticks([])
#        plt.yticks([])
#        plt.grid(False)
#        plt.imshow(img_0)
#        r = prediction2(sess, im_arr)
#        plt.xlabel('%s(%s)' % (r, int(np.sum(im_arr))))
#    plt.show()
        

data_dir = 'D:/machinelearning/codes/ml_learning/NN/numdata/data/'
files = os.listdir(data_dir)

cnt = 0
errors = []
with tf.Session() as sess: 
    saver.restore(sess, './ckpt_cnn/cnn_mnist.ckpt')
    
    
    ns = files
    for i, n in enumerate(ns):
        image = Image.open('./numdata/data/%s' % n)
        image_arr = np.array(image.resize((28,28)))
        #image_arr.shape
        #image_arr / 255
        im_arr = image_arr.reshape((1,784)) / 255
        im_arr[im_arr<0.8] = 0
        
        r = prediction2(sess, im_arr)
        if int(r) == int(n[0]):
            cnt += 1
        else:
            errors.append(n)
    p = cnt / len(files)
    print('正确率:', p)
    print('错误数:', len(errors))
        
        