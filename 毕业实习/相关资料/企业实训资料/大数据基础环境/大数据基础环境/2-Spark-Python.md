# Spark-Python

# 1. PyCharm环境

## 1.1 解压安装包

​	解压Spark安装包到Windows本地路径，路径中最好没有空格。

<img src=".\image\image-20220901090018647.png" alt="image-20220901090018647" style="zoom:40%;" />



## 1.2 Linux安装Python

​	上传Anaconda-Linux安装文件到虚拟机，不需要解压，直接使用bash命令即可运行。文件来自于[https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/]

```shell
#安装插件
yum install -y bzip2

#安装命令
bash Anaconda3-5.2.0-Linux-x86_64.sh
```

​	默认安装路径为“/root/anaconda3”，可自行输入进行修改到空地址，输出的路径必须为不存在，否则会报如下错。

```shell
ERROR: File or directory already exists: '/root/anaconda3'
```

​	安装进行中，一直“yes”，最后一个不行了就“no”，安装完成后，生效环境变量。

```shell
#安装过程中，会默认写入bashrc环境变量中，也可以自行写入/etc/profile
source ~/.bashrc

#命令行输出Python，查看结果
python
```

![image-20220901092014090](.\image\image-20220901092014090.png)



## 1.3 Python版本选择

​	选择与Liunx同一个版本的Anaconda安装包，选择与Linux相同的Python版本，避免报错。

<img src=".\image\image-20220901092913816.png" alt="image-20220901092913816" style="zoom:40%;" />



## 1.4 配置依赖

​	选择菜单栏“File” --->"Settings" —>“Project Structure ”命令，快捷键为“ctrl+alt+shift+s”打开如图所示界面

<img src=".\image\image-20220901085639615.png" alt="image-2022090185639615" style="zoom:60%;" />

​	导包成功

<img src=".\image\image-20220901090259083.png" alt="image-20220901090259083" style="zoom:60%;" />



## 1.5 引入spark-core包

​	将Spark解压路径【spark-2.4.1-bin-hadoop2.7\python】下的【pyspark、pyspark.egg-info】，拷贝到Ananconda安装路径【Anaconda3\Lib\site-packages】下。

​    注：此处版本为Spark2.x，Spark3.x的Python支持库只有【pyspark】，其余步骤一样，不影响。

<img src=".\image\image-20220901093928488.png" alt="image-20220901093928488" style="zoom:60%;" />



## 1.6 添加系统环境变量

​	在Windows的系统环境变量中，新建SPARK_HOME, 添加解压后的Spark文件地址。

![image-20230202105144068](.\image\image-20230202105144068.png)



## 1.7 本地环境测试

​	使用简单WordCount代码进行环境测试，准备wd.txt文件

```
spark hadoop hive
hive hadoop
hbase
hive spark
flume hadoop
spark hive
```

   代码：

```Python
from pyspark import SparkConf, SparkContext

# os.environ["PYSPARK_PYTHON"]="/home/python3/bin/python"
# os.environ["PYSPARK_DRIVER_PYTHON"]="/home/python3/bin/python"

if __name__ == '__main__':
   # conf = SparkConf().setMaster("spark://Pspark:7077").setAppName("wordTest")
    #local[*]为本地模式，aka在windows上运行
    conf = SparkConf().setMaster("local[*]").setAppName("rdd-1")
    sc = SparkContext(conf=conf)

    counts = sc.textFile("hdfs://Pspark:9000/wd.txt")\
        .flatMap(lambda line:line.split(" "))\
        .map(lambda x:(x, 1))\
        .reduceByKey(lambda a,b:a+b).collect()
    print(counts)

    # 习惯
    sc.stop()
```

​	注：此处已经修改了日志等级，未修改情况下，会有较多打印结果。如打印【hadoop winutils.exe】问题，则为win本地缺少hadoop依赖，等级为error，实则不影响，可忽略。

<img src=".\image\image-20220901094603665.png" alt="image-20220901094603665" style="zoom:50%;" />



# 2. 【2/3选一个完成就行】提交服务器

​	代码：

```python
from pyspark import SparkConf, SparkContext

if __name__ == '__main__':
    #其中Pspark为服务端地址ip映射，已经添加到Windows中hosts文件，未添加可使用ip地址替代
    conf = SparkConf().setMaster("spark://Pspark:7077").setAppName("wordTest")
    #conf = SparkConf().setMaster("local[*]").setAppName("rdd-1")
    sc = SparkContext(conf=conf)

    counts = sc.textFile("hdfs://Pspark:9000/wd.txt")\
        .flatMap(lambda line:line.split(" "))\
        .map(lambda x:(x, 1))\
        .reduceByKey(lambda a,b:a+b).collect()
    print(counts)

    # 习惯
    sc.stop()
```

<img src=".\image\image-20220901095026552.png" alt="image-20220901095026552" style="zoom:50%;" />







## 常遇到报错：

### 1.8.1 乱码

​	控制台输出乱码或者符号，究其原理为jdk问题

```
第一步：检查jdk版本，最佳为1.8，不建议版本过高
第二步：检查JAVA_HOME 正确的地址为：【G:\Jdk8】，不需要指定到bin目录，路径中不能有空格
排查完成后，问题基本可以解决
第三步：再出现乱码，或者电脑多版本jdk，则需要使用os.environ的方法，在程序中指定JAVA_HOME
例：
import os
os.environ["JAVA_HOME"]="G:\Jdk8"
```



