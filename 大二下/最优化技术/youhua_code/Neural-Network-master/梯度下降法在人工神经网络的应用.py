import gzip
import struct
import matplotlib.pyplot as plt
import numpy as np
import os

PATH = os.getcwd()#得到当前路径
epoch       = 500 #总共训练500轮
feature     = 784 # 输入层神经元个数
hideCount   = 30  # 隐藏层神经元个数
outputCount = 10  # 输出层神经元个数
np.random.seed(0)
total_cost = []   # 记录总的代价
def load_mnist(path, kind):
    """
    path:数据集的路径
    kind:值为train，代表读取训练集
    return: images: 60000*784
    labels:手写数字对应的类标（整数0~9）
    """
    labels_path = os.path.join(path, '%s-labels-idx1-ubyte.gz' % kind)
    images_path = os.path.join(path, '%s-images-idx3-ubyte.gz' % kind)
    # 使用gzip打开文件
    with gzip.open(labels_path, 'rb') as lbpath:
        # 使用struct.unpack方法读取前两个数据，>代表高位在前，I代表32位整型。lbpath.read(8)表示一次从文件中读取8个字节
        # 这样读到的前两个数据分别是magic number和样本个数
        magic, n = struct.unpack('>II', lbpath.read(8))
        # 使用np.fromstring读取剩下的数据，lbpath.read()表示读取所有的数据
        labels = np.frombuffer(lbpath.read(), dtype=np.uint8)
        # labels.setflages(write=1)
    with gzip.open(images_path, 'rb') as imgpath:
        magic, num, rows, cols = struct.unpack('>IIII', imgpath.read(16))
        images = np.frombuffer(imgpath.read(), dtype=np.uint8).reshape(len(labels), 784)
        # images.setflags(write=1)
    return images/250 , labels

x_train, y_train = load_mnist(PATH , 'train')  # 读取训练集
x_test , y_test  = load_mnist(PATH , 't10k')

def sigmoid(x):#sigmoid函数
    return 1.0/(1.0 + np.exp(-x))

def sigmoid_derivative(x):#sigmoid函数求导
    return sigmoid(x)*(1-sigmoid(x))

def computeOutput(sample, W_1, W_2, hideCount, outputCount):
    """
    通过一个样本的特征向量，就算出它在这个标签下所算出的结果
    sample: 特征向量 1 x 785
    W_1: 输入层到隐层的权值 785 x 30
    W_2: 隐层到输出层的权值 30 x 10
    hideCount: 隐层数量
    outputCount: 输出层的数量
    return: 计算出来的标签 1 x 10
    """
    # 将输入层算到隐层
    hideRes = sigmoid(sample.dot(W_1))
    # 将隐层算到输出层
    outputRes = sigmoid(hideRes.dot(W_2))  # 1 x 10
    return outputRes, hideRes

def get_cost(res, y):
    """
    计算损失函数的值
    这里我采用均方误差计算损失值
    res: 用样本训练出来的结果
    y:   样本的标签
    """
    temp = res - y
    #C = 0.5*(a3-ti)**2
    return (temp.dot(temp.T))[0][0] / 2

def grandOptimal(x, y, Ss, hs, W_1, W_2, alpha):
    """
    对某一个样本进行梯度下降优化
    x: 样本的特征值 1 x 785
    y: 样本标签的增广矩阵 1 x 10
    Ss: 样本的结果矩阵 1 x 10
    hs: 隐层的结果矩阵 1 x 30
    W_1: 输入层到隐层的权值 785 x 30
    W_2: 隐层到输出层的权值 31 x 10
    alpha: 学习率
    :return: 更新好的权值
    """
    # 计算权值的导数
    grandW_1 = (hs * (1 - hs)).T * (W_2 @ (Ss * (1 - Ss) * (y - Ss)).T) @ x  # 30 x 785
    grandW_2 = (Ss * (1 - Ss) * (y - Ss)).T @ hs  # 10 x 30
    grandW_1 = grandW_1.T  # 785 x 30
    grandW_2 = grandW_2.T  # 30 x 10
    # 更新权值
    W_1 += alpha * grandW_1
    W_2 += alpha * grandW_2
    return W_1, W_2

def train():
    # 在x_train最后一列加上一列1，便于加上偏置项 60000*785
    X_train = np.concatenate((x_train, np.ones((x_train.shape[0], 1))), axis=1)
    # 采用正太随机生成权值w1 785 x 30
    W_1 = np.random.uniform(-1.0, 1.0, size = hideCount * (feature + 1))
    W_1 = W_1.reshape(feature + 1 , hideCount)
    # 采用正太随机生成权值w2 30 x 10
    W_2 = np.random.uniform(-1.0, 1.0, size = outputCount * (hideCount))
    W_2 = W_2.reshape(hideCount , outputCount)
    alpha = 0.1  # 学习率

    # 开始训练
    for j in range(epoch):
        res = []  # 存储每个样本训练出来的结果
        cost = 0
        # print('epoch %d' %j)
        for i in range(X_train.shape[0]):  # 每个样本都会进行 X_train.shape[0]
            sample = np.array([X_train[i, :]])  # 获取样本 1 x 785
            outputRes, hideRes = computeOutput(sample, W_1, W_2, hideCount, outputCount)  # 计算此权值下的结果
            y = [0] * outputCount  # 构造标签的增广矩阵
            y[y_train[i]] = 1
            y = np.array([y])  # 1 x 10
            cost += get_cost(outputRes, y)  # 计算均方误差
            W_1, W_2 = grandOptimal(sample, y, outputRes, hideRes, W_1, W_2, alpha)  # 更新权值
            sampleRes = np.where(outputRes[0] == max(outputRes[0]))[0][0]  # 一个样本训练完成
            res.append(sampleRes)  # 将样本结果装入好的
        total_cost.append(cost)
        if j % 50 == 0:
            print("epoch {:d}: 总均方差为: {:.5f}" .format(j,cost))
    #绘制损失度曲线图
    arr_cost = np.asarray(total_cost)
    x = range(epoch)
    plt.plot(x , arr_cost)
    plt.ylabel('Cost')
    plt.xlabel('Epochs')
    plt.show()
    print("训练完成")
    return W_1, W_2

def test(W_1, W_2):
    # 在x_test最后一列加上一列1，便于加上偏置项 10000*785
    X_test = np.concatenate((x_test, np.ones((x_test.shape[0], 1))), axis=1)
    Y_test = np.array([y_test]).T
    res = []
    for i in range(X_test.shape[0]):
        sample = np.array([X_test[i, :]])  # 获取测试样本 1 x 785
        outputRes, _ = computeOutput(sample, W_1, W_2, hideCount, outputCount)  # 计算结果
        res.append(np.argmax(outputRes, axis=1))
    rightCount = 0
    for i in range(Y_test.shape[0]):
        if res[i][0] == Y_test[i][0]:
            rightCount += 1
    print('测试正确率为{:.3%}'.format(rightCount / Y_test.shape[0]))
if __name__ == "__main__":
    w1, w2 = train()
    test(w1, w2)
