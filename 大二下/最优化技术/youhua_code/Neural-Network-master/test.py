
import gzip
import struct
import numpy as np
import os

def load_mnist_test(path, kind='t10k'):
    """
    path:数据集的路径
    kind:值为test，代表读取测试集
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

def sigmoid(x):
    return 1.0/(1.0 + np.exp(-x))

def computeOutput(sample, W_1, W_2, hideCount, outputCount):
    """
    通过一个样本的特征向量，就算出它在这个标签下所算出的结果
    sample: 特征向量 1 x 785
    W_1: 输入层到隐层的权值 785 x 128
    W_2: 隐层到输出层的权值 128 x 10
    hideCount: 隐层数量
    outputCount: 输出层的数量
    :return: 计算出来的标签 1 x 10
    """
    # 将输入层算到隐层
    hideRes = sigmoid(sample@W_1)
    # 将隐层算到输出层
    outputRes = sigmoid(hideRes @ W_2)  # 1 x 10
    return outputRes, hideRes

if __name__ == '__main__':
    W_1 = np.loadtxt('W1.txt')
    W_2 = np.loadtxt('W2.txt')
    x_test, y_test = load_mnist_test('D:/learning program/python/最优化技术')  # 读取测试集
    X_test = np.concatenate((x_test, np.ones((x_test.shape[0], 1))), axis=1)  # 增加偏置项 10,000 x 785

    # 设置参数
    hideCount = 128
    outputCount = 10
    y_test = np.array([y_test]).T

    res = []
    for i in range(X_test.shape[0]):
        sample = np.array([X_test[i, :]])  # 获取测试样本 1 x 785
        outputRes, _ = computeOutput(sample, W_1, W_2, hideCount, outputCount)  # 计算结果
        res.append(np.argmax(outputRes, axis=1))

    rightCount = 0
    for i in range(y_test.shape[0]):
        if res[i][0] == y_test[i][0]:
            rightCount += 1

    print('经比较，正确率为{:.3%}'.format(rightCount / y_test.shape[0]))
