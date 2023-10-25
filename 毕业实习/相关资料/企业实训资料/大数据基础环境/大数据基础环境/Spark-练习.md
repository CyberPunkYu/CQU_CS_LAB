## 职位投递分析

### 数据

   id      			地区    		职位id    	IP地址 			 日期

```
uid56231 shanghai jobid53 192.168.54.90 2020-10-15
uid56231 shanghai jobid32 192.168.54.90 2020-10-15
uid56231 shanghai jobid32 192.168.54.90 2020-10-15
uid56231 shanghai jobid20 192.168.54.90 2020-10-15
uid56231 shanghai jobid73 192.168.54.90 2020-10-15
uid56231 shanghai jobid34 192.168.54.90 2020-10-15
uid56231 shanghai jobid73 192.168.54.90 2020-10-15
uid09796 beijing jobid74 192.168.74.167 2020-10-15
uid09796 beijing jobid74 192.168.74.167 2020-10-15
uid09796 beijing jobid52 192.168.74.167 2020-10-15
uid09796 beijing jobid33 192.168.74.167 2020-10-15
uid09796 beijing jobid11 192.168.74.167 2020-10-15
```

1、统计每个职位投递总次数 & 投递总人数

```python
from pyspark import SparkConf, SparkContext
if __name__ == '__main__':
    conf = SparkConf().setMaster("spark://Pspark:7077").setAppName("job01")
    sc = SparkContext(conf=conf)
    lines=sc.textFile("hdfs://Pspark:9000/data")

#    uid56231 shanghai jobid53 192.168.54.90 2020-10-15
# 计算每个职位的投递总次数


# 计算每个职位的投递总人数
    #(uid56231&jobid53, 1)
    # map
  

    sc.stop()
```

2、统计指定地区的投递的总人数 & 总次数

```python
#!/usr/bin/python
# -*- coding:UTF-8 -*-
# @File : job_stu.py
from pyspark import SparkConf, SparkContext
if __name__ == '__main__':
    conf = SparkConf().setMaster("spark://cat:7077").setAppName("job01")
    sc = SparkContext(conf=conf)
    lines=sc.textFile("hdfs://cat:9000/data")
    # 统计每个职位投递总次数 & 投递总人数
    # 职位id
    lines_sum = lines.map(lambda line: (line.split(" ")[2], 1)) \
        .reduceByKey(lambda v1, v2: v1 + v2) \
        .sortBy(lambda x: x[1], False)\
        .collect()
    print("每个职位投递总次数:", lines_sum)

    # 每个职位投递总人数
    lines_num = lines.map(lambda line: line.split(" ")[0] + "&" + line.split(" ")[2]) \
        .distinct() \
        .map(lambda line: (line.split("&")[1], 1))\
        .reduceByKey(lambda v1, v2: v1 + v2) \
        .sortBy(lambda x: x[1], False)\
        .collect()
    print("每个职位投递总人数:", lines_num)

    # 统计指定地区的投递的总人数 & 总次数
    lines_count = lines.filter(lambda line: line.split(" ")[1] == "beijing")\
        .map(lambda line:(line.split(" ")[2],1)) \
        .reduceByKey(lambda v1, v2: v1 + v2) \
        .sortBy(lambda x: x[1], False) \
        .collect()
    print("北京地区的岗位投递的总人数:", lines_count)

    #
    lines_people = lines.filter(lambda line: line.split(" ")[1] == "beijing") \
        .map(lambda line: line.split(" ")[0] + "&" + line.split(" ")[2]) \
        .distinct() \
        .map(lambda line: (line.split("&")[1], 1)) \
        .reduceByKey(lambda v1, v2: v1 + v2) \
        .sortBy(lambda x: x[1], False) \
        .collect()
    print("北京地区的岗位投递的总次数:", lines_people)
```

3、统计每个地区投递次数最多职位top3

