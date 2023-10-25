import numpy as np
import matplotlib.pyplot as plt
import random

CITIES = [(116.46,39.92),(117.2,39.13),(121.48,31.22),(106.54,29.59),(91.11,29.97),   #十座城市的经纬度
        (87.98,43.77),(106.27,38.47),(111.65,40.82),(108.33,22.84),(126.63,45.75)]

X = [116.46, 117.2, 121.48, 106.54, 91.11, 87.98, 106.27, 111.65, 108.33, 126.63] #纬度
Y = [39.92, 39.13, 31.22, 29.59, 29.97, 43.77, 38.47, 40.82, 22.84, 45.75] #经度

CITY_NUM = 10   #城市数量

'''
由于随机生成序列过于随机，种群中各个个体的适应度相差太大，导致轮盘赌操作中
选择某个个体的概率很容易大于99%而无法选择其他个体，导致轮盘赌死循环。并且随机序列
在实现中难以调试，所以固定初始种群
'''
s1 = [0,1,2,3,4,5,6,7,8,9,0]
s2 = [0,5,4,6,9,2,1,7,8,3,0]
s3 = [0,1,2,3,7,8,9,4,5,6,0]
s4 = [0,1,2,3,4,5,7,6,8,9,0]
POPULATION = [s1,s2,s3,s4]

PC = 1    #交叉率PC = 1，交叉必然发生

PM = 0.2    #变异率

def getDistance(a , b):   #计算两点之间的距离
    a = np.array(a)
    b = np.array(b)
    c = a - b
    distance = np.sqrt(np.sum(c * c))
    return distance

def cityDistance():    #获得距离矩阵
    mat = np.zeros([CITY_NUM , CITY_NUM])
    for i in range(CITY_NUM - 1):
        for j in range(i + 1 , CITY_NUM):
            d = getDistance(CITIES[i] , CITIES[j])
            mat[i , j] = d
    for i in range(CITY_NUM):
        mat[:,i] = mat[i,:]     #对称矩阵
    return mat

CITY_MAP = cityDistance()   #距离矩阵

MIN_ANS = []    #全局最优解

def cost(s):    #计算适应度函数
    cost = 0
    for i in range(CITY_NUM):
        cost += CITY_MAP[s[i] , s[(i + 1) % CITY_NUM]]  #最终回到原点
    return -cost    #距离越近，适应度越高

def init(size):   #随机生成种群
    population = []
    for i in range(size):
        race = [0] * (CITY_NUM + 1) #最终会经过11点，起点和终点为同一个点
        for j in range(1 , CITY_NUM):#初始点为0，此后将1-9随机放入race
            tmp = np.random.randint(1 , CITY_NUM)
            while race[tmp] > 0:
                tmp = np.random.randint(1 , CITY_NUM)
            race[tmp] = j
        population.append(race)
    return population

# POPULATION = init(4)    #初始种群为随机生成的四个个体

def crossOver(p1 , p2): #交叉
    a = np.array(p1).copy()
    b = np.array(p2).copy()

    begin = random.randint(1,9) #1-9之间的随机数，由于第0位和第10位都是0
    end = random.randint(1,9)
    # begin = 2
    # end = 5
    if begin > end: # swap if end < begin 
        (begin , end) = (end , begin)
    # print(begin,end)
    cross_map = {} #建立交叉的映射关系，PMX保证基因仅出现一次

    for i in range(begin , end + 1):    #初步建立映射
        if a[i] not in cross_map.keys():
            cross_map[a[i]] = []
        if b[i] not in cross_map.keys():
            cross_map[b[i]] = []
        #a, b中交叉元素互相映射
        cross_map[a[i]].append(b[i])
        cross_map[b[i]].append(a[i])
    
    c1 = a.copy()#孩子的染色体
    c2 = b.copy()
    c1[begin : end + 1] = b[begin : end + 1]#交换两组基因的位置
    c2[begin : end + 1] = a[begin : end + 1]

    for i in range(11):
        if(i < begin or i > end):  #对所有非交换序列遍历
            mark = 0
            tmp = 0
            while(c1[i] in b[begin : end + 1]): #如果该序列中存在重复基因，则替换为该基因的映射
                if(mark == 3):
                    mark = 0
                    tmp += 1   #如果该基因映射多个基因，则重复替换失败后，替换下一个
                # print(c1[i],cross_map[c1[i]][tmp])
                c1[i] = cross_map[c1[i]][tmp]
                mark += 1
            mark = 0
            tmp = 0
            while(c2[i] in a[begin : end + 1]):
                if(mark == 3):
                    mark = 0
                    tmp += 1
                # print(c2[i],cross_map[c2[i]][tmp])
                c2[i] = cross_map[c2[i]][tmp]
                mark += 1
        else:
            continue
    
    # print(c1)
    # print(c2)
    # print(cross_map)
    return c1,c2
# crossOver((0,1,2,3,4,5,6,7,8,9,0),(0,3,5,8,1,7,4,2,6,9,0))
# crossOver((0,1,3,4,5,6,8,7,9,2,0),(0,1,4,5,6,7,8,3,2,9,0))

def Variation(s):   #变异
    # print(s)
    c = range(1,10) #第0位和第11位固定为0
    index1,index2 = random.sample(c,2)
    # print(index1,index2)
    (s[index1] , s[index2]) = (s[index2] , s[index1])   #随机交换染色体中的基因
    # print(s)
    return s
# Variation(POPULATION[0])

def TakeThird(elem):    #按适应度从大到小，排序时作为sort的key参数
    return elem[2]

