# 1. RDD详解

## 1.1 为什么需要RDD

​	没有RDD之前：

​		1.MR:只提供了map和reduce的API,而且编写麻烦,运行效率低。

​		2.使用Scala/Java的本地集合:但是只能完成本地单机版的,如果要实现分布式的,难度较大。

​	所以需要有一个**分布式的数据抽象**,也就是用该抽象,可以表示分布式的集合,那么基于这个分布式集合进行操作,就可以很方便的完成分布式的WordCount!（该分布式集合底层应该将实现的细节封装好,提供简单易用的API）**在此背景之下,RDD就诞生了。**

​	Hadoop的MapReduce是一种基于数据集的工作模式，面向数据，这种工作模式一般是从存储上加载数据集，然后操作数据集，最后写入物理存储设备。数据更多面临的是一次性处理。

​	MR的这种方式对数据领域两种常见的操作不是很高效。**第一种是迭代式的算法**。比如机器学习中**ALS、凸优化**梯度下降等。这些都需要基于数据集或者数据集的衍生数据反复查询反复操作。MR这种模式不太合适，即使多MR串行处理，性能和时间也是一个问题。数据的共享依赖于磁盘。另外一种是交互式数据挖掘，MR显然不擅长。

![image-20230525150343847](.\1-SparkBase-Core.assets\image-20230525150343847.png)



![image-20230525150413011](.\1-SparkBase-Core.assets\image-20230525150413011.png)

​	我们需要一个效率非常快，且能够支持迭代计算和有效数据共享的模型，Spark应运而生。RDD是基于工作集的工作模式，更多的是面向工作流。

​	**但是无论是MR还是RDD都应该具有类似位置感知、容错和负载均衡等特性。**

​	总结：

​	RDD将Spark的底层的细节都隐藏起来了(自动容错、位置感知、任务调度执行，失败重试…)，让开发者可以像操作本地集合一样以函数式编程的方式操作RDD这个分布式数据集进行各种并行计算。

## 1.2 什么是RDD

​	RDD提供了一个抽象的数据模型，让我们不必担心底层数据的**分布式特性**，只需将具体的应用逻辑表达为**一系列转换操作(函数)**，不同RDD之间的转换操作之间还可以形成依赖关系，进而实现管道化，从而避免了中间结果的存储，大大降低了数据复制、磁盘IO和序列化开销，并且还提供了更多的API。（map/reduec/filter/groupBy..）

![image-20230525151348919](.\1-SparkBase-Core.assets\image-20230525151348919.png)


## 1.3 RDD 定义

​	RDD（Resilient Distributed Dataset）叫做弹性分布式数据集，是Spark中最基本的数据抽象，代表一个**不可变、可分区、里面的元素可并行计算的集合**。

​	**A Resilient Distributed Dataset (RDD), the basic abstraction in Spark. Represents an immutable, partitioned collection of elements that can be operated on in parallel.**

​	· **Resilient**：RDD中的数据可以存储在内存中或者磁盘中；

​	· **Datase**t：一个数据集合，用于存放数据的；

​	· **Resilient**：RDD中的数据可以存储在内存中或者磁盘中。

![image-20230525170917404](.\1-SparkBase-Core.assets\image-20230525170917404.png)

​	可以认为RDD是分布式的列表List或数组Array，抽象的数据结构，RDD是一个抽象类Abstract Class和泛型Generic Type。

<img src=".\1-SparkBase-Core.assets\image-20230525172101799.png" alt="image-20230525172101799" style="zoom:60%;" />

## 1.4 RDD的5大特性

### 1.4.1 RDD五大特性

​	RDD 数据结构内部有五个特性，前三个特征每个RDD都具备的，后两个特征可选的：

<img src=".\1-SparkBase-Core.assets\image-20230525175720711.png" alt="image-20230525175720711" style="zoom:50%;" />



​	第一个：**A list of partitions** ：

​		一组分片(Partition)/一个分区(Partition)列表，即数据集的基本组成单位；

​		对于RDD来说，每个分片都会被一个计算任务处理，分片数决定并行度；

​		用户可以在创建RDD时指定RDD的分片个数，如果没有指定，那么就会采用默认值；

​	第二个：**A function for computing each split** ：

​		一个函数会被作用在每一个分区；

​		Spark中RDD的计算是以分片为单位的，compute函数会被作用到每个分区上；

​	第三个：**A list of dependencies on other RDDs**：

​		一个RDD会依赖于其他多个RDD；

​		RDD的每次转换都会生成一个新的RDD，所以RDD之间就会形成类似于流水线一样的前后依赖关系。在部分分区数据丢失时，Spark可	以通过这个依赖关系重新计算丢失的分区数据，而不是对RDD的所有分区进行重新计算（Spark的容错机制）；

​	第四个：**Optionally, a Partitioner for key-value RDDs (e.g. to say that the RDD is hash-partitioned)**：

​		可选项,对于KeyValue类型的RDD会有一个Partitioner，即RDD的分区函数；

​		当前Spark中实现了两种类型的分区函数，一个是基于哈希的HashPartitioner，另外一个是基于范围的RangePartitioner；

​		只有对于于key-value的RDD，才会有Partitioner，非key-value的RDD的Parititioner的值是None；

​		Partitioner函数不但决定了RDD本身的分片数量，也决定了parent RDD Shuffle输出时的分片数量。

​	第五个：**Optionally, a list of preferred locations to compute each split on (e.g. block locations for an HDFS file)**：

​		可选项，一个列表，存储存取每个Partition的优先位置(preferred location)；

​		对于一个HDFS文件来说，这个列表保存的就是每个Partition所在的块的位置；

​		按照"移动数据不如移动计算"的理念，Spark在进行任务调度的时候，会尽可能选择那些存有数据的worker节点来进行任务计算。（数	据本地性）

<img src=".\1-SparkBase-Core.assets\image-20230525180241487.png" alt="image-20230525180241487" style="zoom:67%;" />	

​	**RDD 是一个数据集的表示，不仅表示了数据集，还表示了这个数据集从哪来、如何计算，主要属性包括五个方面。**

​	RDD将Spark的底层的细节都隐藏起来（自动容错、位置感知、任务调度执行，失败重试等），让开发者可以像操作本地集合一样**以函数式编程的方式操作RDD**这个分布式数据集，进行各种并行计算，RDD中很多处理数据函数与列表List中相同与类似。

### 1.4.2 总结

​	RDD是一个应用层面的逻辑概念。一个RDD多个分片。RDD就是一个元数据记录集，记录了RDD内存所有的关系数据。

<img src=".\1-SparkBase-Core.assets\image-20230525180415512.png" alt="image-20230525180415512" style="zoom:50%;" />

## 1.5 RDD特点

​	RDD表示只读的分区的数据集，对RDD进行改动，只能通过RDD的转换操作，由一个RDD得到一个新的RDD，新的RDD包含了从其他RDD衍生所必需的信息。RDDs之间存在依赖，RDD的执行是按照血缘关系延时计算的。如果血缘关系较长，可以通过持久化RDD来切断血缘关系。	

### 1.5.1 分区

​	 **RDD逻辑上是分区**的，每个分区的数据是**抽象**存在的，计算的时候会通过**一个compute函数得到每个分区的数据**。如果RDD是通过已有的文件系统构建，则compute函数是读取指定文件系统中的数据，如果RDD是通过其他RDD转换而来，则compute函数是执行转换逻辑将其他RDD的数据进行转换。

<img src=".\1-SparkBase-Core.assets\image-20230525180914581.png" alt="image-20230525180914581" style="zoom:50%;" />

### 1.5.2 只读

​	如下图所示，RDD是只读的，**要想改变RDD中的数据，只能在现有的RDD基础上创建新的RDD。**

<img src=".\1-SparkBase-Core.assets\image-20230525181326613.png" alt="image-20230525181326613" style="zoom:50%;" />

​	由一个RDD转换到另一个RDD，可以通过丰富的操作算子实现，不再像MapReduce那样只能写map和reduce了，如下图所示。

<img src=".\1-SparkBase-Core.assets\image-20230525181502223.png" alt="image-20230525181502223" style="zoom:50%;" />

​	RDD的操作算子包括两类，一类叫做transformations，它是用来将RDD进行转化，构建RDD的血缘关系；另一类叫做actions，它是用来触发RDD的计算，得到RDD的相关计算结果或者将RDD保存的文件系统中。下图是RDD所支持的部分操作算子列表。

<img src=".\1-SparkBase-Core.assets\image-20230525181549603.png" alt="image-20230525181549603" style="zoom:50%;" />

### 1.5.3 依赖

​	RDDs通过操作算子进行转换，转换得到的新RDD包含了从其他RDDs衍生所必需的信息，RDDs之间维护着这种血缘关系，也称之为依赖。如下图所示，依赖包括两种，一种是窄依赖，RDDs之间分区是一一对应的，另一种是宽依赖，**下游RDD的每个分区与上游RDD(也称之为父RDD)的每个分区都有关，是多对多的关系。**

<img src=".\1-SparkBase-Core.assets\image-20230525181651725.png" alt="image-20230525181651725" style="zoom:50%;" />

​	通过RDDs之间的这种依赖关系，一个任务流可以描述为DAG(有向无环图)，如下图所示，在实际执行过程中宽依赖对应于Shuffle(图中的reduceByKey和join)，窄依赖中的所有转换操作可以通过类似于管道的方式一气呵成执行(图中map和union可以一起执行)。

<img src=".\1-SparkBase-Core.assets\image-20230525181723105.png" alt="image-20230525181723105" style="zoom:50%;" />

### 1.5.4 缓存

​	如果**在应用程序中多次使用同一个RDD，可以将该RDD缓存起来**，该RDD只有在第一次计算的时候会根据**血缘关系得到分区的数据**，在后续其他地方用到该RDD的时候，会直接从缓存处取而不用再根据血缘关系计算，这样就加速后期的重用。**如下图所示**，RDD-1经过一系列的转换后得到RDD-n并保存到hdfs，RDD-1在这一过程中会有个中间结果，如果将其缓存到内存，那么在随后的RDD-1转换到RDD-m这一过程中，就不会计算其之前的RDD-0了。

<img src=".\1-SparkBase-Core.assets\image-20230525181808063.png" alt="image-20230525181808063" style="zoom:50%;" />

### 1.5.5 checkpoint

​	虽然RDD的血缘关系天然地可以实现容错，当RDD的某个分区数据失败或丢失，可以通过血缘关系重建。但是对于长时间迭代型应用来说，随着迭代的进行，**RDDs之间的血缘关系会越来越长，一旦在后续迭代过程中出错，则需要通过非常长的血缘关系去重建，势必影响性能**。为此，RDD支持checkpoint将数据保存到持久化的存储中，这样就可以切断之前的血缘关系，因为checkpoint后的RDD不需要知道它的父RDDs了，它可以从checkpoint处拿到数据。

​	给定一个RDD我们至少可以知道如下几点信息：

​		1、分区数以及分区方式；

​		2、由父RDDs衍生而来的相关依赖信息；

​		3、计算每个分区的数据，计算步骤为：

​			1）如果被缓存，则从缓存中取的分区的数据；

​			2）如果被checkpoint，则从checkpoint处恢复数据；

​			3）根据血缘关系计算分区的数据。

# 2. RDD的创建

​	将数据封装到RDD集合中，主要有两种方式：**并行化本地集合（Driver Program中）和引用加载外部存储系统（如HDFS、Hive、HBase、Kafka、Elasticsearch等）数据集**。

<img src=".\1-SparkBase-Core.assets\image-20230525182254439.png" alt="image-20230525182254439" style="zoom:67%;" />

## 2.1 方式一：并行化

​	使用并行化集合，本质上是将本地的集合作为参数传递到sc.parallelize函数中

<img src=".\1-SparkBase-Core.assets\image-20230525183206388.png" alt="image-20230525183206388" style="zoom:67%;" />

```python
data = [1, 2, 3, 4, 5]
# 调用`SparkContext`的 `parallelize` 方法并且传入已有的可迭代对象或者集合
distData = sc.parallelize(data)

# 调用
data
```

## 2.2 方式二：通过文件创建

​	使用sc.textFile方式读取外部文件系统，包括hdfs和本地文件系统


​	Spark将为群集的每个分区（partition）运行一个任务（task）。 通常，可以根据CPU核心数量指定分区数量（每个CPU有2-4个分区）如未指定分区数量，Spark会自动设置分区数对应local参数设置。	

