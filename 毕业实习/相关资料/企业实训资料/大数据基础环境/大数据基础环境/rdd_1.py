#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Filename: rdd_1.py

from pyspark import SparkConf, SparkContext

#构建Spark接口对象 SparkConf
#设置运行模式
#调用算子处理数据
#关闭进程


if __name__ == '__main__':
    conf = SparkConf().setMaster("spark://cat:7077").setAppName("rdd-1")
    # conf = SparkConf().setMaster("local[*]").setAppName("rdd-1")
    sc = SparkContext(conf=conf)

    def my_map():
        data = [1,2,3,4,5]
        rdd1 = sc.parallelize(data)
        #rdd2 = rdd1.map(lambda x:x*2)
        rdd2 = rdd1.map(lambda x:x*2)
        #rdd3 = rdd2.mapPartitions(lambda x:x*2)
        print(rdd2.collect())

    def my_map2():
        a = sc.parallelize(["dog", "lion", "cat", "tiger"])
        b = a.map(lambda x:(x,1))  #(dog,1)
        print(b.collect())

    def my_filter():
        data = [1,2,3,4,5]
        rdd1 = sc.parallelize(data)
        mapRdd = rdd1.map(lambda x:x*2).filter(lambda a:a>5)
        print(mapRdd.collect())

        # print(sc.parallelize(data).map(lambda x:x*2).filter(lambda x:x>5).collect())

    def my_flatMap():
        data = ["hello spark", "hello world", "hello spark"]
        rdd = sc.parallelize(data)
        print(rdd.flatMap(lambda line:line.split(" ")).collect())

    def my_groupByKey():
        data = ["hello spark", "hello world", "hello spark"]
        rdd = sc.parallelize(data)
        print(rdd.flatMap(lambda line:line.split(" ")).map(lambda x:(x, 1)).groupByKey().collect())
        print(rdd.flatMap(lambda line:line.split(" ")).map(lambda x:(x, 1)).groupByKey().map(lambda x:{x[0]:list(x[1])}).collect())

    def my_reduceByKey():
        data = ["hello spark", "hello world", "hello spark"]
        rdd = sc.parallelize(data)
        mapRdd = rdd.flatMap(lambda line:line.split(" ")).map(lambda x:(x,1))
        reduceRdd = mapRdd.reduceByKey(lambda a,b:a+b).collect()
        print(reduceRdd)

        #print(sc.parallelize(data).flatMap(lambda line:line.split(" ")).map(lambda x:(x,1)).reduceByKey(lambda a,b:a+b).collect())

    def my_union():
        a = sc.parallelize([1, 2, 3, 4, 5])
        b = sc.parallelize([5, 4, 6, 7, 8])
        print(a.union(b).collect())
        print(a.zip(b).collect())

    def my_distinct():
        a = sc.parallelize([1, 2, 3, 4, 5])
        b = sc.parallelize([5, 4, 6, 7])
        print(a.union(b).distinct().collect())

    def my_intersection():
        a = sc.parallelize([1, 2, 3, 4, 5])
        b = sc.parallelize([5, 4, 6, 7])
        print(a.intersection(b).collect())

    def my_join():
        #只用于二元元祖-------kv键值对
        #关联条件 指定为key
        a = sc.parallelize([("A", "a1"), ("C", "c1"), ("D", "d1"), ("F", "f1"), ("F", "f2")])
        b = sc.parallelize([("A", "a2"), ("C", "c2"), ("C", "c3"), ("E", "e1")])
        print(a.join(b).collect())
        print(a.leftOuterJoin(b).collect())
        print(a.rightOuterJoin(b).collect())
        print(a.fullOuterJoin(b).collect())

    def my_sortBy():
        data = [('a',1), ('a',3), ('a',7), ('b',1), ('a',5), ('k',1)]
        rdd1 = sc.parallelize(data)
        #参数1：排序依据  参数2：true升序   参数3：排序分区
        #分区数：1为全局   其余更具业务调整
        rdd2 = rdd1.sortBy(lambda x: x[1], ascending=False, numPartitions=3).collect()
        rdd3 = rdd1.sortBy(lambda x: x[0], ascending=False, numPartitions=3).collect()
        print(rdd2)
        print(rdd3)

    def my_sortByKey():
        data = ["hello spark", "hello world", "hello spark"]
        print(sc.parallelize(data).flatMap(lambda line:line.split(" ")).map(lambda x:(x,1))\
              .reduceByKey(lambda a,b:a+b)\
              .map(lambda x:(x[1],x[0]))\
              .sortByKey(False)\
              .map(lambda x:(x[1],x[0]))\
              .collect())

    def my_action():
        data = [1,2,3,4,5,6,7,8,9,10]
        rdd = sc.parallelize(data)
        print(rdd.collect())
        print(rdd.count())
        print(rdd.take(3))
        print(rdd.max())
        print(rdd.sum())

        print(rdd.reduce(lambda x,y:x+y))

        print(rdd.foreach(lambda x:print(x)))


    my_sortBy()
    sc.stop()