def cacAdap(population):#计算每一个个体的适应度，选择概率
    adap = []    # adap n*4,n为行数，每行包括：个体下标,适应度,选择概率,累积概率
    psum = 0
    i = 0
    for p in population:
        cost_p = np.exp(cost(p))    #将适应度规范到0-1区间
        psum += cost_p 
        adap.append([i])    #添加个体
        adap[i].append(cost_p)  #添加适应度
        i += 1
    for p in adap:  #添加选择概率和累积概率
        p.append(p[1] / psum) #归一化
        p.append(p[2])
    # print(adap)
    adap.sort(key = TakeThird , reverse = True)

    n = len(adap)   # 计算累计概率
    for i in range(1,n):
        adap[i][3] += adap[i-1][3]
    # print(adap)
    return adap
# cacAdap(POPULATION)

def select(adap):    #轮盘赌法
    chose = set()
    epochs = 20 #选择次数
    n = len(adap)
    for a in range(epochs):
        p = random.random()
        if adap[0][3] >= p: #如果随机概率p落在某个个体的概率区间，则选择相应的个体
            chose.add(adap[0][0])
        else:
            for i in range(1 , n):
                if adap[i][3] >= p and adap[i-1][3] < p:
                    chose.add(adap[i][0])
                    break
    while(len(set(chose)) <2):#避免出现选择少于两个的情况
        # print('chosing...length %d'%len(set(chose)))
        chose = select(adap)
    chose = list(chose)
    # print(chose)
    return chose
# adat = cacAdap(POPULATION)
# select(adat)

def Copy(chose , population):
    parent_population = []
    chose_num = len(chose)
    sample_times = chose_num//2
    for i in range(sample_times):
        index1,index2 = random.sample(chose,2)
        # print (index1,index2)
        parent1 = population[index1]# 参与复制的父结点
        parent2 = population[index2]
        chose.remove(index1)# 这两个父结点已经复制，后面就不要参与了
        chose.remove(index2)
        parent_population.append(parent1)
        parent_population.append(parent2)
    return parent_population
# print(parent_population)
# adat = cacAdap(POPULATION)
# print(POPULATION)
# chose1 = select(adat)
# print(Copy(chose1,POPULATION))

def Cross_Variation(chose , population): #将轮盘赌选择的个体参与交叉变异操作
    child_population = []   #经交叉变异产生的孩子
    chose_num = len(chose)
    sample_times = chose_num//2
    # print(sample_times)
    for i in range(sample_times):
        index1,index2 = random.sample(chose,2)
        # print (index1,index2)
        parent1 = population[index1]# 参与交叉的父结点
        parent2 = population[index2]
        chose.remove(index1) # 这两个父结点已经交叉，后面就不要参与了
        chose.remove(index2)
        
        p = random.random()
        if PC >= p:
            child1,child2 = crossOver(parent1 , parent2)
            # print (child1,child2)
            p1 = random.random()
            p2 = random.random()
            if PM > p1:
                child1 = Variation(child1)
            if PM > p2:
                child2 = Variation(child2)
            child_population.append(list(child1))
            child_population.append(list(child2))
    return child_population
# adat = cacAdap(POPULATION)
# chose2 = select(adat)
# print(Cross_Variation(chose2,POPULATION))

def GA(population): #一次遗传过程
    # print(population)
    adap = cacAdap(population)
    chose1 = select(adap) # 选择操作
    parent_population = Copy(chose1 , population)
    chose2 = select(adap)
    child_population = Cross_Variation(chose2 , population)
    new_population = parent_population + child_population   #将复制的前一代与交叉变异的后一代结合得到新一代
    # print(new_population)
    return new_population
# GA(POPULATION)

def findMin(population):
    loss = []
    epochs = 101 #遗传次数
    i = 0
    while i < epochs:
        adap = []
        for p in population:    #计算适应度
            icost = cost(p)
            adap.append(icost)
        population = GA(population) #使用遗传算法更新种群
        min_cost = max(adap)    #最大适应度及最小代价
        if i % 10 == 0:
            print('epoch %d: loss = %.2f'%(i,-min_cost))
        loss.append([i,-min_cost])
        i += 1
        if i == epochs:# 输出最优解
            p_len = len(population)
            for index in range(p_len):
                if adap[index] == min_cost:
                    print('最优路径:')
                    print(population[index])
                    MIN_ANS = population[index]
                    print('代价大小:')
                    print(-min_cost)
                    break
    #画图部分
    #损失函数
    loss = np.array(loss)
    plt.subplot(1,2,1)
    plt.xlabel('generation' , fontsize = 16)
    plt.ylabel('loss' , fontsize = 16)
    plt.plot(loss[:,0] , loss[:,1])
    plt.title('GA')

    #路径图
    X = []  #按照最优路径排序的纬度
    Y = []  #按照最优路径排序的经度
    for i in MIN_ANS:
        X.append(CITIES[i][0])
        Y.append(CITIES[i][1])
    # print(Y)
    plt.subplot(1,2,2)
    plt.cla()
    plt.scatter(X, Y, s = 10, c='k')  #画散点图
    n = MIN_ANS[0:10]   #对散点编号，编号顺序为最优路径的前十位
    for i, label in enumerate(n):
        plt.annotate(label, (X[i] , Y[i]))
    plt.plot(X , Y) #连接散点
    plt.xlabel('latitude',fontsize = 16)
    plt.ylabel('longitude',fontsize = 16)
    plt.title('map')

    plt.show()

findMin(POPULATION)