```Python
#!/usr/bin/python
# -*- coding:UTF-8 -*-
# Filename: test.py
'''
1-准备SparkContext的入口，申请资源
2-使用rdd创建的第一种方法
3-使用rdd创建的第二种方法
4-关闭SparkContext
'''

from pyspark import SparkConf, SparkContext

# import os
# os.environ["JAVA_HOME"] = '/home/app/jdk1.8'
# os.environ["PYSPARK_PYTHON"] = '/home/anaconda3/envs/pyspark_3.6/bin/python'

if __name__ == '__main__':
    # 1-准备SparkContext的入口，申请资源
    conf = SparkConf().setMaster("spark://xian:7077").setAppName("rdd-1")
    # conf = SparkConf().setMaster("local[*]").setAppName("rdd-1")
    sc = SparkContext(conf=conf)

    def my_create_one():
        # 2- 使用rdd创建的第一种方法
        data = [1, 2, 3, 4, 5]
        rdd1 = sc.parallelize(data)
        rdd2 = rdd1.map(lambda x: x * 2)
        print(rdd2.collect())
    def my_create_two():
        # 3- 使用rdd创建的第种方法
        counts = sc.textFile("hdfs://xian:9000/word/wd.txt")\
        	.flatMap(lambda line:line.split(" "))\
        	.map(lambda x:(x, 1))\
        	.reduceByKey(lambda a,b:a+b).collect()
   		print(counts)

    my_create_one()
    # 4- 关闭SparkContext
    sc.stop()
```

## 2.3 读取小文件

​	在实际项目中，有时往往处理的数据文件属于**小文件（每个文件数据数据量很小，比如KB，几十MB等），文件数量又很大**，如果一个个文件读取为RDD的一个个分区，计算数据时很耗时性能低下，使用SparkContext中提供：**wholeTextFiles**类，专门读取小文件数据。

![image-20230531143728850](.\1-SparkBase-Core.assets\image-20230531143728850.png)



​	范例演示：读取100个小文件rating数据，每个文件大小小于1MB，**查看默认情况下分区个数情况**

```Python
from pyspark import SparkContext, SparkConf

if __name__ == '__main__':
    print('PySpark WholeTextFile Program')
    # TODO：1、创建应用程序入口SparkContext实例对象
    conf = SparkConf().setAppName("miniProject").setMaster("local[*]")
    sc = SparkContext.getOrCreate(conf)
    # TODO: 2、从文件系统加载数据，调用textFile
    resultRDD1 = sc.textFile("file:///home/data/ratings100/")
    # TODO: 3、调用集合RDD中函数处理分析数据，调用wholeTextFiles
    resultRDD2 = sc.wholeTextFiles("file:///home/data/ratings100/")
    # TODO: 4、获取分区数
    print("textFile numpartitions:", resultRDD1.getNumPartitions())
    print("whole textFile numpartitions:", resultRDD2.getNumPartitions())
    # print(resultRDD2.take(2))
    print('停止 PySpark SparkSession 对象')
    # 关闭SparkContext
    sc.stop()
```



# 3. RDD的操作

​	有一定开发经验的读者应该都使用过多线程，**利用多核 CPU 的并行能力来加快运算速率**。在开发并行程序时，**可以利用类似 Fork/Join 的框架将一个大的任务切分成细小的任务，每个小任务模块之间是相互独立的，可以并行执行，然后将所有小任务的结果汇总起来，得到最终的结果。**

​	一个非常好的例子便是归并排序。对整个序列进行排序时，可以将序列切分成多个子序列进行排序，然后将排好序的子序列归并起来得到最终的结果。

<img src=".\1-SparkBase-Core.assets\image-20230531145308952.png" alt="image-20230531145308952" style="zoom:67%;" />

​	对 Hadoop 有所了解的读者都知道 map、reduce 操作。对于大量的数据，我们可以通过 map 操作让不同的集群节点并行计算，之后通过 reduce 操作将结果整合起来得到最终输出。

## 3.1 函数分类

​	对于 Spark 处理的大量数据而言，会将数据切分后放入RDD作为Spark 的基本数据结构，开发者可以在 RDD 上进行丰富的操作，之后 Spark 会根据操作调度集群资源进行计算。总结起来，RDD 的操作主要可以**分为 Transformation 和 Action 两种**。

<img src=".\1-SparkBase-Core.assets\image-20230531145439271.png" alt="image-20230531145439271" style="zoom:50%;" />

​	**Transformation转换操作：**返回一个新的RDD，所有Transformation函数都是**Lazy**，不会立即执行，需要Action函数触发；

​	**Action动作操作：**返回值不是RDD(无返回值或返回其他的），所有Action函数立即执行（Eager），比如count、first、collect、take等。

<img src=".\1-SparkBase-Core.assets\image-20230531150118768.png" alt="image-20230531150118768" style="zoom: 50%;" />

注意：

​	第一点：RDD不实际存储真正要计算的数据，而是记录了数据的位置在哪里，数据的转换关系(调用了什么方法，传入什么函数)；

​	第二点：RDD中的所有转换都是惰性求值/延迟执行的，也就是说并不会直接计算。只有当发生一个要求返回结果给Driver的Action动作时，这些转换才会真正运行。之所以使用惰性求值/延迟执行，是因为这样**可以在Action时对RDD操作形成DAG有向无环图进行Stage的划分和并行优化，这种设计让Spark更加有效率地运行**。

## 3.2 Transformation算子

### 3.2.1 概念

​	在Spark中Transformation操作表示将一个RDD通过一系列操作变为另一个RDD的过程，这个操作可能是简单的加减操作，也可能是某个函数或某一系列函数。值得注意的是Transformation操作并不会触发真正的计算，只会建立RDD间的关系图。

​	如下图所示，RDD内部每个方框是一个分区。**假设需要采样50%的数据，通过sample函数，从 V1、V2、U1、U2、U3、U4 采样出数据 V1、U1 和 U4，形成新的RDD**。

<img src=".\1-SparkBase-Core.assets\image-20230531151322350.png" alt="image-20230531151322350" style="zoom:50%;" />

​	常用Transformation转换函数：

<img src=".\1-SparkBase-Core.assets\image-20230531151656371.png" alt="image-20230531151656371" style="zoom:50%;" />

<img src=".\1-SparkBase-Core.assets\image-20230531151736024.png" alt="image-20230531151736024" style="zoom:50%;" />

| Transformation算子                                    | 含义                                                         |
| ----------------------------------------------------- | ------------------------------------------------------------ |
| map(func)                                             | 返回一个新的RDD，该RDD由每一个输入元素经过func函数转换后组成 |
| filter(func)                                          | 返回一个新的RDD，该RDD由经过func函数计算后返回值为true的输入元素组成 |
| flatMap(func)                                         | 类似于map，但是每一个输入元素可以被映射为0或多个输出元素(所以func应该返回一个序列，而不是单一元素) |
| mapPartitions(func)                                   | 类似于map，但独立地在RDD的每一个分片上运行，因此在类型为T的RDD上运行时，func的函数类型必须是Iterator[T] => Iterator[U] |
| mapPartitionsWithIndex(func)                          | 类似于mapPartitions，但func带有一个整数参数表示分片的索引值，因此在类型为T的RDD上运行时，func的函数类型必须是  (Int, Interator[T]) => Iterator[U] |
| sample(withReplacement, fraction,  seed)              | 根据fraction指定的比例对数据进行采样，可以选择是否使用随机数进行替换，seed用于指定随机数生成器种子 |
| union(otherDataset)                                   | 对源RDD和参数RDD求并集后返回一个新的RDD                      |
| intersection(otherDataset)                            | 对源RDD和参数RDD求交集后返回一个新的RDD                      |
| distinct([numTasks]))                                 | 对源RDD进行去重后返回一个新的RDD                             |
| groupByKey([numTasks])                                | 在一个(K,V)的RDD上调用，返回一个(K, Iterator[V])的RDD        |
| reduceByKey(func, [numTasks])                         | 在一个(K,V)的RDD上调用，返回一个(K,V)的RDD，使用指定的reduce函数，将相同key的值聚合到一起，与groupByKey类似，reduce任务的个数可以通过第二个可选的参数来设置 |
| aggregateByKey(zeroValue)(seqOp,  combOp, [numTasks]) |                                                              |
| sortByKey([ascending], [numTasks])                    | 在一个(K,V)的RDD上调用，K必须实现Ordered接口，返回一个按照key进行排序的(K,V)的RDD |
| sortBy(func,[ascending], [numTasks])                  | 与sortByKey类似，但是更灵活                                  |
| join(otherDataset, [numTasks])                        | 在类型为(K,V)和(K,W)的RDD上调用，返回一个相同key对应的所有元素对在一起的(K,(V,W))的RDD |
| cogroup(otherDataset, [numTasks])                     | 在类型为(K,V)和(K,W)的RDD上调用，返回一个(K,(Iterable<V>,Iterable<W>))类型的RDD |
| cartesian(otherDataset)                               | 笛卡尔积                                                     |
| pipe(command, [envVars])                              | 对rdd进行管道操作                                            |
| coalesce(numPartitions)                               | 减少 RDD 的分区数到指定值。在过滤大量数据之后，可以执行此操作 |
| repartition(numPartitions)                            | 重新给 RDD 分区                                              |

### 3.2.2 值类型 ValueType

#### map

<img src=".\1-SparkBase-Core.assets\image-20230531153212374.png" alt="image-20230531153212374" style="zoom:70%;" />

​	将func函数作用到数据集的**每一个**元素上，生成一个新的RDD返回。

```python
# 参数3表示预设3个分区
rdd1 = sc.parallelize([1,2,3,4,5,6,7,8,9],3)
rdd2 = rdd1.map(lambda x: x+1)
rdd2.collect()
```

​	自定义lambda函数：

<img src=".\1-SparkBase-Core.assets\image-20230531153708786.png" alt="image-20230531153708786" style="zoom:67%;" />

```python
rdd1 = sc.parallelize([1,2,3,4,5,6,7,8,9],3)
def add(x):
   return x+1
rdd2 = rdd1.map(add).collect()
```

#### groupBy

```python
# 分组函数
x = sc.parallelize([1,2,3]) 
y = x.groupBy(lambda x: 'A' if (x%2 == 1) else 'B' )
print(y.mapValues(list).collect())
```

#### filter

```python
# filter(func) 选出所有func返回值为true的元素，生成一个新的RDD返回
rdd1 = sc.parallelize([1,2,3,4,5,6,7,8,9],3)
rdd2 = rdd1.map(lambda x:x*2)
rdd3 = rdd2.filter(lambda x:x>4)
rdd3.collect()
```

#### flatMap

```python
# flatMap会先执行map的操作，再将所有对象合并为一个对象
rdd1 = sc.parallelize(["a b c","d e f","h i j"])
rdd2 = rdd1.flatMap(lambda x:x.split(" "))
rdd2.collect()
```

#### sortBy

```python
data = [('a',1), ('a',3), ('a',7), ('b',1), ('a',5), ('k',1)]
rdd1 = sc.parallelize(data)
#参数1：排序依据  参数2：true升序   参数3：排序分区
#分区数：1为全局   其余更具业务调整
rdd2 = rdd1.sortBy(lambda x: x[1], ascending=False, numPartitions=3).collect()
rdd3 = rdd1.sortBy(lambda x: x[0], ascending=False, numPartitions=3).collect()
```

### 3.2.3 双值类型 DoubleValueType

#### Union

```python
# 两个RDD求并集
rdd1 = sc.parallelize([("a",1),("b",2)])
rdd2 = sc.parallelize([("c",1),("b",3)])
rdd3 = rdd1.union(rdd2)
rdd3.collect()
```

#### Intersection

```python
# 两个RDD求交集
rdd1 = sc.parallelize([("a",1),("b",2)])
rdd2 = sc.parallelize([("c",1),("b",3)])
rdd3 = rdd1.union(rdd2)
rdd4 = rdd3.intersection(rdd2)
rdd4.collect()
```

#### zip

```python
# 拉链
rdd1 = sc.parallelize([1, 2, 3, 4, 5])
rdd2 = sc.parallelize([5, 4, 6, 7, 8])
rdd4 = rdd1.zip(rdd2).collect()
```

#### distinct

```python
rdd1 = sc.parallelize([1, 2, 3, 4, 5])
rdd2 = sc.parallelize([5, 4, 6, 7])
rdd4 = rdd1.union(rdd2).distinct().collect()
```

### 3.2.4 Key-Value值类型

#### groupByKey

​	以元组中的第0个元素作为key，进行分组，返回一个新的RDD

```python
rdd1 = sc.parallelize([("a",1),("b",2)])
rdd2 = sc.parallelize([("c",1),("b",3)])
rdd3 = rdd1.union(rdd2)
rdd4 = rdd3.groupByKey()
rdd4.collect()
# groupByKey之后的结果中 value是一个Iterable
# 需要通过mapValues的方式来获取其中内容
rdd4 = rdd3.groupByKey().map(lambda x:{x[0]:list(x[1])}).collect()
```

#### reduceByKey

​	将key相同的键值对，按照Function进行计算

```python
rdd = sc.parallelize([("a", 1), ("b", 1), ("a", 1)])
rdd.reduceByKey(lambda x,y:x+y).collect()
```

#### sortByKey

​	根据key进行排序