### 1.8.2 Python报错

​	一般是由于电脑内Python版本过多，环境变量过于复杂导致。

```
方法一：在环境变量删除不必要的Python

方法二：使用os.environ的方法，在程序中指定PYSPARK_PYTHON
import os
os.environ["PYSPARK_PYTHON"]="G:\Anaconda3\envs\Pspark3.6\python.exe"
方法二弊端：强制写入的话，如果提交服务器运行，则需要修改PYSPARK_PYTHON地址，指向为虚拟机的Python地址，麻烦。
```



### 1.8.3 资源请求报错

​	提交服务端运行Spark时，程序卡在请求资源直达超时。原因为：提交服务本质为双向通讯，虚拟机【Pspark】与Windows的双向通讯，所以需要添加双向的映射服务。如果是手机热点提供的WiFi或者不稳定连接【校园网也有可能玄学出发】，包括360都会有可能导致报错。

```shell
vim /etc/hosts
#虚拟机映射，主要修改为最后一行，其余已在前面步骤完成
#192.168.80.1 为NAT网络连接模式的网关。如果是桥接模式，则可以添加实际的windows ip地址
#MSI 为Windows机器名称，可在设置里面查看，或者进入Spark页面，查看进程阻塞位置，也会看到。
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

192.168.80.150  Pspark
192.168.80.1    MSI


#Windows映射
#地址：C:\Windows\System32\drivers\etc，修改hosts文件，有权限无法修改的话，拖到桌面，修改完再拖回。
#写入内容
192.168.80.150  Pspark

```



# 3. 提交服务器（PyCharm专业版才有远程开发）

## 3.1 构建虚拟环境

查看当前环境的虚拟环境情况

```sh
conda env list
```

![image-20230523094453244](.\2-Spark-Python.assets\image-20230523094453244.png)

​	构建与Windows开发环境相同Python版本的虚拟环境，预计一两分钟左右。

```sh
conda create -n pyspark_3.6 python==3.6

# 构建完成后，再次执行，会显示已有的虚拟环境
conda env list
```

<img src=".\2-PySpark调用.assets\image-20230523094810690.png" alt="image-20230523094810690" style="zoom:80%;" />

​	进入虚拟环境

```sh
# 首次使用 source activate 命令激活虚拟环境
source activate pyspark_3.6

# 退出虚拟环境
conda deactivate

# 后续使用 conda activate 命令激活虚拟环境
conda activate pyspark_3.6
```

![image-20230523100036555](.\2-Spark-Python.assets\image-20230523100036555.png)

​	在虚拟环境中，安装指定版本的pyspark包，与之前安装的Spark版本相同

```python
# 指定国内源，目测会快一些，但是不多
# 目测阿里源快一些
pip install pyspark==2.4.1 -i https://pypi.tuna.tsinghua.edu.cn/simple

#安装完成后，查看库
pip list
```

![image-20230523101936852](.\2-Spark-Python.assets\image-20230523101936852.png)

​	测试pyspark，首先启动HDFS以及Spark服务

```sh
# 查看进程
jps

# 进入到Spark安装目录
bin/pyspark

# 测试功能是否正常
sc.parallelize([1,2,3,4]).collect()
```

![image-20230523104257578](.\2-Spark-Python.assets\image-20230523104257578.png)



## 3.2 PyCharm远程连接

添加远程环境解释器

![image-20230523104749614](.\2-Spark-Python.assets\image-20230523104749614.png)

​	添加“Host”：虚拟机别名/IP【无所谓的，能识别到就行】，“Username”：虚拟机的用户名

<img src=".\2-PySpark调用.assets\image-20230523110453445.png" alt="image-20230523110453445" style="zoom:50%;" />

​	”Password“：虚拟机的密码

<img src=".\2-PySpark调用.assets\image-20230523110652787.png" alt="image-20230523110652787" style="zoom:50%;" />

​		目测没毛病，下一步

<img src=".\2-PySpark调用.assets\image-20230523111003492.png" alt="image-20230523111003492" style="zoom:50%;" />

​	选择虚拟环境

![image-20230523111928168](.\2-Spark-Python.assets\image-20230523111928168.png)

​	设置工程映射，新建虚拟机路径，用于存放过程

<img src=".\2-PySpark调用.assets\image-20230523112535189.png" alt="image-20230523112535189" style="zoom:80%;" />

​	目测没问题，但是运行报错【JAVA_HOME is not set】，需要进行【~/.bashrc】设置，添加【JAVA_HOME】，以及对应的【PYSPARK_PYTHON】。或者在程序中，通过os.environ方式指定。**二选一就行**

<img src=".\2-PySpark调用.assets\image-20230523113441070.png" alt="image-20230523113441070" style="zoom:50%;" />

​	**方法一：**

```sh
vim ~/.bashrc

# 添加
export JAVA_HOME="/home/app/jdk1.8"
export PYSPARK_PYTHON="/home/anaconda3/envs/pyspark_3.6/bin/python"

# 生效环境变量
source ~/.bashrc
```

<img src=".\2-PySpark调用.assets\image-20230523114609237.png" alt="image-20230523114609237" style="zoom:50%;" />

<img src=".\2-PySpark调用.assets\image-20230523115054855.png" alt="image-20230523115054855" style="zoom:67%;" />



​	**方法二：**

​	输出相同,但偶尔会报点红,不影响。强迫症建议选择第一种。

![image-20230523114348856](.\2-Spark-Python.assets\image-20230523114348856.png)