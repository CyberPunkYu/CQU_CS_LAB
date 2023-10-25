import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score, r2_score
from sklearn.model_selection import train_test_split








class Node:
    def __init__(self, feature=None, split=None, score=None):
        '''
        param feature: 第几个特征
        param split: 分裂点
        param score: 回归使用，表示预测的y值是什么
        '''
        self.feature = feature
        self.left = None
        self.right = None
        self.split = split
        self.score = score
        self.mse = 0



class CART:
    def __init__(self, alpha=1e-3, flag=None, max_depth=5):
        """
        :param alpha: 基尼精准度,仅在分类时使用
        :param flag: flag为1表示分类，为0表示回归
        """
        self.root = None
        self.feat_names = None
        self.alpha = alpha
        self.flag = flag
        self.depth = 1
        self.max_depth = max_depth

    def fit(self, x_train, y_train):
        if self.flag:  # 分类
            self.feat_names = x_train.columns.values.tolist()
            self.c_fit(x_train, y_train)
        else:  # 回归
            self.root = Node()
            self.r_fit(x_train, y_train, max_depth=self.max_depth)

    def c_fit(self, x_train, y_train):
        """
        分类
        :param x_train:
        :param y_train:
        :return:
        """

    def predict(self, x_test):
        return [self._predict(xi) for xi in x_test]

    def _predict(self, x):
        if self.flag:  # 分类
            root = self.root
            split = root.split
            while split is not None:  # 遍历直到叶节点
                pass

    def _build(self, x, y):  # 回归过程中建立二叉树
        """
        递归建立二叉树,当节点纯度或者当前节点划分的样本数达到阈值即回溯
        :param x:
        :param y:
        :return:
        """

    # 计算当前划分情况的基尼值
    def get_gini(self, label):
        gini = 1
        for (ck, cnt) in zip(*np.unique(label, return_counts=True)):
            p = cnt / len(label)
            gini -= p * p
        return gini


    def get_continuous_gini(self, feat, label):
       """
       # 计算连续特征的基尼值
       :param feat:
       :param label:
       :return:
       """


    def floorPrint(self):
        """
        # 层序遍历建立的二叉树 队列+BFS
        :return:
        """

    # 以下为回归部分代码
    # 计算均方误差
    def _get_split_mse(self, x, y, idx, feature, split):
        """
        确定划分后的误差(MSE)
        :param x:
        :param y:
        :param idx:
        :param feature:
        :param split:
        :return:
        """

    def _choose_split(self, x, y, idx, feature):
        """
        确定最优划分点
        :param x:
        :param y:
        :param idx:
        :param feature:
        :return:
        """

    def _choose_feature(self, x, y, idx):
        # 共有m个特征
        # 遍历所有特征的最优划分点
        # 在所有特征的最优划分点中，再选取最优特征



    def _list_split(selfx,):
        """
        # 按照已求得的最优特征，最优划分点，划分出新的两部分数据的下标
        :param x:
        :param idxs:
        :param feature:
        :param split:
        :return:
        """

    def r_fit(self,):
        """
        回归

        """



def iris():
    data = load_iris()
    x = data['data']
    y = data['target']
    run(x, y, flag=1)


def wine():
    df = pd.read_excel('winequality_data.xlsx')
    X = df.iloc[:, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]].values  # 读取指定列的所有行数据：读取第0至10列所有数据
    X = list(X)
    X = np.array(X)
    Y = list(df.iloc[:, [11]].values)
    Y = np.array(Y)
    run(X, Y, flag=1)


def ice_cream():
    df = pd.read_excel('icecream_data.xlsx')
    X = df.iloc[:, [0]].values  # 读取指定列的所有行数据：读取第0列所有数据
    X = list(X)
    X = np.array(X)
    Y = list(df.iloc[:, [1]].values)
    Y = np.array(Y)
    run(X, Y, flag=0, max_depth=6)


def housing():
    df = pd.read_excel('housing_data.xlsx')
    X = df.iloc[:, [0, 1, 2, 3, 4]].values  # 读取指定列的所有行数据：读取第0~4列所有数据
    X = list(X)
    X = np.array(X)
    Y = list(df.iloc[:, [5]].values)
    Y = np.array(Y)
    x1, x2, y1, y2 = train_test_split(X, Y, test_size=0.05)
    x_train, x_test, y_train, y_test = train_test_split(x2, y2, test_size=0.2)
    clf = CART(flag=0, max_depth=10)
    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    print(f"层序遍历的结构为:")
    clf.floorPrint()
    print('预测分类:', y_pred)
    print('-------------------------')
    print('真实分类', y_test)
    print(f"剪枝前的R方为{r2_score(y_test, y_pred)}")


def run(X, Y, flag, max_depth=5):
    x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.8)
    if flag:
        x_train = pd.DataFrame(x_train, columns=[str(i) for i in range(X.shape[1])], index=None)
    clf = CART(flag=flag, max_depth=max_depth)
    clf.fit(x_train, y_train)
    y_pred = clf.predict(x_test)
    print(f"层序遍历的结构为:")
    clf.floorPrint()
    print('预测分类:', y_pred)
    print('-------------------------')
    print('真实分类', y_test)
    if flag:
        print(f"层序遍历的结构为:")
        clf.floorPrint()
        print(accuracy_score(y_test, y_pred))
    else:
        print(f"剪枝前的R方为{r2_score(y_test, y_pred)}")



if __name__ == '__main__':
    iris()
    # wine()
    # ice_cream()
    # housing()


    '''测试代码'''
    # n = np.array([3.9, 3.8, 3.7, 3.6, 3.5, 3.4, 3.2, 3.1])
    # m = np.extract(n <= 3.6, n)
    # print(np.where(n <= 3.6))
    # print(y[np.where(n <= 3.6)])
    # kind, cnt = np.unique(y, return_counts=True)
    # (k,c) = zip(*np.unique(y, return_counts = True))
    # print(np.unique(y, return_counts = True))
    # x = np.array([[1,2,3,4],
    #               [2,3,4,5],
    #               [3,4,5,6]])
    # y = np.array([1,2,3])
    # print(x[:,1])
    # ind = np.where(x[:,1] <= 3)
    # print(ind)
    # print(x[ind])
    # print(y[ind])


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
            self.pre_order(root.left, mk, pre, prename)
            self.pre_order(root.right, mk, pre, prename)
        else:
            # 如果是中间节点
            if root == None:
                return
            
            node_info = []
            edge_info = []# ['tail_name', 'head_name', 'label']
            if self.flag:   
                index = root.feature
            else:
                index = root.score
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
                if self.flag:
                    node_info.append("class "+str(index))
                else:
                    node_info.append(index)
            self.node.append(node_info)
            edge_info.append(prename)
            edge_info.append(name)
            edge_info.append(str(pre.split))
            self.edge.append(edge_info)
            pre = root
            prename = name
            self.pre_order(root.left, mk, pre, prename)
            self.pre_order(root.right, mk, pre, prename)