```python
# `sortByKey`(ascending=True, numPartitions=None, keyfunc=<function RDD.<lambda>>)
tmp = [('a', 1), ('b', 2), ('1', 3), ('d', 4), ('2', 5)]
sc.parallelize(tmp).sortByKey().first()

sc.parallelize(tmp).sortByKey(True, 1).collect()
    
sc.parallelize(tmp).sortByKey(True, 2).collect()
   
tmp2 = [('Mary', 1), ('had', 2), ('a', 3), ('little', 4), ('lamb', 5)]
tmp2.extend([('whose', 6), ('fleece', 7), ('was', 8), ('white', 9)])
sc.parallelize(tmp2).sortByKey(True, 3, keyfunc=lambda k: k.lower()).collect()
```

#### countByValue

```python
x = sc.parallelize([1,3,1,2,3])
y = x.countByValue()
print(x.collect())
# [1, 3, 1, 2, 3]

print(y)
# defaultdict(<class 'int'>, {1: 2, 3: 2, 2: 1})
```



## 3.3 Action算子

### 3.3.1 概念

​	不同于Transformation操作，**Action操作代表一次计算的结束，不再产生新的 RDD，将结果返回到Driver程序或者输出到外部**。所以**Transformation操作只是建立计算关系，而Action 操作才是实际的执行者**。每个Action操作都会调用SparkContext的runJob 方法向集群正式提交请求，所以每个Action操作对应一个Job。

<img src=".\1-SparkBase-Core.assets\image-20230531151847008.png" alt="image-20230531151847008" style="zoom:60%;" />

| Action算子                               | 含义                                                         |
| ---------------------------------------- | ------------------------------------------------------------ |
| reduce(func)                             | 通过func函数聚集RDD中的所有元素，这个功能必须是可交换且可并联的 |
| collect()                                | 在驱动程序中，以数组的形式返回数据集的所有元素               |
| count()                                  | 返回RDD的元素个数                                            |
| first()                                  | 返回RDD的第一个元素(类似于take(1))                           |
| take(n)                                  | 返回一个由数据集的前n个元素组成的数组                        |
| takeSample(withReplacement,num,  [seed]) | 返回一个数组，该数组由从数据集中随机采样的num个元素组成，可以选择是否用随机数替换不足的部分，seed用于指定随机数生成器种子 |
| takeOrdered(n, [ordering])               | 返回自然顺序或者自定义顺序的前 n 个元素                      |
| saveAsTextFile(path)                     | 将数据集的元素以textfile的形式保存到HDFS文件系统或者其他支持的文件系统，对于每个元素，Spark将会调用toString方法，将它装换为文件中的文本 |
| saveAsSequenceFile(path)                 | 将数据集中的元素以Hadoop sequencefile的格式保存到指定的目录下，可以使HDFS或者其他Hadoop支持的文件系统。 |
| saveAsObjectFile(path)                   | 将数据集的元素，以 Java 序列化的方式保存到指定的目录下       |
| countByKey()                             | 针对(K,V)类型的RDD，返回一个(K,Int)的map，表示每一个key对应的元素个数。 |
| foreach(func)                            | 在数据集的每一个元素上，运行函数func进行更新。               |
| foreachPartition(func)                   | 在数据集的每一个分区上，运行函数func                         |

​	相关数学操作：

| Action算子     | 含义                      |
| -------------- | ------------------------- |
| count          | 个数                      |
| mean           | 均值                      |
| sum            | 求和                      |
| max            | 最大值                    |
| min            | 最小值                    |
| variance       | 方差                      |
| sampleVariance | 从采样中计算方差          |
| stdev          | 标准差:衡量数据的离散程度 |
| sampleStdev    | 采样的标准差              |
| stats          | 查看统计结果              |

### 3.3.2 详解

#### collect

​	返回一个list，list中包含 RDD中的所有元素。只有当数据量较小的时候使用Collect 因为所有的结果都会加载到内存中

```python
rdd1 = sc.parallelize([1,2,3,4,5,6,7,8,9],3)
rdd2 = rdd1.map(lambda x: x+1)
rdd2.collect()
```

#### reduce

​	reduce将RDD中元素两两传递给输入函数，同时产生一个新的值，新产生的值与RDD中下一个元素再被传递给输入函数直到最后只有一个值为止。

```python
rdd1 = sc.parallelize([1,2,3,4,5])
rdd1.reduce(lambda x,y : x+y)
```

#### first

​	返回RDD的第一个元素

```python
sc.parallelize([2, 3, 4]).first()
```

#### take

​	 返回RDD的前N个元素

```python
#`take`(*num*)
sc.parallelize([2, 3, 4, 5, 6]).take(2)
# [2, 3]

sc.parallelize([2, 3, 4, 5, 6]).take(10)
# [2, 3, 4, 5, 6]

sc.parallelize(range(100), 100).filter(lambda x: x > 90).take(3)
# [91, 92, 93]
```

#### Top 

​	排序取前几个从大到小

```python
x = sc.parallelize([1,3,1,2,3])
y = x.top(num = 3)
print(x.collect())
# [1, 3, 1, 2, 3]

print(y)
# [3, 3, 2]
```

#### Count

​	返回RDD中元素的个数

```python
sc.parallelize([2, 3, 4]).count()
# 3
```

#### takeSample

```python
rdd = sc.parallelize(range(0, 10))
rdd.takeSample(True, 20, 1)
# [0, 6, 3, 4, 3, 1, 3, 7, 3, 5, 3, 0, 0, 9, 6, 5, 7, 9, 4, 7]
rdd.takeSample(True, 5, 1)  
# [8, 8, 0, 3, 6]
rdd.takeSample(True, 5, 1)
# [8, 8, 0, 3, 6]
rdd.takeSample(False, 5, 2)
# [5, 9, 3, 4, 6]
rdd.takeSample(False, 5, 2)
# [5, 9, 3, 4, 6]
```

#### foreach

​	仅返回满足foreach内函数条件元素。在下面的示例中，我们在foreach中调用print函数，它打印RDD中的所有元素。

```python
words = sc.parallelize (["scala","java","hadoop","spark","akka","spark vs hadoop","pyspark","pyspark and spark"])
def f(x): print(x)
fore = words.foreach(f)
```



## 3.4 拓展强化

<img src=".\1-SparkBase-Core.assets\image-20230531163910805.png" alt="image-20230531163910805" style="zoom:67%;" />

### 3.4.1 基本函数

​	RDD中map、filter、flatMap及foreach等函数为最基本函数，都是都RDD中每个元素进行操作，将元素传递到函数中进行转换。基本函数可以理解为常用的Transformation算子与Action算子。

**map 函数：**

​	map(f:T=>U) : RDD[T]=>RDD[U]，表示将 RDD 经由某一函数 f 后，转变为另一个RDD。

**flatMap 函数：**

​	flatMap(f:T=>Seq[U]) : RDD[T]=>RDD[U])，表示将 RDD 经由某一函数 f 后，转变为一个新的 RDD，但是与 map 不同，RDD 中的每一个元素会被映射成新的 0 到多个元素（f 函数返回的是一个序列 Seq）。

**filter 函数：**

​	filter(f:T=>Bool) : RDD[T]=>RDD[T]，表示将 RDD 经由某一函数 f 后，只保留 f 返回为 true 的数据，组成新的 RDD。

 **foreach 函数：**

​	foreach(func)，将函数 func 应用在数据集的每一个元素上，通常用于更新一个累加器，或者和外部存储系统进行交互，例如 Redis。关于 foreach，在后续章节中还会使用，到时会详细介绍它的使用方法及注意事项。

 **saveAsTextFile 函数：**

​	saveAsTextFile(path:String)，数据集内部的元素会调用其 toString 方法，转换为字符串形式，然后根据传入的路径保存成文本文件，既可以是本地文件系统，也可以是HDFS 等

### 3.4.2 分区操作函数

​	每个RDD由多分区组成的，实际开发建议**对每个分区数据的进行操作**，map函数使用mapPartitions代替、foreache函数使用foreachPartition代替。

**foreachPartition**

```Python
def f(iterator):
	for x in iterator:
        print(x)
sc.parallelize([1, 2, 3, 4, 5]).foreachPartition(f)
```

**mapPartition**

```Python
rdd = sc.parallelize([1, 2, 3, 4], 2)
def f(iterator): yield sum(iterator)

rdd.mapPartitions(f).collect()
```

​	应用场景：**处理网站日志数据，数据量为10GB，统计各个省份相关信息；电商后台统计每日销量等**

### 3.4.3 重分区函数

#### **repartition**

​	增加分区函数，此函数使用的谨慎，会产生Shuffle。

```Python
rdd = sc.parallelize([1,2,3,4,5,6,7], 4)
sorted(rdd.glom().collect())
# [[1], [2, 3], [4, 5], [6, 7]]

len(rdd.repartition(2).glom().collect())
# 2
len(rdd.repartition(10).glom().collect())
# 10

rdd.glom().collect()
# [[1], [2, 3], [4, 5], [6, 7]]
```

#### **coalesce**

​	减少分区函数，此函数不会产生Shuffle，当且仅当降低RDD分区数目。比如RDD的分区数目为10个分区，此时调用rdd.coalesce(12)，不会对RDD进行任何操作。

```Python
sc.parallelize([1, 2, 3, 4, 5], 3).glom().collect()            
# [[1], [2, 3], [4, 5]]
sc.parallelize([1, 2, 3, 4, 5], 3).coalesce(1).glom().collect()
# [[1, 2, 3, 4, 5]]
sc.parallelize([1, 2, 3, 4, 5], 3).coalesce(4).glom().collect()
# [[1], [2, 3], [4, 5]]
sc.parallelize([1, 2, 3, 4, 5], 3).coalesce(4,True).glom().collect() 
# [[4, 5], [2, 3], [], [1]]
```

#### PairRDDFunctions

​	在PairRDDFunctions（此类专门针对RDD中数据类型为KeyValue对提供函数）工具类中。

```Python
pairs = sc.parallelize([1, 2, 3, 4, 2, 4, 1]).map(lambda x: (x, x)) 
pairs.getNumPartitions()
# 2
pairs.partitionBy(3).glom().collect()                               
#[[(3, 3)], [(1, 1), (4, 4), (4, 4), (1, 1)], [(2, 2), (2, 2)]]

len(pairs.partitionBy(3).glom().collect())                          
# 3
```

#### 代码示例

```Python
from pyspark import SparkConf, SparkContext
import re
'''
分区内：一个rdd可以分为很多分区，每个分区里面都是有大量元素，每个分区都需要线程执行
分区间：有一些操作分区间做一些累加
alt+6 可以调出来所有TODO，
TODO是Python提供了预留功能的地方
'''
if __name__ == '__main__':
     #TODO:  1-创建SparkContext申请资源
     conf = SparkConf().setAppName("mini2").setMaster("local[*]")
     sc = SparkContext.getOrCreate(conf=conf)
     sc.setLogLevel("WARN")  # 一般在工作中不这么写，直接复制log4j文件
     #TODO:   2-执行重分区函数--repartition
     rdd1 = sc.parallelize([1, 2, 3, 4, 5, 6], 3)
     print("partitions num:",rdd1.getNumPartitions())
     print(rdd1.glom().collect())#[[1, 2], [3, 4], [5, 6]]
     print("repartition result:")
     #TODO:   repartition可以增加分区也可以减少分区，但是都会产生shuflle，如果减少分区的化建议使用coalesc避免发生shuffle
     rdd__repartition1 = rdd1.repartition(5)
     print("increase partition",rdd__repartition1.glom().collect())#[[], [1, 2], [5, 6], [3, 4], []]
     rdd__repartition2 = rdd1.repartition(2)
     print("decrease partition",rdd__repartition2.glom().collect())#decrease partition [[1, 2, 5, 6], [3, 4]]
     #TODO:   3-减少分区--coalese
     print(rdd1.coalesce(2).glom().collect())#[[1, 2], [3, 4, 5, 6]]
     print(rdd1.coalesce(5).glom().collect())#[[1, 2], [3, 4], [5, 6]]
     print(rdd1.coalesce(5,True).glom().collect())#[[], [1, 2], [5, 6], [3, 4], []]
     # 结论：repartition默认调用的是coalese的shuffle为True的方法
     # TODO:  4-PartitonBy,可以调整分区，还可以调整分区器(一种hash分区器(一般打散数据)，一种range分区器(排序拍好的))
     # 此类专门针对RDD中数据类型为KeyValue对提供函数
     # rdd五大特性中有第四个特点key-value分区器，默认是hashpartitioner分区器
     rdd__map = rdd1.map(lambda x: (x, x))
     print("partitions length:",rdd__map.getNumPartitions())#partitions length: 3
     print(rdd__map.partitionBy(2).glom().collect())
```

### 3.4.4 聚合函数

#### reduce&fold

​	在RDD中提供类似列表List中聚合函数reduce和fold。

```Python
from operator import add
sc.parallelize([1, 2, 3, 4, 5]).reduce(add)
# 15
sc.parallelize((2 for _ in range(10))).map(lambda x: 1).cache().reduce(add)
# 10
sc.parallelize([]).reduce(add)
# 报错：Can not reduce() empty RDD

sc.parallelize([1, 2, 3, 4, 5]).fold(0, add)
# 15
```

#### aggregate

