# #TSP  using GA
import csv
import numpy as np
import random
import math
#

# load file
def load_file(filename):
    #filename='C:\youhua_code\GA\cities.csv'
    with open(filename) as f:
        reader=csv.reader(f)
        header_row = next(reader)
        cities=[]
        for row in reader:
           longti=float(row[1])
           lati=float(row[2])
           cities.append([longti,lati])
    return cities


# generate initial population
def generate_population(city_num,n):
    Sindex = np.arange(city_num)
    Cindex=np.zeros((n,city_num))
    for k in range(n):
        Cindex[k,:]=Sindex
        np.random.shuffle(Sindex)


    return Cindex

#define aim function
def Cal_distance(city,Cindex):# Calculate the distance between cities in one route
    
    d=0
    for k in range(city.shape[0]-1):
        
        s=int(Cindex[k])
        e=int(Cindex[k+1])
        d+=math.sqrt(np.sum(np.power(city[e,:]-city[s,:],2)))
    d+=math.sqrt(np.sum(np.power(city[e,:]-city[int(Cindex[0]),:],2)))
    return d

#select parents
def Select(Population,n):
    dist=[]
    print('calculate the distance...')
    for Sel_index in Population:
        print(Sel_index)
        
        dist1=Cal_distance(np.array(cities),Sel_index)
        dist.append(dist1)

    graded =[[dist[x], x] for x in range(n)]
    retain_rate = 0.5
    random_select_rate = 0.5
    graded = [x[1] for x in sorted(graded)]
    retain_length = int(len(graded) * retain_rate)
    parents = graded[:retain_length]
    for chromosome in graded[retain_length:]:
        if random.random() < random_select_rate:
            parents.append(chromosome)
    return parents



filename='C:\youhua_code\GA\cities.csv'
cities=load_file(filename)
city_num=len(cities)
n=200
Population=generate_population(city_num,n)
itter=10
times=0
while times<itter:
     times+=1
     parents=Select(Population,n)

#
#
# #cross
# def crossover(parents):
#     #生成子代的个数,以此保证种群稳定
#     target_count=n-len(parents)
#     #孩子列表
#     children=[]
#     while len(children)<target_count:
#         male_index = random.randint(0, len(parents) - 1)
#         female_index = random.randint(0, len(parents) - 1)
#         if male_index!=female_index:
#             male=parents[male_index]
#             female=parents[female_index]
#
#             left=random.randint(0,len(male)-2)
#             right=random.randint(left+1,len(male)-1)
#
#             #交叉片段
#             gene1=male[left:right]
#             gene2=female[left:right]
#
#             child1_c=male[right:]+male[:right]
#             child2_c=female[right:]+female[:right]
#             child1=child1_c.copy()
#             child2= child2_c.copy()
#
#             for o in gene2:
#                 child1_c.remove(o)
#
#             for o in gene1:
#                 child2_c.remove(o)
#
#             child1[left:right]=gene2
#             child2[left:right]=gene1
#
#             child1[right:]=child1_c[0:len(child1)-right]
#             child1[:left] = child1_c[len(child1) - right:]
#
#             child2[right:] = child2_c[0:len(child1) - right]
#             child2[:left] = child2_c[len(child1) - right:]
#
#             children.append(child1)
#             children.append(child2)
#
#     return children
#
#
# def mutation(children):
#     for i in range(len(children)):
#         if random.random() < mutation_rate:
#             child=children[i]
#             r1,r2=random.sample(range(city_num),2)
#             child[r1],child[r2]=child[r2],child[r1]
#             children[i]=child
#
#
#
# def reverse(children):
#      for i in range(len(children)):
#         if random.random() < reverse_rate:
#             child=children[i]
#             r1=random.randint(0,city_num)
#             child1=child[r1,:]
#             child1.reverse()
#             child[r1,:]=child1
#             childeren[i]=child
#
# def get_result(Cindex):
#     return
#
# #main program
# n=200
#
# retain_rate=0.2
# random_select_rate=0.5
# reverse_rate=0.1
# itter=10
#
#
# while i<itter:
#     parents=Select(Population)
#     children=crossover(parents)
#     #变异操作
#     mutation(children)
#     Cindex=parents+children
#
#
