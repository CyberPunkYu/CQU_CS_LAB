import numpy as np
import pandas as pd
from graphviz import Digraph
from sklearn.datasets import load_iris, load_wine
from sklearn.metrics import accuracy_score, r2_score
from sklearn.model_selection import train_test_split


class Node:
    def __init__(self, feature=None, split=None, score=None):
        '''
        param feature: 第几个特征或者叶节点是哪一类
        param split: 分裂点
        param score: 回归使用，表示预测的y值是什么
        param mse: 均方误差
        '''
        self.feature = feature
        self.split = split
        self.score = score
        self.mse = None
        self.left = None
        self.right = None

class CART:
    def __init__(self, features=None, flag = 0, belong = None):
        """
        :param features: 特征列表，存放所有分裂特征
        :param alpha: 基尼精准度,仅在分类时使用
        :param flag: flag为1表示分类，为0表示回归
        """
        self.root = None
        self.features = features
        self.alpha = 1e-3
        self.max_depth = 5
        self.flag = flag
        self.belong = belong
        self.node = [] # 存储节点信息，方便可视化
        self.edge = [] # 存储连线信息，方便可视化
        self.nodecnt = {}

    # get Gini index
    def calGini(self, label):
        gini = 1
        # 对于一维数组或者列表，unique函数去除其中重复的元素，
        # 并按元素由大到小返回一个新的无元素重复的元组或者列表,
        # 添加return_counts = True 参数，可以返回每个特征出现的次数
        for (kind, cnt) in zip(*np.unique(label, return_counts = True)):
            p = cnt / len(label)
            gini -= p * p
        return gini

    # 计算均方误差
    def calMse(self, data, label, idx, feature, split):
        '''
        对其中一类特征值，且一直划分点，求均方误差
        :param data: x值
        :param label: y值
        :param idx: x值的索引
        :param feature: y值的索引(行)
        :param split: 划分点
        '''
        sum = [0, 0] # 划分点部分y值之和
        cnt  = [0, 0] # 划分点的样本数量
        s_sum = [0.0, 0.0]
        for i in idx:
            x, y = data[i][feature], label[i]
            if data[i][feature] <= split:
                sum[0] += label[i]
                cnt[0] += 1
                s_sum[0] += y**2
            else:
                sum[1] += label[i]
                cnt[1] += 1
                s_sum[1] += y**2
        # 以平均值作为预测y，以此计算均方误差
        left_avg_y = sum[0] * 1.0 / cnt[0] if cnt[0] > 0 else 0
        right_avg_y = sum[1] * 1.0 / cnt[1] if cnt[1] > 0 else 0
        left_mse = s_sum[0] - sum[0]*left_avg_y
        right_mse = s_sum[1] - sum[1]*right_avg_y
        mse = left_mse + right_mse
        avg = left_avg_y + right_avg_y
        return mse, avg, split

    # 确定最优划分点
    def _choose_split(self, x, y, idx, feature):
        '''
        在calMse基础上，计算每一类特征中的最优划分点
        '''
        data = set([x[i][feature] for i in idx]) # 提取要计算的一列样本数据并去重
        # print("feature: ", feature)
        # print("data: ",data)
        final_mse = float('inf')
        final_split = 0
        final_mean = 0
        for i in data:
            mse, avg, split = self.calMse(x, y, idx, feature, i)
            # print("split: ",i)
            # print("mse: ", mse)
            if mse < final_mse:
                final_mse = mse
                final_mean = avg
                final_split = split
        # print("final_mse: ",final_mse)
        # print("final_split: ",final_split)
        return final_mse, final_mean, final_split

    # 在整个样本中确定最优特征及其划分点
    def _choose_feature(self, x, y, idx):
        '''
        在choose_split基础上，选择最优特征
        '''
        final_mse = float('inf')
        final_feature = 0
        final_split = 0
        final_prey = 0
        for i in range(len(x[0])):
            mse, avg, split = self._choose_split(x, y, idx, i)
            if mse < final_mse:
                final_mse = mse
                final_feature = i
                final_split = split
                final_prey = avg
        return final_mse, final_feature, final_split, final_prey


    def fit(self, x_train, y_train):
        if self.flag:
            self.c_fit(x_train, y_train)
        else:
            self.r_fit(x_train, y_train)
        print("-----------------" + self.belong + " train finished-----------------")

    def r_fit(self, x_train, y_train):
        self.root = self._build_node(x_train, y_train, 0)
        

    def c_fit(self, x_train, y_train):
        self.root = self.build_node(x_train, y_train)


    def predict(self, x):
        return [self._predict(xi) for xi in x]

    def _predict(self, x): # 分类
            root = self.root
            # split = root.split
            while root.split != None:  # 遍历直到叶节点
                idx = root.feature
                if x[idx] < root.split:
                    if root.left != None:
                        root = root.left
                    else:
                        break
                else:
                    if root.right != None:
                        root = root.right
                    else:
                        break
            if self.flag:
                return root.feature
            else:
                return root.score

    # 计算单个连续属性的基尼值和划分点
    def get_continuous_gini(self, feature, label):
        # feature = np.sort(feature) # 先对该特征的值进行按列排序
        # feature = np.unique(feature) # 考虑到可能会出现相同值，去除重复函数
        splits = [] # 存放所有划分点
        for i in range(feature.shape[0] - 1):
            splits.append((feature[i] + feature[i+1]) / 2)
        final_split = 0
        final_gini  = 1
        for i in splits: # 遍历所有划分点，找到最优划分点
            # 根据划分点，得到对应划分的下标
            feature1 = np.where(feature < i)
            feature2 = np.where(feature > i)
            # 对应的标签
            label1 = label[feature1]
            label2 = label[feature2]
            # 计算gini
            gini = len(label1) * 1.0 / len(label) * self.calGini(label1) + \
                   len(label2) * 1.0 / len(label) * self.calGini(label2)
            if gini < final_gini:
                final_split = i
                final_gini  = gini
        return final_gini, final_split


    def _build_node(self, x, y, depth):
        idxs = list(range(len(y)))
        # 如果该分支没有样本
        if len(idxs) == 0:
            return None
            # 样本数1
        elif len(idxs) == 1 or depth > self.max_depth:
            mean = 0
            for i in idxs:
                mean += y[i]
            return Node(feature = "end", score = mean / len(idxs))
        else:
            mse, feature, split, prey = self._choose_feature(x, y, idxs)
            # 建立根节点
            tree = Node(feature=feature, split=split, score=prey)
            tree.mse = mse
            left_index  = np.where(x[:, feature] <= split)
            right_index = np.where(x[:, feature] > split)
            tree.left  = self._build_node(x[left_index], y[left_index], depth + 1)
            tree.right = self._build_node(x[right_index], y[right_index], depth + 1)
            return tree


     # 根据当前样本选择最优划分属性和划分点，向下生成两个节点
    def build_node(self, x, y):
        '''
        递归建立二叉树,当节点纯度或者当前节点划分的样本数达到阈值即回溯
        param x: x训练集
        param y: 训练集标签
        '''
        kind, cnt = np.unique(y, return_counts=True)  # 统计类和每类的数量
        if len(kind) == 1: # 递归到只有一个类标签
            return Node(kind[0])
        if x.shape[0] == 0: # 如果该分支没有样本
            return None
        
        final_gini  = 1       # 最优基尼系数
        final_split = 0       # 最优划分点
        final_index = 0       # 最优划分对应下标
        # 遍历训练集中所有的特征，计算对应基尼值
        for i in range(x.shape[1]):
            gini, split = self.get_continuous_gini(x[:,i], y)
            if gini < final_gini:
                final_gini  = gini
                final_split = split
                final_index = i
        # 如果所有特征的基尼值都小于阈值，则返回最多的那个类
        if final_gini < self.alpha: 
            return Node(kind[cnt.argmax(0)]) 
        # 建立根节点
        tree = Node(final_index, final_split)
        # where操作划分左右数据
        left_index  = np.where(x[:,final_index] < final_split)
        right_index = np.where(x[:,final_index] > final_split)
        tree.left  = self.build_node(x[left_index], y[left_index])
        tree.right = self.build_node(x[right_index], y[right_index])
        return tree
    
    def getAcc(self, x_test, y_test):
        y_pre = self.predict(x_test)
        ACC = accuracy_score(y_test, y_pre)
        print(self.belong + "--准确率: ", ACC)

    def getR2(self, x_test, y_test):
        y_pre = np.array(self.predict(x_test))
        R2 = r2_score(y_test, y_pre)
        print(self.belong + "--R2: ", R2)


    # 
    def _pre_order(self, root, mk, pre, prename, icon = None):
        if mk == 1: # 如果是根节点
            if root == None:
                return
            index = root.feature
            feat = self.features[index]
            # 记录该节点出现的次数，用特征加次数作为新的名字
            if feat not in self.nodecnt:
                self.nodecnt[feat] = 1
            else:
                self.nodecnt[feat] += 1
            name = str(feat) + str(self.nodecnt[feat])
            self.node.append([name, str(feat)])
            # 将该节点作为父节点传入子节点递归
            self._pre_order(root.left, mk - 1, root, name, icon="<")
            self._pre_order(root.right, mk - 1, root, name, icon=">")
        else:
            if root == None:
                return
            node_info = []
            index = root.feature
            if index != "end":
                feat = self.features[index]
            else:
                feat = "end"
            if feat not in self.nodecnt:
                self.nodecnt[feat] = 1
            else:
                self.nodecnt[feat] += 1
            name = str(feat) + str(self.nodecnt[feat])
            node_info.append(name) # 'name'
            if root.split != None:
                node_info.append(str(feat)) # 'label'
            else:
                node_info.append(str(root.score))
            self.node.append(node_info)
            self.edge.append([prename, name, (icon + str(pre.split))])
            self._pre_order(root.left, mk, root, name, icon="<")
            self._pre_order(root.right, mk, root, name, icon=">")

    # 前序遍历
    def pre_order(self, root, mk, pre, prename, icon = None):
        if mk == 1: # 如果是根节点
            if root == None:
                return
            index = root.feature
            
            feat = self.features[index]
            # 记录该节点出现的次数，用特征加次数作为新的名字
            if feat not in self.nodecnt:
                self.nodecnt[feat] = 1
            else:
                self.nodecnt[feat] += 1
            name = str(feat) + str(self.nodecnt[feat])
            self.node.append([name, str(feat)])
            self.pre_order(root.left, mk - 1, root, name, icon="<")
            self.pre_order(root.right, mk - 1, root, name, icon=">")
        else:
            # 如果是中间节点
            if root == None:
                return
            node_info = []
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
            self.edge.append([prename, name, (icon + str(pre.split))])

            self.pre_order(root.left, mk, root, name, icon="<")
            self.pre_order(root.right, mk, root, name, icon=">")

                
        
    def draw_tree(self):
        dot = Digraph(name="pic", comment="测试", format="png")
        # 绘制方向。默认自顶向下TB，BT自底向上，LR:左到右
        dot.attr('graph', rankdir='TB')
        # 定义图中的节点
        for i in self.node:
            dot.node(name=i[0], label=i[1])
        # 定义图中的连线
        for j in self.edge:
            dot.edge(tail_name=j[0], head_name=j[1], label=j[2])
        # 存放在当前目录
        dot.render(filename='tree_' + self.belong,
                   directory='.',  # 当前目录
                   view=True)