​	高级聚合函数aggregate，**初始值作用于分区内和分区间**。

​	aggregate函数将**每个\*分区里面\*的元素通过****seqOp和初始值进行聚合**，然后用combine函数将***(分区间)\*每个分区的结果和初始值(zeroValue)进行combine操作**。这个函数最终返回的类型不需要和RDD中元素类型一致。

```Python
seqOp = (lambda x, y: (x[0] + y, x[1] + 1))       
combOp = (lambda x, y: (x[0] + y[0], x[1] + y[1]))
sc.parallelize([1, 2, 3, 4]).aggregate((0, 0), seqOp, combOp)
# (10, 4) 累加求和为10，共计4个元素
```

#### Key/Value聚合函数

​	在Spark中有一个object对象**PairRDDFunctions**，主要针对RDD的数据类型是Key/Value对的数据提供函数，方便数据分析处理。比如使用过的函数：reduceByKey、groupByKey等。**ByKey函数**：**将相同Key的Value进行聚合操作的，省去先分组再聚合**。

​	**分组函数：groupByKey**

​	**分组聚合函数：reduceByKey&foldByKey**，聚合以后的结果数据类型与RDD中Value的数据类型是一样的

​	**分组聚合函数：aggregateByKey**，在企业中如果对数据聚合使用，**不能使用reduceByKey完成时，考虑使用aggregateByKey函数**，基本上都能完成任意聚合功能

代码示例：

```python
# -*- coding: utf-8 -*-
from pyspark import SparkContext, SparkConf
import re
# add == a+b
from operator import add

if __name__ == '__main__':
    print('PySpark agg Function Program')
    # TODO：1、创建应用程序入口SparkContext实例对象
    conf = SparkConf().setAppName("miniProject").setMaster("local[*]")
    sc = SparkContext.getOrCreate(conf)
    # TODO: 2、从本地文件系统创建RDD数据集
    rdd = sc.parallelize([("a", 1), ("b", 1), ("a", 1)])
    # TODO: 3、调用集合RDD中函数处理分析数据
    # TODO: 4、通过ForeachPartition展示结果
    print("==================groupByKey=======================")
    print(sorted(rdd.groupByKey().mapValues(len).collect()))
    # [('a', 2), ('b', 1)]
    print(sorted(rdd.groupByKey().mapValues(list).collect()))
    # [('a', [1, 1]), ('b', [1])]
    print("==================reduceByKey=======================")
    print(sorted(rdd.reduceByKey(add).collect()))
    # [('a', 2), ('b', 1)]
    print("==================foldByKey=======================")
    print(sorted(rdd.foldByKey(0, add).collect()))
    # [('a', 2), ('b', 1)]
    print("===================aggregateByKey======================")
    print(rdd.aggregateByKey(0, add, add).collect())
    # [('b', 1), ('a', 2)]
    print(sorted(rdd.aggregateByKey(0, add, add).collect()))
    # [('a', 2), ('b', 1)]
    print("==================groupByKey实现wordcount=======================")
    lineseq = ["hadoop scala   hive spark scala sql sql",
               "hadoop scala spark hdfs hive    spark",
               "spark hdfs   spark hdfs scala hive spark"]
    inputRDD = sc.parallelize(lineseq, 2)
    wordsRDD = inputRDD.flatMap(lambda line: re.split("\\s+", line)).map(lambda word: (word, 1))
    wordsGroupRDD = wordsRDD.groupByKey()
    # 仅仅对value进行sum加和
    print(wordsGroupRDD.mapValues(sum).collectAsMap())#mapValues(list)
    print("==方法2实现wordcount==")
    print(wordsRDD.foldByKey(0,add).collect())
    # [('hadoop', 2), ('scala', 4), ('hive', 3), ('hdfs', 3), ('spark', 6), ('sql', 2)]
    print("==方法3实现wordcount==")
    print(wordsRDD.aggregateByKey(0,add,add).collect())
    # [('hadoop', 2), ('scala', 4), ('hive', 3), ('hdfs', 3), ('spark', 6), ('sql', 2)]
    # 关闭SparkContext
    print('停止 PySpark SparkContext对象')
    sc.stop()

```

# 4. RDD持久化&关联函数[理解]

## 4.1 为什么使用缓存

​	使用缓存的原因——提升应用程序性能与容错。

<img src=".\1-SparkBase-Core.assets\image-20230601111948921.png" alt="image-20230601111948921" style="zoom:67%;" />

​	思考：当在计算 RDD3 的时候如果出错了, 会怎么进行容错? 会再次计算 RDD1 和 RDD2 的整个链条, 假设 RDD1 和 RDD2 是通过比较昂贵的操作得来的, 有没有什么办法减少这种开销?

​	上述两个问题的解决方案其实都是 **缓存**, 除此之外, 使用缓存的理由还有很多, 但是总结一句, 就是缓存能够帮助开发者在进行一些昂贵操作后, 将其结果保存下来, 以便下次使用无需再次执行, 缓存能够显著的提升性能.

​	所以, 缓存适合在一个 RDD 需要重复多次利用, 并且还不是特别大的情况下使用, 例如迭代计算等场景.

​	因此，**Spark速度非常快的原因之一，就是在不同操作中可以在内存中持久化或者缓存数据集**。当持久化某个RDD后，每一个节点都将把计算分区结果保存在内存中，对此RDD或衍生出的RDD进行的其他动作中重用。这使得后续的动作变得更加迅速。RDD相关的持久化和缓存，是Spark最重要的特征之一。可以说，缓存是Spark构建迭代式算法和快速交互式查询的关键。

## 4.2 缓存函数

​	可以将RDD数据直接缓存到内存中，函数声明如下：

<img src=".\1-SparkBase-Core.assets\image-20230601112312266.png" alt="image-20230601112312266" style="zoom:67%;" />

​	但是实际项目中，不会直接使用上述的缓存函数，RDD数据量往往很多，内存放不下的。在实际的项目中缓存RDD数据时，往往使用如下函数，依据具体的业务和数据量，指定缓存的级别：

```python
def presist(newLevel: StorageLevel): this.type
```

<img src=".\1-SparkBase-Core.assets\image-20230601105004614.png" alt="image-20230601105004614" style="zoom:67%;" />

## 4.3 缓存级别

​	在Spark框架中对数据缓存可以指定不同的级别，对于开发来说至关重要，如下所示：

<img src=".\1-SparkBase-Core.assets\image-20230601112557214.png" alt="image-20230601112557214" style="zoom:67%;" />

​	实际项目中缓存数据时，往往选择如下两种级别：

<img src=".\1-SparkBase-Core.assets\image-20230601112930226.png" alt="image-20230601112930226" style="zoom:67%;" />

​	缓存函数与Transformation函数一样，都是Lazy操作，需要Action函数触发，通常使用count函数触发。

<img src=".\1-SparkBase-Core.assets\image-20230601113054833.png" alt="image-20230601113054833" style="zoom:67%;" />

​	官网注释：

<img src=".\1-SparkBase-Core.assets\image-20230601105103110.png" alt="image-20230601105103110" style="zoom:67%;" />

<img src=".\1-SparkBase-Core.assets\image-20230601105118090.png" alt="image-20230601105118090" style="zoom:67%;" />![image-20230601105141430](.\1-SparkBase-Core.assets\image-20230601105141430.png)

<img src=".\1-SparkBase-Core.assets\image-20230601105118090.png" alt="image-20230601105118090" style="zoom:67%;" />![image-20230601105141430](.\1-SparkBase-Core.assets\image-20230601105141430.png)

如何选择：

​	1-首选内存；

​	2-内存放不下，尝试序列化；

​	3-如果算子比较昂贵可以缓存在磁盘中，否则不要直接放入磁盘；

​	4-使用副本机制完成容错性质。



**如何选择分区级别**

​		Spark 的存储级别的选择，核心问题是在 memory 内存使用率和 CPU 效率之间进行权衡。建议按下面的过程进行存储级别的选择:

​		如果您的 RDD 适合于默认存储级别（MEMORY_ONLY），leave them that way。这是 CPU 效率最高的选项，允许 RDD 上的操作尽可能快地运行.

​		如果不是，试着使用 MEMORY_ONLY_SER 和 selecting a fast serialization library 以使对象更加节省空间，但仍然能够快速访问。(Java和Scala)

​		不要溢出到磁盘，除非计算您的数据集的函数是昂贵的，或者它们过滤大量的数据。否则，重新计算分区可能与从磁盘读取分区一样快.

​		如果需要快速故障恢复，请使用复制的存储级别（例如，如果使用 Spark 来服务 来自网络应用程序的请求）。All 存储级别通过重新计算丢失的数据来提供完整的容错能力，但复制的数据可让您继续在 RDD 上运行任务，而无需等待重新计算一个丢失的分区.

## 4.4 释放缓存

​	当缓存的RDD数据，不再被使用时，考虑释资源，使用如下函数，此函数属于eager，立即执行。

<img src=".\1-SparkBase-Core.assets\image-20230601114436720.png" alt="image-20230601114436720" style="zoom:67%;" />



## 4.5 何时缓存数据

​	第一种情况：当**某个RDD被使用多次**的时候，建议缓存此RDD数据。比如，从HDFS上读取网站行为日志数据，进行多维度的分析，最好缓存数据

​	第二种情况：当**某个RDD来之不易，并且使用不止一次**，建议缓存此RDD数据。比如，从HBase表中读取历史订单数据，与从MySQL表中商品和用户维度信息数据，进行关联Join等聚合操作，获取RDD：etlRDD，后续的报表分析使用此RDD，此时建议缓存RDD数据

```python
# -*- coding: utf-8 -*-
# Program function：演示关联函数-join操作
from pyspark import SparkConf, SparkContext
from pyspark.storagelevel import StorageLevel
import time
if __name__ == '__main__':
    print('PySpark join Function Program')
    # TODO：1、创建应用程序入口SparkContext实例对象
    conf = SparkConf().setAppName("miniProject").setMaster("local[*]")
    sc = SparkContext.getOrCreate(conf)
    # TODO: 2、从本地文件系统创建RDD数据集
    x = sc.parallelize([(1001, "zhangsan"), (1002, "lisi"), (1003, "wangwu"), (1004, "zhangliu")])
    y = sc.parallelize([(1001, "sales"), (1002, "tech")])
    # TODO:3、使用join完成联合操作
    join_result_rdd = x.join(y)
    print(join_result_rdd.collect())  # [(1001, ('zhangsan', 'sales')), (1002, ('lisi', 'tech'))]
    print(x.leftOuterJoin(y).collect())
    print(x.rightOuterJoin(y).collect())  # [(1001, ('zhangsan', 'sales')), (1002, ('lisi', 'tech'))]
    # 缓存--基于内存缓存-cache底层调用的是self.persist(StorageLevel.MEMORY_ONLY)
    join_result_rdd.cache()
    # join_result_rdd.persist(StorageLevel.MEMORY_AND_DISK_2)
    # 如果执行了缓存的操作，需要使用action算子触发，在4040页面上看到绿颜色标识
    join_result_rdd.collect()
    # 如果后续执行任何的操作会直接基于上述缓存的数据执行，比如count
    print(join_result_rdd.count())
    time.sleep(600)
    sc.stop()    
```



```python
# -*- coding: utf-8 -*-
from pyspark import SparkContext, SparkConf
import re
from pyspark.storagelevel import StorageLevel

if __name__ == '__main__':
    print('PySpark RDD Program')
    # TODO：1、创建应用程序入口SparkContext实例对象
    conf = SparkConf().setAppName("miniProject").setMaster("local[*]")
    sc = SparkContext.getOrCreate(conf)
    # TODO: 2、从文件系统加载数据，创建RDD数据集
    # TODO: 3、调用集合RDD中函数处理分析数据
    fileRDD = sc.textFile("file:///home/data/word.txt")
    # 缓存RDD
    fileRDD.cache()
    fileRDD.persist()
    # 使用Action触发缓存操作
    print("fileRDD count:", fileRDD.count())
    # 释放缓存
    fileRDD.unpersist()
    # 数据的相关操作
    resultRDD2 = fileRDD.flatMap(lambda line: re.split("\s+", line)) \
        .map(lambda x: (x, 1)) \
        .reduceByKey(lambda a, b: a + b)

    # StorageLevel.DISK_ONLY = StorageLevel(True, False, False, False)
    # StorageLevel.DISK_ONLY_2 = StorageLevel(True, False, False	, False, 2)
    # StorageLevel.DISK_ONLY_3 = StorageLevel(True, False, False, False, 3)
    # StorageLevel.MEMORY_ONLY = StorageLevel(False, True, False, False)
    # StorageLevel.MEMORY_ONLY_2 = StorageLevel(False, True, False, False, 2)
    # StorageLevel.MEMORY_AND_DISK = StorageLevel(True, True, False, False)
    # StorageLevel.MEMORY_AND_DISK_2 = StorageLevel(True, True, False, False, 2)
    # StorageLevel.OFF_HEAP = StorageLevel(True, True, True, False, 1)
    # StorageLevel.MEMORY_AND_DISK_DESER = StorageLevel(True, True, False, True)
    resultRDD2.persist(StorageLevel.MEMORY_ONLY)
    print("resultRDD2 count:", fileRDD.count())

    print('停止 PySpark SparkSession 对象')
    # 关闭SparkContext
    sc.stop()
```

