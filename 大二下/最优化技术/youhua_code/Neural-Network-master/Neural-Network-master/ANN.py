from ctypes import sizeof
import gzip
import os
import struct
from matplotlib.image import imsave
import numpy as np
import matplotlib.pyplot as plt

PATH = os.getcwd()  #得到当前路径

def load_mnist(PATH , KIND = 'train'): 
# 说明：load_mnist 函数返回两个数组, 第一个是一个 n x m 维的 NumPy array(images), 这里的 n 是样本数, m 是特征数。 
# 训练数据集包含 60,000 个样本, 测试数据集包含 10,000 样本. 在 MNIST 数据集中的每张图片由 28 x 28 个像素点构成,
# 每个像素点用一个灰度值表示。 load_mnist 函数返回的第二个数组(labels) 包含了相应的目标变量, 也就是手写数字的类标签(整数 0-9).
# 显示数据集中的某个数字参考代码如下：
# PATH:数据集的路径
# KIND:值为train，代表读取训练集
    labels_path = os.path.join(PATH,'%s-labels-idx1-ubyte.gz'% KIND)    #拼接得到绝对路径
    images_path = os.path.join(PATH,'%s-images-idx3-ubyte.gz'% KIND)
    #使用gzip打开文件
    with gzip.open(labels_path, 'rb') as lbpath:
	    #使用struct.unpack方法读取前两个数据，>代表高位在前，I代表32位整型。lbpath.read(8)表示一次从文件中读取8个字节
	    #这样读到的前两个数据分别是magic number和样本个数
        magic, n = struct.unpack('>II',lbpath.read(8))
        # print(n)
        #使用np.fromstring读取剩下的数据，lbpath.read()表示读取所有的数据
        labels = np.frombuffer(lbpath.read(),dtype = np.uint8)
        # print(labels)
    with gzip.open(images_path, 'rb') as imgpath:
        #使用大端法读取4个字节，第一个是魔数，第二个是个数，三四分别是rows、cols
        magic, num, rows, cols = struct.unpack('>IIII',imgpath.read(16))
        #依次读取值，并reshape为length*784的矩阵
        images = np.frombuffer(imgpath.read(),dtype = np.uint8).reshape(len(labels), 784)
        # print(images)
    return images, labels

#加载数据
TRAIN_IMAGES , TRAIN_LABELS = load_mnist(PATH , KIND = 'train')
PRE_IMAGES   , PRE_LABELS   = load_mnist(PATH , KIND = 't10k')
def plotNumPic(images, labels):# 按照2*5的方式排列显示单个数字的图像
    #创建画布
    fig, ax = plt.subplots(nrows=2, ncols=5, sharex=True, sharey=True, )
    #平铺画布
    ax = ax.flatten()
    for i in range(10):
        #获取数据集中第一次出现的0-9数字，并reshape到28*28的矩阵
        img = images[labels == i][0].reshape(28, 28)
        #绘制数字
        ax[i].imshow(img, cmap='Greys', interpolation='nearest')
    #隐藏横纵坐标
    ax[0].set_xticks([])
    ax[0].set_yticks([])
    #美化画布，使之更紧凑
    plt.tight_layout()
    #绘制
    plt.show()
# print(TRAIN_LABELS)
# plotNumPic(TRAIN_IMAGES,TRAIN_LABELS)
# print(TRAIN_IMAGES.shape[0])
# print(TRAIN_IMAGES.shape[1])
print(TRAIN_LABELS.shape[0])
# print(TRAIN_LABELS.shape[1])