def run(x_train, x_test, y_train, y_test, features, flag, belong):
    cart = CART(features=features, flag=flag, belong=belong)
    cart.fit(x_train, y_train)
    
    if cart.flag:
        cart.getAcc(x_test, y_test)
        cart.pre_order(cart.root, 1, None, None)
        cart.draw_tree()
    else:
        cart.getR2(x_test, y_test)
        cart._pre_order(cart.root, 1, None, None)
        cart.draw_tree()
    

def iris():
    data = load_iris()
    x = data['data']  
    y = data['target']
    features = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=9)
    run(x_train, x_test, y_train, y_test, features, 1, "iris")

def wine():
    df = pd.read_excel('winequality_data.xlsx')
    features = list(df.columns)[0:11]
    data = load_wine()
    x = data['data'][0:,:11]
    y = data['target']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=11)
    run(x_train, x_test, y_train, y_test, features, 1, "wine")
    
def ice_cream():
    df = pd.read_excel('icecream_data.xlsx')
    features = ["Temperature"]
    X = df.iloc[:, [0]].values
    X = np.array(list(X))
    Y = np.array(list(df.iloc[:, [1]].values))
    x1, x2, y1, y2 = train_test_split(X, Y, test_size=0.2)
    run(x1, x2, y1, y2, features, 0, "icecream")

def housing():
    df = pd.read_excel('housing_data.xlsx')
    X = df.iloc[:, [0, 1, 2, 3, 4]].values
    features = list(df.columns)[0:5]
    X = np.array(list(X))
    Y = np.array(list(df.iloc[:, [5]].values))
    x1, x2, y1, y2 = train_test_split(X, Y, test_size=0.05, random_state=0)
    x_train, x_test, y_train, y_test = train_test_split(x2, y2, test_size=0.1, random_state=2)
    run(x_train, x_test, y_train, y_test, features, 0, "house")

if __name__ == "__main__":
    iris()
    # wine()
    # ice_cream()
    # housing()

