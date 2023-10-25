# coding=utf-8
import random
 
#背包问题
# 物品 重量 价格
X = {
    1: [15, 15],
    2: [3, 7],
    3: [2, 10],
    4: [5, 5],
    5: [9, 8],
    6: [20, 17]}
 
#终止界限
FINISHED_LIMIT = 30
 
#重量界限
WEIGHT_LIMIT = 30
 
#染色体长度
CHROMOSOME_SIZE = 6
 
#遴选次数
SELECT_NUMBER = 4
 
max_last = 0
diff_last = 10000
 
#判断退出
def is_finished(fitnesses):
    global max_last
    global diff_last
    max_current = 0
    for v in fitnesses:
        if v[1] > max_current:
            max_current = v[1]
    print('max_current:',max_current)   # 得到当前最大的价值
    diff = max_current - max_last # 价值差，也就是适应度的改变的大小
    # 这里判断连续两代的改变量如果都小于5，则停止迭代
    if diff < FINISHED_LIMIT and diff_last < FINISHED_LIMIT: 
        return True
    else:
        diff_last = diff
        max_last = max_current
        return False
 
#初始染色体样态
def init():
    chromosome_state1 = '100110'
    chromosome_state2 = '001110'
    chromosome_state3 = '010101'
    chromosome_state4 = '011000'
    chromosome_states = [chromosome_state1,
                         chromosome_state2,
                         chromosome_state3,
                         chromosome_state4]
    return chromosome_states
 
 
#计算适应度
def fitness(chromosome_states):
    fitnesses = []
    for chromosome_state in chromosome_states: # 遍历所有的染色体
        value_sum = 0  # 物品重量
        weight_sum = 0 # 物品价值
        # 将一个可遍历的数据对象组合为一个索引序列，同时列出数据和数据下标
        for i, v in enumerate(chromosome_state): 
            # 对染色体中的1，即存在的物品体重和价格求和
            if int(v) == 1:
                weight_sum += X[i + 1][0] 
                value_sum += X[i + 1][1]
        fitnesses.append([value_sum, weight_sum])
    return fitnesses
 
 
#筛选
def filter(chromosome_states, fitnesses):
    #重量大于30的被淘汰
    index = len(fitnesses) - 1
    while index >= 0:
        index -= 1
        if fitnesses[index][1] > WEIGHT_LIMIT:
            chromosome_states.pop(index) # 弹出不符合条件的染色体
            fitnesses.pop(index)  # 弹出不符合条件的适应度
    #print chromosome_states,'\n',fitnesses
 
    #遴选
    selected_index = [0] * len(chromosome_states) # 如果[0]*3得到的是[0,0,0]
    for i in range(SELECT_NUMBER):
        # 随机选择染色体，然后得到相应的索引
        j = chromosome_states.index(random.choice(chromosome_states)) 
        selected_index[j] += 1
    return selected_index
 
 
# 交叉产生下一代
def crossover(chromosome_states, selected_index):
    chromosome_states_new = []
    index = len(chromosome_states) - 1
    #print 'index:',index
    while index >= 0: # 遍历完所有的染色体组的染色体（其中下标-1代表最后一个染色体的索引）
        print ('index:',index)
        index -= 1
        chromosome_state = chromosome_states.pop(index)
        print ('chromosome_states_3:',chromosome_states )# 弹出后的染色体组
        print ('chromosome_state:',chromosome_state ) # 弹出的染色体
        for i in range(selected_index[index]): 
            chromosome_state_x = random.choice(chromosome_states) # 随机选择一个染色体
            print ('chromosome_state_x:',chromosome_state_x)
            pos = random.choice(range(1, CHROMOSOME_SIZE - 1))  # 随机[1, 2, 3, 4]其中的一个数
            print ('pos:',pos)
            chromosome_states_new.append(chromosome_state[:pos] + chromosome_state_x[pos:])
            print ('chromosome_states_new:',chromosome_states_new)
        chromosome_states.insert(index, chromosome_state) # 恢复原染色体组
        print ('chromosome_states_4:', chromosome_states)
    return chromosome_states_new # 返回得到的新的染色体组
 
 
if __name__ == '__main__':
    # 初始群体
    chromosome_states = init() # 是全局的
    print ('chromosome_states:',chromosome_states)
    n = 100  # 迭代次数
    while n > 0:
        n -= 1
        #适应度计算
        fitnesses = fitness(chromosome_states)
        #print 'fitnesses:',fitnesses
        if is_finished(fitnesses):
            break # 如果符合条件，立刻停止循环
        print ('1:', fitnesses)
        #遴选
        selected_index = filter(chromosome_states, fitnesses)
        print ('2:', selected_index)
        print ('chromosome_states_2:',chromosome_states)
        #产生下一代
        chromosome_states = crossover(chromosome_states, selected_index)
        print ('3:', chromosome_states)
        print (str(n)+'..................................' ) # 迭代次数
    fitnesses = fitness(chromosome_states)
    print ('fitnesses:',fitnesses)
    print (chromosome_states)