# 5. RDD Checkpoint[理解]

 	RDD 数据可以持久化，但是持久化/缓存可以把数据放在内存中，虽然是快速的，但是也是最不可靠的；也可以把数据放在磁盘上，也不是完全可靠的！例如磁盘会损坏等。

​	**Checkpoint的产生就是为了更加可靠的数据持久化，在Checkpoint的时候一般把数据放在在HDFS上**，这就天然的借助了HDFS天生的高容错、高可靠来实现数据最大程度上的安全，实现了RDD的容错和高可用。

​	在Spark Core中对RDD做checkpoint，可以切断做checkpoint RDD的依赖关系，将RDD数据保存到可靠存储（如HDFS）以便数据恢复；

​	如何使用Checkpoint机制：

​		指定数据保存位置：**sc.setCheckpointDir**("hdfs://xian:9820/chehckpoint/")；

​		算子缓存：**rdd1.checkpoint**() 斩断依赖关系进行检查点；

​		检查点机制触发方式：**action算子可以触发**；

​		后续的计算：**Spark机制直接从checkpoint中读取数据**

## 5.1 检查点机制初体验

```python
# -*- coding: utf-8 -*-
from pyspark import SparkContext, SparkConf
import time

if __name__ == '__main__':
    print('PySpark checkpoint Program')
    # TODO：1、创建应用程序入口SparkContext实例对象
    conf = SparkConf().setAppName("miniProject").setMaster("local[*]")
    sc = SparkContext.getOrCreate(conf)
    # TODO: 2、RDD的checkpoint
    sc.setCheckpointDir("file:///home/data/checkpoint1")
    # TODO: 3、调用集合RDD中函数处理分析数据
    fileRDD = sc.textFile("file:///home/data/word.txt")
    # TODO: 调用checkpoint函数，将RDD进行备份，需要RDD中Action函数触发
    fileRDD.checkpoint()
    fileRDD.count()
    # TODO: 再次执行count函数, 此时从checkpoint读取数据
    fileRDD.count()

    time.sleep(100)
    print('停止 PySpark SparkSession 对象')
    # 关闭SparkContext
    sc.stop()
    # 可在4041Web端口就行查看
```

## 5.2 持久化和Checkpoint的区别

**存储位置的区别**：

​	Persist 和 Cache 只能保存在本地的磁盘和内存中(或者堆外内存)；

​	Checkpoint 可以保存数据到 HDFS 这类可靠的存储上；

**生命周期**

​	Cache和Persist的RDD会在程序结束后会被清除或者手动调用unpersist方法；

​	Checkpoint的RDD在程序结束后依然存在，不会被删除；

**Lineage(血统、依赖链、依赖关系)**

​	Persist和Cache，**不会丢掉RDD间的依赖链/依赖关系**，因为这种缓存是不可靠的，如果出现了一些错误(例如 Executor 宕机)，需要通过回溯依赖链重新计算出来；

​	**Checkpoint会斩断依赖链**，因为Checkpoint会把结果保存在HDFS这类存储中，更加的安全可靠，一般不需要回溯依赖链；

<img src=".\1-SparkBase-Core.assets\image-20230601134939553.png" alt="image-20230601134939553" style="zoom:67%;" />

## 5.3 先cache再checkpoint测试

​	**Spark容错机制：**首先会查看RDD是否被Cache，如果被Cache到内存或磁盘，直接获取，否则查看Checkpoint所指定的HDFS中是否缓存数据，如果都没有则直接从父RDD开始重新计算还原。

```python
# -*- coding: utf-8 -*-
# Program function：cache&checkpoint RDD

from pyspark import SparkContext, SparkConf
import time

if __name__ == '__main__':
    print('PySpark cache&checkpoint Program')
    # TODO：1、创建应用程序入口SparkContext实例对象
    conf = SparkConf().setAppName("miniProject").setMaster("local[*]")
    sc = SparkContext.getOrCreate(conf)
    # TODO: 2、RDD的checkpoint
    sc.setCheckpointDir("file:///home/data/checkpoint1")
    # TODO: 3、调用集合RDD中函数处理分析数据
    fileRDD = sc.textFile("file:///home/data/word.txt")
    # TODO: 调用checkpoint和cache函数，将RDD进行容错，需要RDD中Action函数触发
    print("=======1-同时做cache和Perisist========")
    fileRDD.cache() #cache会保留依赖链
    fileRDD.checkpoint()
    print("=2-启动Job1跑正常任务，启动Job2就会先从Cache读取数据，Web页面可以看到ProcessLocal===")
    fileRDD.count() #第一次执行action操作才会触发cache和checkpoint
    # TODO: 再次执行count函数, 此时从cache读取数据
    fileRDD.count() #再次触发会从cache中读取
    print("=======3-启动一个Job发现查询数据从checkpoint的hdfs中查找========")
    # TODO:释放cache之后如果在查询数据从哪里读取？ 答案是checkpoint的hdfs的数据中。
    fileRDD.unpersist(True)
    fileRDD.count() #没有绿色的点，也就是没有cache了

    time.sleep(100)
    print('停止 PySpark SparkSession 对象')
    # 关闭SparkContext
    sc.stop()
    # 可在4041Web端口就行查看
```

# 6. Spark案例练习

## 6.1 日志分析

​	在新闻类网站中，经常要衡量一条网络新闻的页面访问量，最常见的就是uv[网站的独立用户访问量]和pv[网站的总访问量]，如果在所有新闻中找到访问最多的前几条新闻，topN是最常见的指标。

​	数据示例：

```shell
#每条数据代表一次访问记录 包含了ip 访问时间 访问的请求方式 访问的地址...信息
194.237.142.21 - - [18/Sep/2013:06:49:18 +0000] "GET /wp-content/uploads/2013/07/rstudio-git3.png HTTP/1.1" 304 0 "-" "Mozilla/4.0 (compatible;)"
183.49.46.228 - - [18/Sep/2013:06:49:23 +0000] "-" 400 0 "-" "-"
163.177.71.12 - - [18/Sep/2013:06:49:33 +0000] "HEAD / HTTP/1.1" 200 20 "-" "DNSPod-Monitor/1.0"
163.177.71.12 - - [18/Sep/2013:06:49:36 +0000] "HEAD / HTTP/1.1" 200 20 "-" "DNSPod-Monitor/1.0"
101.226.68.137 - - [18/Sep/2013:06:49:42 +0000] "HEAD / HTTP/1.1" 200 20 "-" "DNSPod-Monitor/1.0"
101.226.68.137 - - [18/Sep/2013:06:49:45 +0000] "HEAD / HTTP/1.1" 200 20 "-" "DNSPod-Monitor/1.0"
60.208.6.156 - - [18/Sep/2013:06:49:48 +0000] "GET /wp-content/uploads/2013/07/rcassandra.png HTTP/1.0" 200 185524 "http://cos.name/category/software/packages/" "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36"
222.68.172.190 - - [18/Sep/2013:06:49:57 +0000] "GET /images/my.jpg HTTP/1.1" 200 19939 "http://www.angularjs.cn/A00n" "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.66 Safari/537.36"
222.68.172.190 - - [18/Sep/2013:06:50:08 +0000] "-" 400 0 "-" "-"
```

​	需求：

​		求出Pv：页面访问量，用户每点击一次都会产生一条点击日志，一共计算有多少行的点击日志数据；

​		求出Uv：用户访问量，针对Ip地址去重之后得到结果；

​		求出TopK：访问的网站求解出用户访问网站的前几名。

​	准备步骤：
​		1-准备SparkContext的环境；

​		2-读取网站日志数据，通过空格分隔符进行分割；

​		3-计算Pv，统计有多少行，一行就算做1次Pv；

​		4-计算Uv，筛选出ip，统计去重后Ip；

​		5-计算topk，筛选出对应业务的topk。

```python
# -*- coding: utf-8 -*-
# Program function：完成网站访问指标的统计，Pv，Uv，TopK
'''
* 1-准备SparkContext的环境
* 2-读取网站日志数据，通过空格分隔符进行分割
* 3-计算Pv，统计有多少行，一行就算做1次Pv
* 4-计算Uv，筛选出ip，统计去重后Ip
* 5-计算topk，筛选出对应业务的topk
'''
from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
      # *1 - 准备SparkContext的环境
      conf = SparkConf().setAppName("click").setMaster("local[*]")
      sc = SparkContext.getOrCreate(conf=conf)
      sc.setLogLevel("WARN")  # 直接将log4j放入文件夹中
      # *2 - 读取网站日志数据，通过空格分隔符进行分割
      file_rdd = sc.textFile("/home/data/click/access.log")
      # *3 - 计算Pv，统计有多少行，一行就算做1次Pv
      rdd_map_rdd = file_rdd.map(lambda line: ("pv", 1))
      print("pv result is:", rdd_map_rdd.reduceByKey(lambda x, y: x + y).collect())  # pv result is: [('pv', 14619)]
      # *4 - 计算Uv，筛选出ip，统计去重后Ip
      # file_rdd_map = file_rdd.map(lambda line: line.split(" ")[0])
      file_rdd_map = file_rdd \
          .map(lambda line: line.split(" ")) \
          .map(lambda x: x[0])
      # print(file_rdd_map.take(5))
      uv_num = file_rdd_map \
          .distinct() \
          .map(lambda line: ("uv", 1))
      print("uvCount:", uv_num.reduceByKey(lambda x, y: x + y).collect())  # uvCount: [('uv', 1051)]
      # *5 - 计算topk，筛选出对应业务的topk,访问网站【10下标】的Topk,"需要使用\"-\"
      re = file_rdd \
          .map(lambda x: x.split(" ")) \
          .filter(lambda line: len(line) > 10) \
          .map(lambda line: (line[10], 1)) \
          .reduceByKey(lambda x, y: x + y) \
          .sortBy(lambda x: x[1], False) \
          .filter(lambda x: x[0] != "\"-\"")
      print(re.take(10))
      re1 = file_rdd \
          .map(lambda x: x.split(" ")) \
          .filter(lambda line: len(line) > 10) \
          .map(lambda line: (line[10], 1)) \
          .groupByKey()\
          .mapValues(sum) \
          .sortBy(lambda x: x[1], False) \
          .filter(lambd、a x: x[0] != "\"-\"")
      print(re1.take(10))
```

# 7. Spark内核调度

​	Spark的核心是根据RDD来实现的，Spark Scheduler则为Spark核心实现的重要一环，其作用就是任务调度。Spark的任务调度就是**如何组织任务去处理RDD中每个分区的数据，根据RDD的依赖关系构建DAG[有向无环图]，基于DAG划分Stage，将每个Stage中的任务发到指定节点运行**。基于Spark的任务调度原理，可以合理规划资源利用，做到尽可能用最少的资源高效地完成任务计算。

​	以词频统计WordCount程序为例，Job执行是DAG图：

<img src=".\1-SparkBase-Core.assets\image-20230601150359628.png" alt="image-20230601150359628" style="zoom:67%;" />	

## 7.1 RDD依赖

​	RDD 的容错机制是通过将 RDD 间转移操作构建成有向无环图来实现的。从抽象的角度看，RDD 间存在着血统继承关系，其本质上是 RDD之间的依赖（Dependency）关系。

​	从图的角度看，**RDD 为节点，在一次转换操作中，创建得到的新 RDD 称为子 RDD，同时会产生新的边，即依赖关系，子 RDD 依赖向上依赖的 RDD 便是父 RDD，可能会存在多个父 RDD。**可以将这种依赖关系进一步分为两类，分别是窄依赖（NarrowDependency）和 Shuffle 依赖（Shuffle Dependency 在部分文献中也被称为 Wide Dependency，即宽依赖）。

<img src=".\1-SparkBase-Core.assets\image-20230601150915239.png" alt="image-20230601150915239" style="zoom:50%;" />

### 7.1.1 为什么要设计宽窄依赖

**对于窄依赖**

​	Spark可以并行计算;

​	如果有一个分区数据丢失，只需要从父RDD的对应1个分区重新计算即可，不需要重新计算整个任务，提高容错。

**对于宽依赖**

​	是划分Stage的依据。

**构建Lineage血缘关系**

​	RDD只支持粗粒度转换，即只记录单个块上执行的单个操作。将创建RDD的一系列Lineage（即血统）记录下来，以便恢复丢失的分区。RDD的Lineage会**记录RDD的元数据信息和转换行为**，当该RDD的部分分区数据丢失时，它可以根据这些信息来重新运算和恢复丢失的数据分区。

### 7.1.2 窄依赖（Narrow Dependency）

​	窄依赖中：**即父 RDD 与子 RDD 间的分区是一对一的**。换句话说父RDD中，一个分区内的数据是不能被分割的，只能由子RDD中的一个分区整个利用。

