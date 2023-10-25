import random
from re import X
from sklearn.model_selection import train_test_split
from sklearn import datasets
import numpy as np
from logisticModel import LogisticModel

# 具体分类结果
x1_train = []
x2_train = []
x3_train = []
x1_test = []
x2_test = []
x3_test = []
Y1_train = []
Y2_train = []
Y3_train = []
Y1_test = []
Y2_test = []
Y3_test = []

def Classification(x_train, x_test, Y_train, Y_test):
    '''
    手动将数据集内各个样本分离，方便进行两两预测
    input:  输入即为train_test_split函数分离的输出
    '''
    for i in range(len(Y_train)):
        if(Y_train[i] == 0):
            Y1_train.append(Y_train[i])
            x1_train.append(list(x_train[i]))
        elif(Y_train[i] == 1):
            Y2_train.append(Y_train[i])
            x2_train.append(list(x_train[i]))
        else:
            Y3_train.append(Y_train[i])
            x3_train.append(list(x_train[i]))

    for i in range(len(Y_test)):
        if(Y_test[i] == 0):
            Y1_test.append(Y_test[i])
            x1_test.append(list(x_test[i]))
        elif(Y_test[i] == 1):
            Y2_test.append(Y_test[i])
            x2_test.append(list(x_test[i]))
        else:
            Y3_test.append(Y_test[i])
            x3_test.append(list(x_test[i]))

# 根据三个模型的预测情况，预测最终结果
def final_predict(pre12, pre13, pre23):
    '''
    input: 三个模型的预测值,数组,均为01序列
    output: 最终预测值,数组,为012序列
    '''
    pre = []
    for i in range(len(pre12)):
        # 记录abc类被预测的次数
        a = b = c = 0
        if(pre12[i] == 0):
            a += 1
        else:
            b += 1
        if(pre13[i] == 0):
            a += 1
            if(a == 2):
                pre.append(0)
                continue
        else:
            c += 1
        if(pre23[i] == 0):
            b += 1
            if(b == 2):
                pre.append(1)
                continue
        else:
            c += 1
            if(c == 2):
                pre.append(2)
                continue
        # 如果abc分别预测出1次
        pre.append(random.randint(0,2))
    return pre

#导入数据和标签
iris = datasets.load_iris()
iris_X = iris.data
iris_y = iris.target

#划分为训练集和测试集数据
x_train, x_test, Y_train, Y_test = train_test_split(iris_X, iris_y, test_size=0.3, random_state = 8)
Classification(x_train, x_test, Y_train, Y_test)

# 样本两两组合
x12_train = np.vstack((np.array(x1_train), np.array(x2_train)))
x13_train = np.vstack((np.array(x1_train), np.array(x3_train)))
x23_train = np.vstack((np.array(x2_train), np.array(x3_train)))
x12_test = np.vstack((np.array(x1_test), np.array(x2_test)))
x13_test = np.vstack((np.array(x1_test), np.array(x3_test)))
x23_test = np.vstack((np.array(x2_test), np.array(x3_test)))

y12_train = np.vstack((np.array(Y1_train).reshape(-1, 1), np.array(Y2_train).reshape(-1, 1)))
y13_train = np.vstack((np.array(Y1_train).reshape(-1, 1), np.array(Y3_train).reshape(-1, 1)))
y23_train = np.vstack((np.array(Y2_train).reshape(-1, 1), np.array(Y3_train).reshape(-1, 1)))
Y12_test = Y1_test + Y2_test
Y13_test = Y1_test + Y3_test
Y23_test = Y2_test + Y3_test

for i in range(len(y13_train)):
    if(y13_train[i][0] == 2):
        y13_train[i][0] = 1
for i in range(len(y23_train)):
    if(y23_train[i][0] == 1):
        y23_train[i][0] = 0
    else:
        y23_train[i][0] = 1

'''以上为数据预处理，接下来准备进行分类'''
# print(len(Y_train))

# 使用三个logistic模型
model12 = LogisticModel(x12_train, y12_train)
model13 = LogisticModel(x13_train, y13_train)
model23 = LogisticModel(x23_train, y23_train)

# 模型训练
model12.fit()
model13.fit()
model23.fit()

# 这里的Y_test并没有参与准确度运算，所以不用对他进行转换
pre12 = model12.predict(x_test, Y_test)
pre13 = model13.predict(x_test, Y_test)
pre23 = model23.predict(x_test, Y_test)

# 画图
# model12.model_show("ab")
# model13.model_show("ac")
# model23.model_show("bc")

pre = final_predict(pre12, pre13, pre23)

# 最终结果分析
model12.model_report_iris(pre, Y_test)