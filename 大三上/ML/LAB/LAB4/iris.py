#---------------------------------模型引入---------------------------------
import csv
import os
import time
import numpy as np
from easydict import EasyDict as edict
from matplotlib import pyplot as plt
import mindspore
from mindspore import nn
from mindspore import context
from mindspore import dataset
from mindspore.train.callback import TimeMonitor, LossMonitor
from mindspore import Tensor
from mindspore.train import Model
from mindspore.train.callback import ModelCheckpoint, CheckpointConfig
# 设定运行模式为静态图模式，并且运行设备为昇腾芯片
context.set_context(mode=context.GRAPH_MODE, device_target="Ascend") 

#---------------------------------变量定义---------------------------------
cfg = edict({
    'data_size': 150,
    'train_size': 120, #训练集大小
    'test_size': 30 , #测试集大小
    'feature_number': 4, #输入特征数
    'num_class': 3, #分类类别
    'batch_size': 30, #批次大小
    'data_dir': 'iris.data', # 数据集路径
    'save_checkpoint_steps': 5, #多少步保存一次模型
    'keep_checkpoint_max': 1, #最多保存多少个模型
    'out_dir_no_opt': './model_iris/no_opt', #保存模型路径，无优化器模型
    'out_dir_sgd': './model_iris/sgd', #保存模型路径,SGD优化器模型
    'out_dir_momentum': './model_iris/momentum', #保存模型路径，momentum模型
    'out_dir_adam': './model_iris/adam', #保存模型路径，adam优化器模型
    'output_prefix': "checkpoint_fashion_forward" #保存模型文件名
})

#---------------------------------数据读取---------------------------------
print(cfg.data_dir)
f = open('iris.data', mode = 'r', encoding = 'utf-8-sig')
for i in f.readlines():
    print(i)
f.close()
#鸢尾花数据集，本数据集共有150个带标签的数据
with open(cfg.data_dir) as csv_file:
    data = list(csv.reader(csv_file, delimiter=','))
label_map = {'setosa': 0,'versicolor': 1,'virginica':2 }
#分别获取数据中的特征值X和标签值Y
X = np.array([[float(x) for x in s[:-1]] for s in data[:cfg.data_size]],np.float32)
Y = np.array([label_map[s[-1]] for s in data[:cfg.data_size]], np.int32)
# 将数据集分为训练集120条，测试集30条。
train_idx = np.random.choice(cfg.data_size, cfg.train_size, replace=False)
test_idx = np.array(list(set(range(cfg.data_size)) - set(train_idx)))
X_train, Y_train = X[train_idx], Y[train_idx]
X_test, Y_test = X[test_idx], Y[test_idx]

#---------------------------------数据预处理---------------------------------
def pre_process_data(X_train, Y_train, epoch_size):
    #生成训练集和测试集
    train = list(zip(X_train, Y_train))
    test = list(zip(X_test, Y_test))
    #使用MindSpore GeneratorDataset接口将numpy.ndarray类型的数据转换为 Dataset
    ds_train = dataset.GeneratorDataset(train, ['x', 'y'])
    ds_test = dataset.GeneratorDataset(test, ['x', 'y'])
    #数据处理--打乱顺序+分批
    ds_train = ds_train.shuffle(buffer_size=cfg.train_size)
    ds_test  = ds_test.shuffle (buffer_size=cfg.test_size)
    ds_train = ds_train.batch(batch_size=cfg.batch_size, drop_remainder=True)
    ds_test  = ds_test.batch (batch_size=cfg.test_size , drop_remainder=True)
    return ds_train, ds_test

#---------------------------------构建神经网络---------------------------------
# 训练函数
def train(network, net_opt, ds_train, prefix, directory, print_times):
    #定义网络损失函数
    net_loss = nn.SoftmaxCrossEntropyWithLogits(sparse=True, reduction="mean")
    #定义模型
    model = Model(network, loss_fn=net_loss, optimizer=net_opt, metrics={"acc"})
    #定义损失值指标
    loss_cb = LossMonitor(per_print_times=int(cfg.train_size / cfg.batch_size))
    #设置checkpoint
    config_ck = CheckpointConfig(save_checkpoint_steps=cfg.save_checkpoint_steps,
                                 keep_checkpoint_max=cfg.keep_checkpoint_max)
    ckpoint_cb = ModelCheckpoint(prefix=prefix, directory=directory, config=config_ck)
    print("============== Starting Training ==============")
    #训练模型
    model.train(epoch_size, ds_train, callbacks=[ckpoint_cb, loss_cb], dataset_sink_mode=False)
    return model

class_names=['setosa', 'versicolor', 'virginica']
# 评估预测函数
def eval_predict(model, ds_test):
    # 使用测试集评估模型，打印总体准确率
    metric = model.eval(ds_test)
    print(metric)
    # 预测
    test_ = ds_test.create_dict_iterator().__next__()
    test = Tensor(test_['x'], mindspore.float32)
    predictions = model.predict(test)
    predictions = predictions.asnumpy()
    true_label = test_['y'].asnumpy()
    for i in range(10):
        p_np = predictions[i, :]
        pre_label = np.argmax(p_np)
        print('第' + str(i) + '个sample预测结果：', class_names[pre_label], '   真实结果：', class_names[true_label[i]])


#---------------------------------模型预测---------------------------------

# --------------------------------------------------无优化器-----------------------------------

epoch_size = 20
print('------------------无优化器--------------------------')
# 数据
ds_train, ds_test = pre_process_data(X_train, Y_train, epoch_size)
# 定义网络并训练
network = nn.Dense(cfg.feature_number, cfg.num_class)
model = train(network, None, ds_train, "checkpoint_no_opt", cfg.out_dir_no_opt, 4)
# 评估预测
eval_predict(model, ds_test)

#---------------------------------