<img src=".\1-SparkBase-Core.assets\image-20230601151151679.png" alt="image-20230601151151679" style="zoom:67%;" />

​	上图中 P代表 RDD中的每个分区（Partition），我们看到，RDD 中每个分区内的数据在上面的几种转移操作之后被一个分区所使用，即其依赖的父分区只有一个。比如图中的 map、union 和 join 操作，都是窄依赖的。注意，join 操作比较特殊，可能同时存在宽、窄依赖。

### 7.1.3 Shuffle 依赖（宽依赖 Wide Dependency）

​	Shuffle 有“洗牌、搅乱”的意思，这里所谓的 **Shuffle 依赖也会打乱原 RDD 结构的操作**。具体来说**，父 RDD 中的分区可能会被多个子 RDD 分区使用**。因为父 RDD 中一个分区内的数据会被分割并发送给子 RDD 的所有分区，因此 Shuffle 依赖也意味着父 RDD与子 RDD 之间存在着 Shuffle 过程。

<img src=".\1-SparkBase-Core.assets\image-20230601151242746.png" alt="image-20230601151242746" style="zoom:67%;" />

​	上图中 P 代表 RDD 中的多个分区，我们会发现对于 Shuffle 类操作而言，结果 RDD 中的每个分区可能会依赖多个父 RDD 中的分区。需要说明的是，依赖关系是 RDD 到 RDD 之间的一种映射关系，是两个 RDD 之间的依赖，如果在一次操作中涉及多个父 RDD，也有可能同时包含窄依赖和 Shuffle 依赖。

### 7.1.4 如何区分宽窄依赖

​	区分RDD之间的依赖为宽依赖还是窄依赖，主要在于父RDD分区数据与子RDD分区数据关系：

​	**窄依赖：**父RDD的一个分区只会被子RDD的一个分区依赖；

​	**对于窄依赖来说**，Spark可以并行计算，如果有一个分区数据丢失，只需要从父RDD的对应个分区重新计算即可，不需要重新计算整个任务，提高容错。

​	**宽依赖**：父RDD的一个分区会被子RDD的多个分区依赖，涉及Shuffle；

​	**对应宽依赖来说**，划分Stage的依据，产生Shuffle。



## 7.2 DAG和Stage

### 7.2.1 什么是DAG

​	在图论中，**如果一个有向图无法从任意顶点出发经过若干条边回到该点**，则这个图是一个有向无环图（DAG图）。而在Spark中，由于计算过程很多时候会有先后顺序，受制于某些任务必须比另一些任务较早执行的限制，必须对任务进行排队，形成一个队列的任务集合，这个队列的任务集合就是DAG图，**每一个定点就是一个任务，每一条边代表一种限制约束（Spark中的依赖关系）**。

<img src=".\1-SparkBase-Core.assets\image-20230601151613756.png" alt="image-20230601151613756" style="zoom:50%;" />

​	Spark中DAG生成过程的重点是**对Stage的划分**，其划分的依据是RDD的依赖关系，对于不同的依赖关系，高层调度器会进行不同的处理。

​	**对于窄依赖**，RDD之间的数据不需要进行Shuffle，**多个数据处理可以在同一台机器的内存中完成，所以窄依赖在Spark中被划分为同一个Stage**；

​	**对于宽依赖**，由于Shuffle的存在，必须等到父RDD的Shuffle处理完成后，才能开始接下来的计算，所以会在此处进行Stage的切分。

<img src=".\1-SparkBase-Core.assets\image-20230601151655789.png" alt="image-20230601151655789" style="zoom:50%;" />

​	在Spark中，DAG生成的流程关键在于**回溯**，在程序提交后，高层调度器将所有的RDD看成是一个Stage，然后对此Stage进行从后往前的回溯，遇到Shuffle就断开，遇到窄依赖，则归并到同一个Stage。等到所有的步骤回溯完成，便生成一个DAG图。

<img src=".\1-SparkBase-Core.assets\image-20230601151722375.png" alt="image-20230601151722375" style="zoom:57%;" />

​	把DAG划分成互相依赖的多个Stage，划分依据是RDD之间的宽依赖，Stage是由一组并行的Task组成。**Stage切割规则：从后往前，遇到宽依赖就切割Stage。**Stage计算模式：**pipeline管道计算模式**，pipeline只是一种计算思想、模式，来一条数据然后计算一条数据，把所有的逻辑走完，然后落地。准确的说：**一个task处理一串分区的数据，整个计算逻辑全部走完**。

<img src=".\1-SparkBase-Core.assets\image-20230601151802065.png" alt="image-20230601151802065" style="zoom:67%;" />



### 7.2.2 DAG如何划分Stage

<img src=".\1-SparkBase-Core.assets\image-20230601151906252.png" alt="image-20230601151906252" style="zoom:67%;" />

​	为什么要划分Stage? --**并行计算**

​	一个复杂的业务逻辑如果有shuffle，那么就意味着前面阶段产生结果后，才能执行下一个阶段，即**下一个阶段的计算要依赖上一个阶段的数据**。那么我们按照shuffle进行划分(也就是按照宽依赖就行划分)，**就可以将一个DAG划分成多个Stage/阶段，在同一个Stage中，会有多个算子操作，可以形成一个pipeline流水线，流水线内的多个平行的分区可以并行执行。**

​	**Pipeline：HDFS----textRDD----splitRDD-----tupleRDD**

​	如何划分DAG的stage？

​	对于窄依赖，partition的转换处理在stage中完成计算，**不划分**(将窄依赖尽量放在在同一个stage中，可以实现流水线计算)；

​	对于宽依赖，由于有shuffle的存在，只能在父RDD处理完成后，才能开始接下来的计算，也就是说需要要**划分stage**。

**总结：**

​	Spark会根据shuffle/宽依赖使用回溯算法来对DAG进行Stage划分，从后往前，遇到宽依赖就断开，遇到窄依赖就把当前的RDD加入到当前的stage/阶段中。

## 7.3 Spark Shuffle

### 7.3.1 MR的Shuffle回顾

​	首先回顾MapReduce框架中Shuffle过程，整体流程图如下：

<img src=".\1-SparkBase-Core.assets\image-20230601154126270.png" alt="image-20230601154126270" style="zoom:67%;" />



### 7.3.2 Spark的Shuffle简介

​	Spark在DAG调度阶段会将**一个Job划分为多个Stage，上游Stage做map工作，下游Stage做reduce工作，其本质上还是MapReduce计算框架**。Shuffle是连接map和reduce之间的桥梁，它将map的输出对应到reduce输入中，涉及到序列化反序列化、跨节点网络IO以及磁盘读写IO等。

<img src=".\1-SparkBase-Core.assets\image-20230601154414104.png" alt="image-20230601154414104" style="zoom:67%;" />

​	Spark的Shuffle分为**Write和Read两个阶段，分属于两个不同的Stage**，前者是Parent Stage的最后一步，后者是Child Stage的第一步。

<img src=".\1-SparkBase-Core.assets\image-20230601154835559.png" alt="image-20230601154835559" style="zoom:67%;" />

​	执行Shuffle的主体是Stage中的并发任务，这些**任务分ShuffleMapTask和ResultTask**两种，ShuffleMapTask要进行Shuffle，ResultTask负责返回计算结果，一个Job中只有最后的Stage采用ResultTask，其他的均为ShuffleMapTask。如果要按照map端和reduce端来分析的话，ShuffleMapTask可以即是map端任务，又是reduce端任务，因为Spark中的Shuffle是可以串行的；ResultTask则只能充当reduce端任务的角色。

​	Spark在1.1以前的版本一直是采用**Hash Shuffle**的实现的方式，到1.1版本时**参考Hadoop MapReduce**的实现开始引入**Sort Shuffle**，在1.5版本时开始**Tungsten钨丝计划，引入UnSafe Shuffle优化内存及CPU的使用**，在1.6中将**Tungsten统一到Sort Shuffle中**，实现自我感知选择最佳Shuffle方式，到的**2.0版本，Hash Shuffle已被删除，所有Shuffle方式全部统一到Sort Shuffle**一个实现中。

<img src=".\1-SparkBase-Core.assets\image-20230601154912732.png" alt="image-20230601154912732" style="zoom:60%;" />



​	具体各阶段Shuffle如何实现，参考思维导图XMIND，大纲如下：

<img src=".\1-SparkBase-Core.assets\image-20230601154952549.png" alt="image-20230601154952549" style="zoom:67%;" />

​	在Spark的中，负责shuffle过程的执行、计算和处理的[组件](https://www.2cto.com/kf/all/zujian/)主要就是ShuffleManager，也即shuffle管理器。ShuffleManager随着Spark的发展有两种实现的方式，分别为HashShuffleManager和SortShuffleManager，因此spark的Shuffle有Hash Shuffle和Sort Shuffle两种。

​	在Spark 1.2以前，默认的shuffle计算引擎是HashShuffleManager。该ShuffleManager而HashShuffleManager有着一个非常严重的弊端，就是会产生大量的中间磁盘文件，进而由大量的磁盘IO操作影响了性能。因此在Spark 1.2以后的版本中，默认的ShuffleManager改成了SortShuffleManager。SortShuffleManager相较于HashShuffleManager来说，有了一定的改进。主要就在于，每个Task在进行shuffle操作时，虽然也会产生较多的临时磁盘文件，但是最后会将所有的临时文件合并(merge)成一个磁盘文件，因此每个Task就只有一个磁盘文件。在下一个stage的shuffle read task拉取自己的数据时，只要根据索引读取每个磁盘文件中的部分数据即可。

### 7.3.3 HashShuffle图解[了解]

**Shuffle阶段划分：**

​	shuffle write：mapper阶段，上一个stage得到最后的结果写出；

​	shuffle read ：reduce阶段，下一个stage拉取上一个stage进行合并。

**1)未经优化的hashShuffleManager：**

​	**首先1个cpu里面建议设置2到3倍的task**，根据下游的task决定生成几个文件，先生成缓冲区文件在写入磁盘文件，在将block文件进行合并。对相同的key执行hash算法，从而将相同的key都写入到一个磁盘文件中，而每一个磁盘文件都只属于下游stage的一个task。每个文件中只存储key取hash之后相同的数据，导致了当下游的task任务过多的时候，上游会堆积大量的小文件。

​	HashShuffle是根据task的计算结果的key值的hashcode%ReduceTask来决定放入哪一个区分，这样保证相同的数据一定放入一个分区，Hash Shuffle过程如下：

<img src=".\1-SparkBase-Core.assets\image-20230601155236642.png" alt="image-20230601155236642" style="zoom:60%;" />

​	根据下游的task决定生成几个文件，先生成缓冲区文件在写入磁盘文件，再将block文件进行合并。未经优化的shuffle write操作所产生的磁盘文件的数量是极其惊人的。

**2)经过优化的hashShuffleManager：**

​	在shuffle write过程中，task就不是为下游stage的每个task创建一个磁盘文件了。此时会出现shuffleFileGroup的概念，每个shuffleFileGroup会对应一批磁盘文件，每一个Group磁盘文件的数量与下游stage的task数量是相同的。而第一批并行执行的每个task都会创建一个shuffleFileGroup，并将数据写入对应的磁盘文件内。当Executor的CPU core执行完一批task，接着执行下一批task时，下一批task就会复用之前已有的shuffleFileGroup，包括其中的磁盘文件。也就是说，此时task会将数据写入已有的磁盘文件中，而不会写入新的磁盘文件中。因此，consolidate机制允许不同的task复用同一批磁盘文件，这样就可以有效将多个task的磁盘文件进行一定程度上的合并，从而大幅度减少磁盘文件的数量，进而提升shuffle write的性能。

​	设置配置consolidateFiles调整为true。（当然，默认是开启的）

<img src=".\1-SparkBase-Core.assets\image-20230601155357481.png" alt="image-20230601155357481" style="zoom:60%;" />

​	开启consolidate机制之后，在shuffle write过程中，task就不是为下游stage的每个task创建一个磁盘文件了。此时会出现shuffleFileGroup的概念，每个shuffleFileGroup会对应一批磁盘文件。

**总结：**

未经优化：

​	上游的task数量：m

​	下游的task数量：n

​	上游的executor数量：k (m>=k)

​	总共的磁盘文件：m*n

优化之后的：

​	上游的task数量：m

​	下游的task数量：n

​	上游的executor数量：k (m>=k)

​	总共的磁盘文件：k*n

### 7.3.4 SortShuffleManager基本[了解]

​	SortShuffleManager的运行机制主要分成两种，一种是普通运行机制，另一种是bypass运行机制。当shuffle write task的数量小于等于spark.shuffle.sort.bypassMergeThreshold参数的值时(**默认为200**)，就会启用bypass机制。

#### 7.3.4.1 SortShuffle的普通机制

<img src=".\1-SparkBase-Core.assets\image-20230601155929339.png" alt="image-20230601155929339" style="zoom:67%;" />

