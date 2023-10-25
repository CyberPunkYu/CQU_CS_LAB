
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import sklearn.metrics as mtr
from sklearn.datasets import load_iris, load_wine, load_boston
from pydotplus.graphviz import graph_from_dot_data
from sklearn.tree import export_graphviz
from draw_tree import createPlot
import matplotlib.pyplot as plt



class Node:
    '''
    description: 
    param {*} self
    param {*} score
    return {*}
    '''

    def __init__(self, score=None):
        self.score = score
        self.feat_idx = None
        self.lc = None
        self.rc = None
        self.pos = None


def list_split(X, idxs, feature, split):
    ret = [[], []]

    while idxs:
        if X[idxs[0]][feature] < split:
            ret[0].append(idxs.pop(0))
        else:
            ret[1].append(idxs.pop(0))
    # left_index  = np.where(X[:, feature] < split)
    # right_index = np.where(X[:, feature] > split)
    # ret[0] = left_index
    # ret[1] = right_index
    return ret


class Reg(object):

    '''
    description: 构造函数，为了防止过拟合，要限制树的深度
    '''

    def __init__(self):
        self.root = Node()
        self.depth = 0

    '''
    description: 计算划分的MSE，此处以MSE作为损失函数
    param {*} self
    param {*} data 特征矩阵
    param {*} labels 类别
    param {*} nums 样本数量
    param {*} feat_idx 选择的特征下标
    param {*} pos 该特征划分点
    return {*}
    '''

    def get_mse(self, data, labels, nums, feat_idx, pos):
        split_sum = [0.0, 0.0]
        split_cnt = [0.0, 0.0]
        split_square_sum = [0.0, 0.0]
        # 对所有样本进行划分
        for i in nums:
            # 样本该特征的值和类别
            x, y = data[i][feat_idx], labels[i]
            if x < pos:
                split_cnt[0] += 1
                split_sum[0] += y
                split_square_sum[0] += y**2
            else:
                split_cnt[1] += 1
                split_sum[1] += y
                split_square_sum[1] += y**2
        # 计算MSE
        split_average = [split_sum[0]/split_cnt[0], split_sum[1]/split_cnt[1]]
        split_mse = [split_square_sum[0] - split_sum[0]*split_average[0],
                     split_square_sum[1] - split_sum[1]*split_average[1]]
        return sum(split_mse), pos, split_average

    '''
    description: 选择最优划分
    param {*} self
    param {*} data 特征矩阵
    param {*} labels 类别
    param {*} rows 样本数量列表
    param {*} feat_idx 特征索引
    return {*}
    '''

    def get_best_split(self, data, labels, nums, feat_idx):
        ss = set([data[i][feat_idx] for i in nums])
        if len(ss) == 1:
            return None
        # 无分割
        ss.remove(min(ss))
        # 获取最优划分
        mse, pos, split_average = min((self.get_mse(
            data, labels, nums, feat_idx, pos) for pos in ss), key=lambda x: x[0])
        return mse, feat_idx, pos, split_average

    '''
    description: 获取最优特征
    param {*} self
    param {*} data
    param {*} labels
    param {*} idx
    return {*}
    '''

    def get_best_feature(self, data, labels, idx):
        length = len(data[0])
        split_rets = map(lambda j: self.get_best_split(
            data, labels, idx, j), range(length))
        split_rets = filter(lambda x: x is not None, split_rets)
        return min(split_rets, default=None, key=lambda x: x[0])

    '''
    description: 拟合
    param {*} self
    param {*} data 特征矩阵
    param {*} labels 类别
    param {*} max_depth 最大深度，注意太深导致过拟合
    param {*} min_samples_split 
    return {*}
    '''

    def fit(self, data, labels, max_depth=5):
        idxs = list(range(len(labels)))
        q = [(self.depth + 1, self.root, idxs)]
        while q:
            depth, node, idx = q.pop(0)
            # 超过最大深度，停止循环
            if depth > max_depth:
                break
            # 节点属于同一类别
            if len(idx) == 1:
                continue
            split_ret = self.get_best_feature(data, labels, idx)
            if split_ret == None:
                continue
            _, feat_idx, pos, split_average = split_ret
            # 更新当前节点属性
            node.feat_idx = feat_idx
            node.pos = pos
            node.lc = Node(split_average[0])
            node.rc = Node(split_average[1])
            # 当前节点的子节点放入队列中
            idx_list = list_split(data, idx, feat_idx, pos)
            q.append((depth + 1, node.lc, idx_list[0]))
            q.append((depth + 1, node.rc, idx_list[1]))

    def predOne(self, sample):
        node = self.root
        while node.lc != None and node.rc != None:
            if sample[node.feat_idx] < node.pos:
                node = node.lc
            else:
                node = node.rc
        return node.score

    def predAll(self, samples):
        return [self.predOne(sample) for sample in samples]


if __name__ == "__main__":
    # data = pd.read_excel("housing_data.xlsx")
    data = pd.read_excel("icecream_data.xlsx")

    X = data.iloc[:1000, :len(data.columns)-1].values
    y = data.iloc[:1000, -1].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    reg = Reg()

    reg.fit(X_train, y_train, max_depth=5)

    y_pred = reg.predAll(X_test)
    mse = mtr.mean_squared_error(y_test, y_pred)
    R2 = mtr.r2_score(y_test, y_pred)
    print("R2为:{},  均方误差为: {}".format(R2, mse))
