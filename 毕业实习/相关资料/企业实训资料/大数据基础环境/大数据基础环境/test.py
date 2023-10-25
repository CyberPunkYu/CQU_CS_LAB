#!/usr/bin/python
# -*- coding:UTF-8 -*-
# Filename: test.py
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


if __name__ == '__main__':
    spark = SparkSession.builder\
        .appName("test")\
        .master("spark://cat:7077")\
        .getOrCreate()
    sc = spark.sparkContext

    rdd = sc.textFile("hdfs://cat:9000/happy/wd.txt") \
        .flatMap(lambda line: line.split(" ")) \
        .map(lambda x:[x])

    df = rdd.toDF(["word"])

    df.createTempView("words")
    df2 = spark.sql("select word, count(*) as zishu from words group by word order by zishu DESC").show()