（1）该模式下，数据会先写入一个内存数据结构中(默认5M)，此时根据不同的shuffle算子，可能选用不同的数据结构。如果是reduceByKey这种聚合类的shuffle算子，那么会选用Map数据结构，一边通过Map进行聚合，一边写入内存;如果是join这种普通的shuffle算子，那么会选用Array数据结构，直接写入内存。

（2）接着，每写一条数据进入内存数据结构之后，就会判断一下，是否达到了某个临界阈值。如果达到临界阈值的话，那么就会尝试将内存数据结构中的数据溢写到磁盘，然后清空内存数据结构。

​	注意：

​	shuffle中的定时器：定时器会检查内存数据结构的大小，如果内存数据结构空间不够，那么会申请额外的内存，申请的大小满足如下公式：

​		applyMemory=nowMenory*2-oldMemory

​	申请的内存=当前的数据内存情况*2-上一次的内嵌情况

​	意思就是说内存数据结构的大小的动态变化，如果存储的数据超出内存数据结构的大小，将申请内存数据结构存储的数据*2-内存数据结构的设定值的内存大小空间。申请到了，内存数据结构的大小变大，内存不够，申请不到，则发生溢写。

​	由于Spark是一个内存计算框架，没有办法严格控制Executor内存，只能采用监控方式监控内存，**内存初始值为5M，当超出的时候，如5.02M，监控内存数据的对象会去申请5.02\*2-5=5.04M内存，**如果申请到了就不需要溢写，否则会发生溢写。

​	区别：

​		（a）Spark内存数据初始值为5M，他可以申请扩大，而MR固定的Buffer为100M

​		（b）溢写磁盘文件还带有索引文件，索引文件是对磁盘文件的描述，还记录每个分区的起始位置**start offset**和终止位置**end offset**。

（3）排序

​	在溢写到磁盘文件之前，会先根据key对内存数据结构中已有的数据进行排序。

（4）溢写

​	排序过后，会分批将数据写入磁盘文件。**默认的batch数量是10000条，也就是说，排序好的数据，会以每批1万条数据的形式分批写入磁盘文件。**写入磁盘文件是通过[Java](https://www.2cto.com/kf/ware/Java/)的BufferedOutputStream实现的。BufferedOutputStream是Java的缓冲输出流，首先会将数据缓冲在内存中，当内存缓冲满溢之后再一次写入磁盘文件中，这样可以减少磁盘IO次数，提升性能。

（5）merge

​	**一个task**将所有数据写入内存数据结构的过程中，会发生多次磁盘溢写操作，也就会产生多个临时文件。最后会将之前所有的临时磁盘文件都进行合并成1个磁盘文件，这就是merge过程，此时会将之前所有临时磁盘文件中的数据读取出来，然后依次写入最终的磁盘文件之中。此外，由于一个task就只对应一个磁盘文件，也就意味着该task为Reduce端的stage的task准备的数据都在这一个文件中，**因此还会单独写一份索引文件，其中标识了下游各个task的数据在文件中的start offset与end offset。**

​	SortShuffleManager由于有一个磁盘文件merge的过程，因此大大减少了文件数量。比如第一个stage有50个task，总共有10个Executor，每个Executor执行5个task，而第二个stage有100个task。由于每个task最终只有一个磁盘文件，因此此时每个Executor上只有5个磁盘文件，所有Executor只有50个磁盘文件。

#### 7.3.4.2 Sort shuffle的bypass机制

<img src=".\1-SparkBase-Core.assets\image-20230601160121880.png" alt="image-20230601160121880" style="zoom:60%;" />

bypass运行机制的触发条件如下：

​	**1)shuffle map task数量小于spark.shuffle.sort.bypassMergeThreshold=200参数的值。**

​	**2)不是map combine聚合的shuffle算子(比如reduceByKey有map combie)。**

​	此时task会为每个reduce端的task都创建一个临时磁盘文件，并将数据按key进行hash，然后根据key的hash值，将key写入对应的磁盘文件之中。当然，写入磁盘文件时也是先写入内存缓冲，缓冲写满之后再溢写到磁盘文件的。最后，同样会将所有临时磁盘文件都合并成一个磁盘文件，并创建一个单独的索引文件。

​	该过程的磁盘写机制其实跟未经优化的HashShuffleManager是一模一样的，因为都要创建数量惊人的磁盘文件，只是在最后会做一个磁盘文件的合并而已。因此少量的最终磁盘文件，也让该机制相对未经优化的HashShuffleManager来说，shuffle read的性能会更好。

​	而该机制与普通SortShuffleManager运行机制的不同在于：

​		**第一，磁盘写机制不同;**

​		**第二，不会进行排序。也就是说，启用该机制的最大好处在于，shuffle write过程中，不需要进行数据的排序操作，也就节省掉了这部分的性能开销。**

​	**总结：**SortShuffle也分为普通机制和bypass机制，普通机制在内存数据结构(默认为5M)完成排序，会产生2M个磁盘小文件。而当shuffle map task数量小于spark.shuffle.sort.bypassMergeThreshold参数的值。或者算子不是聚合类的shuffle算子(比如reduceByKey)的时候会触发SortShuffle的bypass机制，SortShuffle的bypass机制不会进行排序，极大的提高了其性能。

### 7.3.5 Shuffle的配置选项

