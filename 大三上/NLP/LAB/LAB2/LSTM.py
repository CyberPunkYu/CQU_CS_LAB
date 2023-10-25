import tensorflow as tf
import numpy as np
import tensorflow.contrib.rnn
from tensorflow.python.ops.rnn import dynamic_rnn
import random

#时间步骤，60天为周期
time_steps = 60
#每个时间序列中向量的维度，对应[开，收，最高，最低，换手，总手，金额，总值，流值，市盈]
element_size = 10
#隐藏层向量大小
hidden_layer_size = 128

num_classes = 1

#LSTM核心部分
with tf.variable_scope("lstm"):
    input = tf.placeholder(tf.float32, [None, time_steps, element_size])
    lstm_cell = tf.nn.rnn_cell.BasicLSTMCell(hidden_layer_size,forget_bias=1.0)
    outputs , states=dynamic_rnn(lstm_cell,input,dtype= tf.float32)
    #states大小为time_steps * hidden_layer_size

with tf.name_scope("line"):
    weight = tf.Variable(tf.truncated_normal([hidden_layer_size,num_classes],mean=0,stddev=.01),name='weight')
    bias = tf.Variable(tf.truncated_normal([num_classes], mean=0, stddev=.01), name='bias')
    #最后一个有效向量 1 * hidd_layer_size
    finial_output = tf.matmul(states[-1],weight) + bias
    #交叉熵
    true_labels = tf.placeholder(tf.float32,None)
    softmax = tf.nn.softmax_cross_entropy_with_logits(logits= finial_output,labels= true_labels)
    cross_entropy = tf.reduce_mean(softmax)
    #训练
    train = tf.train.RMSPropOptimizer(0.001,0.9).minimize(cross_entropy)

#生成测试数据
x = [[[0 for i in range(10)] for j in range(60)]for k in range(10)]
y = [i for i in range(10)]
for i in range(10):
    for j in range(60):
        for k in range(10):
            x[i][j][k]=random.random()*100
    y[i] = random.randint(0,1)


with tf.Session()as sess:
    sess.run(tf.global_variables_initializer())
    #训练次数
    for i in range(10):
        sess.run(train,feed_dict={input:np.array(x),true_labels:np.array(y)})

    #测试用
    print(sess.run([weight,bias]))