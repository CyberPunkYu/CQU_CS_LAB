﻿from pyspark import SparkConf, SparkContext
from visualize import visualize
import jieba

SRCPATH = '/home/hadoop/Experiment/Ex2_WordCount/src/'
# SparkContext的初始化需要一个SparkConf对象，SparkConf包含了Spark集群配置的各种参数。
conf = SparkConf().setAppName("ex2").setMaster("spark://master:7077")
conf = SparkConf().setAppName("ex2").setMaster("local")
# 任何Spark程序都是SparkContext开始的,初始化后，就可以使用SparkContext对象所包含的各种方法来创建和操作RDD和共享变量。
sc = SparkContext(conf=conf)
# 读取`stop_words.txt` 所有停用词，返回一个 `python List`
def getStopWords(stopWords_filePath):
    stopwords = [line.strip() for line in open(stopWords_filePath, 'r', encoding='utf-8').readlines()]
    return stopwords
# 将所有答案合并，并进行分词，返回一个 `python List`
def jiebaCut(answers_filePath):
    """
    结巴分词
    :param answers_filePath: answers.txt路径
    :return:
    """
    # 读取answers.txt
    # answersRdd每一个元素对应answers.txt每一行
    answersRdd = sc.textFile(answers_filePath) 
    # 利用SpardRDD reduce()函数,合并所有回答
    str = answersRdd.reduce(lambda a, b: a + b)
    # jieba分词
    words_list = jieba.lcut(str)
    return words_list
# 核心函数，利用`SparkRdd` 完成词频统计
def wordcount(isvisualize=False):
    """
    对所有答案进行
    :param visualize: 是否进行可视化
    :return: 将序排序结果RDD
    """
    # 读取停用词表
    stopwords = getStopWords(SRCPATH + 'stop_words.txt')
    # 结巴分词
    words_list = jiebaCut("file://" + SRCPATH + "answers.txt")
    # 词频统计
    wordsRdd = sc.parallelize(words_list)
    # wordcount：去除停用词等同时对最后结果按词频进行排序
    # 完成SparkRDD操作进行词频统计
    #      1.filter函数分别进行停用词过滤、去除长度<=1的词汇
    #      2.map进行映射，如['a','b','a'] --> [('a',1),('b',1),('a',1)]
    #      3.reduceByKey相同key进行合并 [('a',2),('b',1)]
    #      4.sortBy进行排序，注意应该是降序排序
    resRdd = wordsRdd.filter(lambda word:len(word) > 1) \
                     .filter(lambda word:word not in stopwords)\
                     .map(lambda word:(word , 1)) \
                     .reduceByKey(lambda a , b:a + b) \
                     .sortBy(ascending=False, numPartitions=None, keyfunc=lambda x: x[1]) \
    # 可视化展示
    if isvisualize:
        v = visualize()
        # 饼状图可视化
        pieDic = v.rdd2dic(resRdd,10)
        v.drawPie(pieDic)
        # 词云可视化
        wwDic = v.rdd2dic(resRdd,50)
        v.drawWorcCloud(wwDic)
        # 柱状图可视化
        barDic = v.rdd2dic(resRdd,10)
        # v.drawBar(barDic)
        # 折线图可视化
        # v.drawLine(barDic)

    return resRdd
if __name__ == '__main__':
    # 进行词频统计并可视化
    resRdd = wordcount(isvisualize=True)
    print(resRdd.take(10)) # 查看前10个