spark的shuffle配置选项[http://spark.apache.org/docs/3.1.2/configuration.html#shuffle-behavior](http://spark.apache.org/docs/2.2.0/configuration.html#shuffle-behavior)]

**Shuffle阶段划分：**

​		shuffle write：mapper阶段，上一个stage得到最后的结果写出
​		shuffle read ：reduce阶段，下一个stage拉取上一个stage进行合并

 （1）**SortShuffleManager-普通机制**：
		 1，在普通模式下，数据会先写入一个内存数据结构中，此时根据不同的shuffle算子，可以选用不同的数据结构。如果是由聚合操作的shuffle算子，就是用map的数据结构（边聚合边写入内存），如果是join的算子，就使用array的数据结构（直接写入内存）。
 		2，接着，每写一条数据进入内存数据结构之后，就会判断是否达到了某个临界值，如果达到了临界值的话，就会尝试的将内存数据结构中的数据溢写到磁盘，然后清空内存数据结构。
		 3，在溢写到磁盘文件之前，会先根据key对内存数据结构中已有的数据进行排序，排序之后，会分批将数据写入磁盘文件。默认的batch数量是10000条，也就是说，排序好的数据，会以每批次1万条数据的形式分批写入磁盘文件，写入磁盘文件是通过Java的BufferedOutputStream实现的。首先会将数据缓冲在内存中，当内存缓冲满溢之后再一次写入磁盘文件中，这样可以减少磁盘IO次数，提升性能。
 		4，此时task将所有数据写入内存数据结构的过程中，会发生多次磁盘溢写，会产生多个临时文件，最后会将之前所有的临时文件都进行合并，最后会合并成为一个大文件。最终只剩下两个文件，一个是合并之后的数据文件，一个是索引文件（标识了下游各个task的数据在文件中的start offset与end offset）。最终再由下游的task根据索引文件读取相应的数据文件。

**（2）SortShuffleManager-bypass机制：**
	 此时task会为每个下游task都创建一个临时磁盘文件，并将数据按key进行hash然后根据key的hash值，将key写入对应的磁盘文件之中。当然，写入磁盘文件时也是先写入内存缓冲，缓冲写满之后再溢写到磁盘文件的。最后，同样会将所有临时磁盘文件都合并成一个磁盘文件，并创建一个单独的索引文件。
	 bypass机制与普通SortShuffleManager运行机制的不同在于：
 		第一，磁盘写机制不同；
		 第二，不会进行排序。

​	 也就是说，启用该机制的最大好处在于，shuffle write过程中，不需要进行数据的排序操作，也就节省掉了这部分的性能开销。
 	触发bypass机制的条件：
​	shuffle map task的数量小于spark.shuffle.sort.bypassMergeThreshold参数的值（默认200）或者**不是聚合类的shuffle算子（比如groupByKey）**

```python
# 下面列出Shuffle类不同分类算子
# 去重
def distinct()
def distinct(numPartitions: Int)
# 聚合
def reduceByKey(func: (V, V) => V, numPartitions: Int): RDD[(K, V)]
def reduceByKey(partitioner: Partitioner, func: (V, V) => V): RDD[(K, V)]
def groupBy[K](f: T => K, p: Partitioner):RDD[(K, Iterable[V])]
def groupByKey(partitioner: Partitioner):RDD[(K, Iterable[V])]
def aggregateByKey[U: ClassTag](zeroValue: U, partitioner: Partitioner): RDD[(K, U)]
def aggregateByKey[U: ClassTag](zeroValue: U, numPartitions: Int): RDD[(K, U)]
def combineByKey[C](createCombiner: V => C, mergeValue: (C, V) => C, mergeCombiners: (C, C) => C): RDD[(K, C)]
def combineByKey[C](createCombiner: V => C, mergeValue: (C, V) => C, mergeCombiners: (C, C) => C, numPartitions: Int): RDD[(K, C)]
def combineByKey[C](createCombiner: V => C, mergeValue: (C, V) => C, mergeCombiners: (C, C) => C, partitioner: Partitioner, mapSideCombine: Boolean = true, serializer: Serializer = null): RDD[(K, C)]
# 排序
def sortByKey(ascending: Boolean = true, numPartitions: Int = self.partitions.length): RDD[(K, V)]
def sortBy[K](f: (T) => K, ascending: Boolean = true, numPartitions: Int = this.partitions.length)(implicit ord: Ordering[K], ctag: ClassTag[K]): RDD[T]
# 重分区
def coalesce(numPartitions: Int, shuffle: Boolean = false, partitionCoalescer: Option[PartitionCoalescer] = Option.empty)
def repartition(numPartitions: Int)(implicit ord: Ordering[T] = null)
# 集合或者表操作
def intersection(other: RDD[T]): RDD[T]
def intersection(other: RDD[T], partitioner: Partitioner)(implicit ord: Ordering[T] = null): RDD[T]
def intersection(other: RDD[T], numPartitions: Int): RDD[T]
def subtract(other: RDD[T], numPartitions: Int): RDD[T]
def subtract(other: RDD[T], p: Partitioner)(implicit ord: Ordering[T] = null): RDD[T]
def subtractByKey[W: ClassTag](other: RDD[(K, W)]): RDD[(K, V)]
def subtractByKey[W: ClassTag](other: RDD[(K, W)], numPartitions: Int): RDD[(K, V)]
def subtractByKey[W: ClassTag](other: RDD[(K, W)], p: Partitioner): RDD[(K, V)]
def join[W](other: RDD[(K, W)], partitioner: Partitioner): RDD[(K, (V, W))]
def join[W](other: RDD[(K, W)]): RDD[(K, (V, W))]
def join[W](other: RDD[(K, W)], numPartitions: Int): RDD[(K, (V, W))]
def leftOuterJoin[W](other: RDD[(K, W)]): RDD[(K, (V, Option[W]))]
```

**spark 的shuffle调优**
 	主要是调整缓冲的大小，拉取次数重试重试次数与等待时间，内存比例分配，是否进行排序操作等等**spark.shuffle.file.buffer**
	 参数说明：**该参数用于设置shuffle write task的BufferedOutputStream的buffer缓冲大小（默认是32K）**。将数据写到磁盘文件之前，会先写入buffer缓冲中，待缓冲写满之后，才会溢写到磁盘。
 	调优建议：如果作业可用的内存资源较为充足的话，可以适当增加这个参数的大小（比如64k），从而减少shuffle write过程中溢写磁盘文件的次数，也就可以减少磁盘IO次数，进而提升性能。在实践中发现，合理调节该参数，**性能会有1%~5%的提升。**
**spark.reducer.maxSizeInFlight**
 	参数说明：**该参数用于设置shuffle read task的buffer缓冲大小，而这个buffer缓冲决定了每次能够拉取多少数据。(默认48M)**
 	调优建议：如果作业可用的内存资源较为充足的话，可以适当增加这个参数的大小（比如96m），从而减少拉取数据的次数，也就可以减少网络传输的次数，进而提升性能。在实践中发现，合理调节该参数，性能会有1%~5%的提升。

**spark.shuffle.io.maxRetries** ：shuffle read task从shuffle write task所在节点拉取属于自己的数据时，**如果因为网络异常导致拉取失败，是会自动进行重试的**。该参数就代表了可以重试的最大次数。（默认是3次）
**spark.shuffle.io.retryWait：**该参数代表了每次重试拉取数据的等待间隔。（默认为5s）
 	调优建议：一般的调优都是将重试次数调高，不调整时间间隔。
 **spark.shuffle.memoryFraction****：**
	 参数说明：该参数代表了Executor内存中，分配给shuffle read task进行聚合操作内存比例。
**spark.shuffle.manager**
 	参数说明：该参数用于设置shufflemanager的类型（默认为sort）.Spark1.5x以后有三个可选项：
 	Hash：spark1.x版本的默认值，HashShuffleManager
	 Sort：spark2.x版本的默认值，普通机制，当shuffle read task 的数量小于等于spark.shuffle.sort.bypassMergeThreshold参数，自动开启bypass 机制
**spark.shuffle.sort.bypassMergeThreshold**
 	参数说明：当ShuffleManager为SortShuffleManager时，如果shuffle read task的数量小于这个阈值（默认是200），则shuffle write过程中不会进行排序操作。
 	调优建议：当你使用SortShuffleManager时，如果的确不需要排序操作，那么建议将这个参数调大一些

## 7.4 Job 调整流程

​	Spark Application应用的用户代码都是**基于RDD的一系列计算操作**，实际运行时，这些**计算操作是Lazy执行的**，并不是所有的RDD操作都会触发Spark往Cluster上提交实际作业，基本上**只有一些需要返回数据或者向外部输出的操作才会触发实际计算工作**（Action算子），其它的变换操作基本上只是生成对应的RDD记录依赖关系（Transformation算子）。

​	当启动Spark Application的时候，运行MAIN函数，首先**创建SparkContext对象（构建DAGScheduler和TaskScheduler）**。

​	第一点、**DAGScheduler**实例对象——将每个Job的DAG图划分为Stage，依据RDD之间依赖为宽依赖（产生Shuffle）

​	第二点、**TaskScheduler**实例对象——调度每个Stage中所有Task：TaskSet，发送到Executor上执行

<img src=".\1-SparkBase-Core.assets\image-20230601161109875.png" alt="image-20230601161109875" style="zoom:60%;" />

​	当RDD调用Action函数（比如count、saveTextFile或foreachPartition）时，触发一个Job执行，调度中流程如下图所示：

<img src=".\1-SparkBase-Core.assets\image-20230601161138946.png" alt="image-20230601161138946" style="zoom:60%;" />

​	Spark RDD通过其Transactions操作，形成了RDD血缘关系图，即DAG，最后通过Action的调用，触发Job并调度执行。

​	1）、**DAGScheduler负责Stage级的调度**，主要是将DAG切分成若干Stages，并将每个Stage打包成TaskSet交给TaskScheduler调度。

​	2）、**TaskScheduler负责Task级的调度**，将DAGScheduler给过来的TaskSet按照指定的调度策略分发到Executor上执行，调度过程中SchedulerBackend负责提供可用资源，其中SchedulerBackend有多种实现，分别对接不同的资源管理系统。

​	Spark的任务调度总体来说分两路进行，**一路是Stage级的调度，一路是Task级的调度**。

<img src=".\1-SparkBase-Core.assets\image-20230601161219697.png" alt="image-20230601161219697" style="zoom:50%;" />

​	一个Spark应用程序包括Job、Stage及Task：

​		第一：Job是以Action方法为界，遇到一个Action方法则触发一个Job；

​		第二：Stage是Job的子集，以RDD宽依赖(即Shuffle)为界，遇到Shuffle做一次划分；

​		第三：Task是Stage的子集，以并行度(分区数)来衡量，分区数是多少，则有多少个task。



## 7.5 Spark基本概念

​	Spark Application运行时，涵盖很多概念，主要如下表格：

<img src=".\1-SparkBase-Core.assets\image-20230601161312912.png" alt="image-20230601161312912" style="zoom:60%;" />

官方文档：http://spark.apache.org/docs/2.4.5/cluster-overview.html#glossary

l **Application**：指的是用户编写的Spark应用程序/代码，包含了Driver功能代码和分布在集群中多个节点上运行的Executor代码；

l  **Driver**：Spark中的Driver即运行上述Application的Main()函数并且创建SparkContext，SparkContext负责和ClusterManager通信，进行资源的申请、任务的分配和监控等；

l  **Cluster Manager**：指的是在集群上获取资源的外部服务，Standalone模式下由Master负责，Yarn模式下ResourceManager负责;

l  **Executor**：是运行在工作节点Worker上的进程，负责运行任务，并为应用程序存储数据，是执行分区计算任务的进程；

l  **RDD**：Resilient Distributed Dataset弹性分布式数据集，是分布式内存的一个抽象概念；

l  **DAG**：Directed Acyclic Graph有向无环图，反映RDD之间的依赖关系和执行流程；

l  **Job**：作业，按照DAG执行就是一个作业，Job==DAG；

l  **Stage**：阶段，是作业的基本调度单位，同一个Stage中的Task可以并行执行，多个Task组成TaskSet任务集；

l  **Task**：任务，运行在Executor上的工作单元，1个Task计算1个分区，包括pipline上的一系列操作；

## 7.6 Spark并行度

### 7.6.1 资源并行度与数据并行度

​	在Spark Application运行时，并行度可以从两个方面理解：	

​		 1）资源的并行度：由节点数(executor)和cpu数(core)决定的

​		 2）数据的并行度：task的数据，partition大小

​	task又分为map时的task和reduce(shuffle)时的task；

​	task的数目和很多因素有关，资源的总core数，spark.default.parallelism参数，spark.sql.shuffle.partitions参数，读取数据源的类型,shuffle方法的第二个参数,repartition的数目等等。

​	如果Task的数量多，能用的资源也多，那么并行度自然就好。如果Task的数据少，资源很多，有一定的浪费，但是也还好。如果Task数目很多，但是资源少，那么会执行完一批，再执行下一批。所以官方给出的建议是，这个**Task数目要是core总数的2-3倍为佳**。如果core有多少Task就有多少，那么有些比较快的task执行完了，一些资源就会处于等待的状态。

### 7.6.2 设置Task数量

​	将Task数量设置成与Application总CPU Core 数量相同（理想情况，150个core，分配150 Task）官方推荐，**Task数量，设置成Application总CPU Core数量的2~3倍（150个cpu core，设置task数量为300~500）**与理想情况不同的是：有些Task会运行快一点，比如50s就完了，有些Task可能会慢一点，要一分半才运行完，所以如果你的Task数量，刚好设置的跟CPU Core数量相同，也可能会导致资源的浪费，比如150 Task，10个先运行完了，剩余140个还在运行，但是这个时候，就有10个CPU Core空闲出来了，导致浪费。如果设置2~3倍，那么一个Task运行完以后，另外一个Task马上补上来，尽量让CPU Core不要空闲。

### 7.6.3 设置Application的并行度

​	参数**spark.defalut.parallelism**默认是没有值的，如果设置了值，是在shuffle的过程才会起作用

​	定义如下：

<img src=".\1-SparkBase-Core.assets\image-20230601162007531.png" alt="image-20230601162007531" style="zoom:50%;" />

​	代码设置如下：

<img src=".\1-SparkBase-Core.assets\image-20230601162031976.png" alt="image-20230601162031976" style="zoom:50%;" />

​	测试：

```python
from pyspark import SparkContext, SparkConf
import os

os.environ['SPARK_HOME'] = '/home/app/spark'
PYSPARK_PYTHON = "/root/anaconda3/envs/pyspark_env/bin/python"
# 当存在多个版本时，不指定很可能会导致出错
os.environ["PYSPARK_PYTHON"] = PYSPARK_PYTHON
os.environ["PYSPARK_DRIVER_PYTHON"] = PYSPARK_PYTHON

if __name__ == '__main__':
    print('PySpark First Program')
    # 输入数据
    data = ["hello", "world", "hello", "world"]
    conf = SparkConf().setAppName("miniProject").setMaster("local[*]")
    conf.set("spark.defalut.parallelism", 4)
    conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
    # sc = SparkContext.getOrCreate(conf)
    sc = SparkContext(conf=conf)
    # 将collection的data转为spark中的rdd并进行操作
    rdd = sc.parallelize(data)
    # rdd = sc.textFile("file:///export/pyfolder1/pyspark-chapter02_3.8/data/word.txt") \
    #    .flatMap(lambda line: line.split(" "))
    print("rdd numpartitions:", rdd.getNumPartitions())
    # 执行map转化操作以及reduceByKey的聚合操作
    res_rdd = rdd.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)
    # 并行度决定了可以同时处理多少个分区
    print("shuffle numpartitions:", res_rdd.getNumPartitions())
    print('停止 PySpark SparkSession 对象')
    sc.stop()
```

### 7.6.4 案例说明

​	当提交一个Spark Application时，设置资源信息如下，基本已经达到了集群或者yarn队列的资源上限：

<img src=".\1-SparkBase-Core.assets\image-20230601162305286.png" alt="image-20230601162305286" style="zoom:60%;" />

​	**Task没有设置或者设置的很少，比如为100个task** ，平均分配一下，每个executor 分配到2个task，每个executor 剩下的一个cpu core 就浪费掉了！

​	虽然分配充足了，但是问题是：并行度没有与资源相匹配，导致你分配下去的资源都浪费掉了。**合理的并行度的设置，应该要设置的足够大，大到可以完全合理的利用你的集群资源。**可以调整Task数目，按照原则：**Task数量，设置成Application总CPU Core数量的2~3倍**

<img src=".\1-SparkBase-Core.assets\image-20230601162340945.png" alt="image-20230601162340945" style="zoom:67%;" />

​	实际项目中，往往依据数据量（Task数目）配置资源。

## 7.7 万能的combineByKey

​	combineByKey是Spark中一个比较核心的高级且底层函数，其他一些高阶键值对函数底层都是用它实现的。诸如 groupByKey,reduceByKey等等。

​	l 如下解释下3个重要的函数参数：

​	l createCombiner: V => C ，**这个函数把当前的值作为参数**，此时我们可以对其做些附加操作(类型转换)并把它返回 (这一步类似于初始化操作)

​	l mergeValue: (C, V) => C，**该函数把元素V合并到之前的元素C(createCombiner)上** (这个操作在每个分区内进行)

​	l mergeCombiners: (C, C) => C，**该函数把2个元素C合并** (这个操作在不同分区间进行)。

<img src=".\1-SparkBase-Core.assets\image-20230601163021397.png" alt="image-20230601163021397" style="zoom:60%;" />

案例1：实现将相同Key的Value进行合并，使用groupBy很容易实现

```python
# -*- coding: utf-8 -*-
# Program function：外部集合转为RDD
from pyspark import SparkConf, SparkContext
import re

# 1-准备环境
conf = SparkConf().setAppName("collection").setMaster("local[*]")
sc = SparkContext(conf=conf)
sc.setLogLevel("WARN")

x = sc.parallelize([("a", 1), ("b", 1), ("a", 2)])
def to_list(a):
    return [a]

def append(a, b):
    a.append(b)
    return a

def extend(a, b):
    a.extend(b)
    return a
print(sorted(x.combineByKey(to_list, append, extend).collect()))
#[('a', [1, 2]), ('b', [1])]
```

案例2：求解平均分的案例

​	要求：对数据集按照 Key 进行聚合

​	调用：combineByKey(createCombiner, mergeValue, mergeCombiners, [partitioner], [mapSideCombiner], [serializer])

​	参数：

​		l createCombiner 将 Value 进行初步转换

​		l mergeValue **在每个分区把上一步转换的结果聚合**

​		l mergeCombiners 在所有分区上把每个分区的聚合结果聚合

​		l partitioner 可选, 分区函数

​		l mapSideCombiner 可选, 是否在 Map 端 Combine

​		l serializer 序列化器

​	注意点：

​		l combineByKey 的要点就是三个函数的意义要理解

​		l groupByKey, reduceByKey 的底层都是 combineByKey

```python
# -*- coding: utf-8 -*-
# Program function：外部集合转为RDD
from pyspark import SparkConf, SparkContext
import re

# 1-准备环境
conf = SparkConf().setAppName("collection").setMaster("local[*]")
sc = SparkContext(conf=conf)
sc.setLogLevel("WARN")

x = sc.parallelize([("Fred", 88), ("Fred", 95), ("Fred", 91), ("Wilma", 93), ("Wilma", 95), ("Wilma", 98)])

# (v)=>(v,1)，得到的是（88,1），因为这是combineByKey是按照key处理value操作，
# acc:(Int,Int)代表的是(88,1),其中acc._1代表的是88，acc._2代表1值，v代表是同为Fred名称的95的数值，
# 所以acc._1+v=88+95,即相同Key的Value相加结果，第三个参数是分区间的相同key的value进行累加，
# 得到Fred的88+95+91，Wilma累加和为93+95+98。
def createCombiner(a):
    return [a, 1]
def mergeValue(a, b):
    return [a[0] + b, a[1] + 1]
def mergeCombiners(a, b):
    return [a[0] + b[0], a[1] + b[1]]
resultKey = x.combineByKey(createCombiner, mergeValue, mergeCombiners)
print(sorted(resultKey.collect()))
# [('Fred', [274, 3]), ('Wilma', [286, 3])]
print(resultKey.map(lambda score: (score[0], int(score[1][0]) / int(score[1][1]))).collect())
# [('Fred', 91.33333333333333), ('Wilma', 95.33333333333333)]
#lambda表达式版本
resultKey = x.combineByKey(lambda x:[x,1], lambda x,y:[x[0]+y,x[1]+1], lambda x,y:[x[0]+y[0],x[1]+y[1]])
print(sorted(resultKey.collect()))
```

