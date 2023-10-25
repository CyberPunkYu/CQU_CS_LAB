'''
Author: XiangxinZhong
Date: 2021-11-21 20:12:57
LastEditors: XiangxinZhong
LastEditTime: 2021-11-22 23:02:22
Description: ML Lab3 决策树分类
'''

from graphviz import Digraph
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import sklearn.metrics as mtr
from sklearn.datasets import load_iris, load_wine
from draw_tree import createPlot


class Node:

    def __init__(self, feature=0.0, split=None):
        self.feature = feature
        self.split = split
        self.lc = None
        self.rc = None
        

class Clf:

    def __init__(self, features=None):
        self.root = None
        self.features = features
        self.node = [] # 存储节点信息，方便可视化
        self.edge = [] # 存储连线信息，方便可视化
        self.nodecnt = {}

    def Gini(self, label):
        gini = 1
        for (ck, cnt) in zip(*np.unique(label, return_counts=True)):
            prob_ck = cnt / len(label)
            gini -= prob_ck * prob_ck
        return gini

    def get_final_split(self, feature, label):
        # feature = np.unique(np.sort(feature))
        splits = [] # 存放所有划分点
        for i in range(feature.shape[0] - 1):
            splits.append((feature[i] + feature[i+1]) / 2)
        final_gini  = 1  # 临时最优基尼系数
        final_split = 0  # 临时最优划分点
        for i in splits:
            feature1 = np.where(feature < i)
            feature2 = np.where(feature > i)
            label1 = label[feature1]
            label2 = label[feature2]
            gini = len(label1) * 1.0 / len(label) * self.Gini(label1) + \
                   len(label2) * 1.0 / len(label) * self.Gini(label2)
            if gini < final_gini:
                final_gini = gini
                final_split = i
        return final_gini, final_split

    def buildTree(self, x, y):
        kinds, cnts = np.unique(y, return_counts=True)  # 类和每类的数量
        # 若样本全部属于同一类别，节点标记为该类
        if len(kinds) == 1:
            return Node(kinds[0])
        if x.shape[0] == 0:
            return None

        final_gini  = 1    # 最优基尼系数
        final_split = None # 最优划分
        final_feature = 0  # 最优划分点

        # 遍历每个特征的每个值
        for i in range(x.shape[1]):
            gini, split = self.get_final_split(x[:, i], y)
            if gini < final_gini:
                final_gini = gini
                final_split = split
                final_feature = i
        if final_gini < 1e-3:
            return Node(kinds[cnts.argmax(0)])  # 返回最多的那个类
        # 初始化根节点
        tree = Node(final_feature, final_split)
        # 连续值二分左右子树 递归建树
        left_index  = np.where(x[:,final_feature] < final_split)
        right_index = np.where(x[:,final_feature] > final_split)
        tree.lc  = self.buildTree(x[left_index], y[left_index])
        tree.rc = self.buildTree(x[right_index], y[right_index])
        return tree


    def fit(self, x, y):
        self.root= self.buildTree(x,y)
        
    # 前序遍历
    def pre_order(self, root, mk, pre, prename):
        if mk == 1: # 如果是根节点
            if root == None:
                return
            node_info = [] # ['name', 'label']
            index = root.feature
            feat = self.features[index]
            # 记录该节点出现的次数，用特征加次数作为新的名字
            if feat not in self.nodecnt:
                self.nodecnt[feat] = 1
            else:
                self.nodecnt[feat] += 1
            name = str(feat) + str(self.nodecnt[feat])
            node_info.append(name) # 'name'
            node_info.append(str(feat)) # 'label'
            self.node.append(node_info)
            pre = root
            prename = name
            mk -= 1
            self.pre_order(root.lc, mk, pre, prename)
            self.pre_order(root.rc, mk, pre, prename)
        else:
            # 如果是中间节点
            if root == None:
                return
            
            node_info = []
            edge_info = []# ['tail_name', 'head_name', 'label']
            index = root.feature
            feat  = self.features[index]
            if feat not in self.nodecnt:
                self.nodecnt[feat] = 1
            else:
                self.nodecnt[feat] += 1
            name = str(feat) + str(self.nodecnt[feat])
            node_info.append(name) # 'name'
            if root.split != None:
                node_info.append(str(feat)) # 'label'
            else:
                node_info.append("class "+str(index))
            self.node.append(node_info)
            edge_info.append(prename)
            edge_info.append(name)
            edge_info.append(str(pre.split))
            self.edge.append(edge_info)
            pre = root
            prename = name
            self.pre_order(root.lc, mk, pre, prename)
            self.pre_order(root.rc, mk, pre, prename)



    def draw_tree(self, name):
        dot = Digraph(name="pic", comment="测试", format="png")
        # 绘制方向。默认自顶向下TB，BT自底向上，LR:左到右
        dot.attr('graph', rankdir='TB')
        # 定义图中的节点
        for i in self.node:
            dot.node(name=i[0], label=i[1])
        # 定义图中的节点
        for j in self.edge:
            dot.edge(tail_name=j[0], head_name=j[1], label=j[2])
        # 存放在当前目录
        dot.render(filename='test_tree_' + name,
                   directory='.',  # 当前目录
                   view=True)
                   
    def get_label(self, x):
        root = self.root
        split = root.split
        while root.split is not None:
            idx = root.feature
            if x[idx] < root.split:
                # if root.lc != None:
                    root = root.lc
                # else:
                #     break
            else:
                # if root.rc != None:
                    root = root.rc
                # else:
                #     break
        return root.feature

    def pred(self, x, y):
        y_pred = [self.get_label(xi) for xi in x]
        scores = mtr.accuracy_score(y, y_pred)
        return scores


if __name__ == "__main__":
    data = load_wine()
    df = pd.read_excel('winequality_data.xlsx')
    x = df.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]].values
    features = list(df.columns)[0:11]
    x = np.array(list(x))
    y = np.array(list(df.iloc[:, [11]].values))

    # 划分数据集
    # x, y = data['data'][0:,:11], data['target']
    # features = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    # print(y_test)
    clf = Clf()
    clf.features = features
    
    clf.fit(x_train, y_train)
    clf.pre_order(clf.root, 1, None, None)
    clf.draw_tree("wine")
    scores = clf.pred(x_test, y_test)
    print("Accuracy: {}".format(scores))
    