class ANN():
    def __init__(self, n_output, n_feature, n_hidden = 30 ,
                l1 = 0, l2 = 2, epoch = 500, eta = 0.001, alpha = 0.0, decrease_const=0.0,
                 shuffle=True, minibatches=1, random_state=None):
        '''
        n_output: 输出单元
        n_feature: 输入单元
        n_hidden: 隐层单元
        l1: L1正则化系数 lamda
        l2: L2正则化系数 lamda
        epoch: 遍历训练集的次数（迭代次数）
        eta: 学习速率
        alpha: 动量学习进度的参数，它在上一轮的基础上增加一个因子，用于加快权重更新的学习
        decrease_const: 用于降低自适应学习速率 n 的常数 d ，随着迭代次数的增加而随之递减以更好地确保收敛
        shuffle: 在每次迭代前打乱训练集的顺序，以防止算法陷入死循环
        minibatches: 在每次迭代中，将训练数据划分为 k 个小的批次，为加速学习的过程，
                            梯度由每个批次分别计算，而不是在整个训练集数据上进行计算。
        random_state:
        '''
        np.random.seed(random_state)
        self.n_output = n_output
        self.n_feature = n_feature
        self.n_hidden = n_hidden
        self.w1, self.w2 = self.initialize_weights()
        self.l1 = l1
        self.l2 = l2
        self.epoch = epoch
        self.eta = eta
        self.alpha = alpha
        self.decrease_const = decrease_const
        self.shuffle = shuffle
        self.minibatches = minibatches

    def encode_onehot(self, y_label, k):  #将标签信息编码为独热码
        #y为训练集的标签， k为第一维度，即输出层个数
        onehot = np.zeros((k, y_label.shape[0]), dtype=np.int)  #10*60000
        for idx, val, in enumerate(y_label):
            onehot[val, idx] = 1.0
        return onehot

    def initialize_weights(self):
        #采用正太分布随机数设置权重
        w1 = np.random.uniform(-1,1,size = self.n_hidden * (self.n_feature + 1))
        #规范成矩阵型----30*785
        w1 = w1.reshape(self.n_hidden , self.n_feature + 1) 
        w2 = np.random.uniform(-1,1,size = self.n_output * (self.n_hidden + 1))
        #规范成矩阵型----10*31
        w2 = w2.reshape(self.n_output, self.n_hidden)
        return w1, w2
    
        
    def sigmoid(self, z):  #sigmoid 激活函数
        return 1.0/(1.0 + np.exp(-z))

    def sigmoid_g(self, z): #sigmoid 梯度
        return self.sigmoid(z) * (1 - self.sigmoid(z))

    def add_b(self, x_image, mode = 'c'):#由于偏置是放在w中的，在这添加一行1后，方便偏置的直接相加
        if mode == 'c':
            #在第一列添加1
            x_new = np.ones((x_image.shape[0], x_image.shape[1] + 1))
            x_new[:, 1:] = x_image
        elif mode == 'r':
            #在第一行添加1
            x_new = np.ones((x_image.shape[0] + 1, x_image.shape[1]))
            x_new[1:, :] = x_image
        else: raise AttributeError("'mode' must be 'c' or 'r'")
        return x_new
    
    def forward(self, x_image, w1, w2, b1, b2):
        '''
        x  = 60000*784  输入层
        w1 = 30*784     第一层权重
        b1 = 30*1       第一层偏移
        w2 = 10*30      第二层权重
        b2 = 10*1       第二层偏移
        a1 = 60000*784  输入层
        z2 = 30*60000   隐藏层
        a2 = 30*60000   激活后
        z3 = 10*60000   输出层
        a3 = 10*60000   激活后
        '''
        z2 = w1.dot(x_image.T)
        #每一列加上偏置
        for col in z2.T:
            col += b1.T[0]
        a2 = self.sigmoid(z2)
        z3 = w2.dot(a2)
        #每一列加上偏置
        for col in z3.T:
            col += b2.T[0]
        a3 = self.sigmoid(z3)
        return  z2, a2, z3, a3

    def L2(self, lambda_, w1, w2):#计算 L2 正则化代价
        return (lambda_/2.0) * (np.sum(w1[:, 1:] ** 2) + np.sum(w2[:, 1:] ** 2))

    def L1(self, lambda_, w1, w2):#计算 L1 正则化代价
        return (lambda_/2.0) * (np.abs(w1[:,1:]).sum() + np.abs(w2[:, 1:]).sum())

    def get_cost(self, y_label, a3, w1, w2):#计算代价
        '''
        y_label 10*60000
        a3 10*60000
        w1 30*784
        w2 10*30
        '''
        t1 = -y_label * np.log(a3)    #-t * log(a3)
        t2 = (1 - y_label) * np.log(1 - a3) #(1-t) * log(1-a3)
        c1 = np.sum(t1 - t2)
        lt1= self.L1(self.l1, w1, w2)
        lt2= self.L2(self.l2, w1, w2)
        cost = c1 + lt1 + lt2
        return cost

    def _get_gradient(self, a1, a2, a3, z2, y_enc, w2, w1):
        # 反向传播
        sigma3 = a3 - y_enc
        z2 = self._add_bias_unit(z2, how='row')
        sigma2 = w2.T.dot(sigma3) * self._sigmoid_gradient(z2)
        sigma2 = sigma2[1:, :]
        grad1 = sigma2.dot(a1)
        grad2 = sigma3.dot(a2.T)
        # 调整
        grad1[:, 1:] += (w1[:, 1:] * (self.l1 + self.l2))
        grad2[:, 1:] += (w2[:, 1:] * (self.l1 + self.l2))

        return grad1, grad2
if __name__ == '__main__':
    nn = ANN(n_output=10,
            n_feature = TRAIN_IMAGES.shape[1],
            n_hidden = 30,
            l2 = 0.1,
            l1 = 0.0,
            epoch = 1000,
            eta = 0.001,
            decrease_const = 0.00001,
            shuffle = True,
            minibatches = 50,
            random_state = 1)
    



