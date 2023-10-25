import tensorflow as tf
import numpy as np

def w_variable(shape):
    # 随机初始化权重
    initial = tf.truncated_normal(shape,stddev= 0.1)
    return tf.Variable(initial)

def b_variable(shape):
    initial = tf.constant(0.1,shape=shape)
    return tf.Variable(initial)

#卷积运算
def conv2d(x,w):
    return tf.nn.conv2d(x,w,[1,1,1,1],'SAME')

# 2x2 最大池化
def max_pool_2x2(x):
    return tf.nn.max_pool(x,[1,2,2,1],[1,2,2,1],'SAME')

#卷积层
def conv_layer(input,shape):
    w=w_variable(shape)
    b=b_variable([shape[3]])
    return tf.nn.relu(conv2d(input,w)+b)

#全连接层
def full_layer(input,size):
    in_size = int(input.get_shape()[1])
    w=w_variable([in_size,size])
    b=b_variable([size])
    return tf.matmul(input,w)+b


x=tf.placeholder(tf.float32,shape=[None,784])
y=tf.placeholder(tf.float32,shape=[None,10])

x_image = tf.reshape(x,[-1,28,28,1])

conv1 = conv_layer(x_image,shape=[5,5,1,32])
conv1_pool = max_pool_2x2(conv1)

conv2 = conv_layer(conv1_pool,shape=[5,5,32,64])
conv2_pool = max_pool_2x2(conv2)

#全连接层 1
conv2_flat = tf.reshape(conv2_pool,[-1,7*7*64])
full_1 = tf.nn.relu(full_layer(conv2_flat,1024))

#随即丢弃优化
keep_prob = tf.placeholder(tf.float32)
full1_drop = tf.nn.dropout(full_1,keep_prob)

#全连接层 2
y_conv = full_layer(full1_drop,10)

#训练,使用softmax交叉熵
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=y_conv,labels=y_true))
train_step = tf.train.AdadeltaOptimizer(1e-4).minimize(cross_entropy)
