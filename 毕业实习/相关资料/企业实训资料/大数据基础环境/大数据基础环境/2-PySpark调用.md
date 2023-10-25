# 1. Anaconda安装

​	略

# 2. 虚拟环境构建

​	查看当前环境的虚拟环境情况

```sh
conda env list
```

![image-20230523094453244](C:\Users\111\Desktop\企业实训资料\大数据基础环境\大数据基础环境\2-PySpark调用.assets\image-20230523094453244.png)

​	构建与Windows开发环境相同Python版本的虚拟环境，预计一两分钟左右。

```sh
conda create -n pyspark_3.6 python==3.6

# 构建完成后，再次执行，会显示已有的虚拟环境
conda env list
```

<img src="C:\Users\111\Desktop\企业实训资料\大数据基础环境\大数据基础环境\2-PySpark调用.assets\image-20230523094810690.png" alt="image-20230523094810690" style="zoom:80%;" />

​	进入虚拟环境

```sh
# 首次使用 source activate 命令激活虚拟环境
source activate pyspark_3.6

# 退出虚拟环境
conda deactivate

# 后续使用 conda activate 命令激活虚拟环境
conda activate pyspark_3.6
```

![image-20230523100036555](C:\Users\111\Desktop\企业实训资料\大数据基础环境\大数据基础环境\2-PySpark调用.assets\image-20230523100036555.png)

​	在虚拟环境中，安装指定版本的pyspark包，与之前安装的Spark版本相同

```python
# 指定国内源，目测会快一些，但是不多
pip install pyspark==2.4.1 -i https://pypi.tuna.tsinghua.edu.cn/simple

#安装完成后，查看库
pip list
```

![image-20230523101936852](C:\Users\111\Desktop\企业实训资料\大数据基础环境\大数据基础环境\2-PySpark调用.assets\image-20230523101936852.png)

​	测试pyspark，首先启动HDFS以及Spark服务

```sh
# 查看进程
jps

# 进入到Spark安装目录
bin/pyspark

# 测试功能是否正常
sc.parallelize([1,2,3,4]).collect()
```

![image-20230523104257578](C:\Users\111\Desktop\企业实训资料\大数据基础环境\大数据基础环境\2-PySpark调用.assets\image-20230523104257578.png)



# 3. PyCharm远程连接

​	添加远程环境解释器

![image-20230523104749614](C:\Users\111\Desktop\企业实训资料\大数据基础环境\大数据基础环境\2-PySpark调用.assets\image-20230523104749614.png)

​	添加“Host”：虚拟机别名/IP【无所谓的，能识别到就行】，“Username”：虚拟机的用户名

<img src="C:\Users\111\Desktop\企业实训资料\大数据基础环境\大数据基础环境\2-PySpark调用.assets\image-20230523110453445.png" alt="image-20230523110453445" style="zoom:50%;" />

​	”Password“：虚拟机的密码

<img src="C:\Users\111\Desktop\企业实训资料\大数据基础环境\大数据基础环境\2-PySpark调用.assets\image-20230523110652787.png" alt="image-20230523110652787" style="zoom:50%;" />

​		目测没毛病，下一步

<img src="C:\Users\111\Desktop\企业实训资料\大数据基础环境\大数据基础环境\2-PySpark调用.assets\image-20230523111003492.png" alt="image-20230523111003492" style="zoom:50%;" />

​	选择虚拟环境

![image-20230523111928168](C:\Users\111\Desktop\企业实训资料\大数据基础环境\大数据基础环境\2-PySpark调用.assets\image-20230523111928168.png)

​	设置工程映射，新建虚拟机路径，用于存放过程

<img src="C:\Users\111\Desktop\企业实训资料\大数据基础环境\大数据基础环境\2-PySpark调用.assets\image-20230523112535189.png" alt="image-20230523112535189" style="zoom:80%;" />

​	目测没问题，但是运行报错【JAVA_HOME is not set】，需要进行【~/.bashrc】设置，添加【JAVA_HOME】，以及对应的【PYSPARK_PYTHON】。或者在程序中，通过os.environ方式指定。**二选一就行**

<img src="C:\Users\111\Desktop\企业实训资料\大数据基础环境\大数据基础环境\2-PySpark调用.assets\image-20230523113441070.png" alt="image-20230523113441070" style="zoom:50%;" />

​	**方法一：**

```sh
vim ~/.bashrc

# 添加
export JAVA_HOME="/home/app/jdk1.8"
export PYSPARK_PYTHON="/home/anaconda3/envs/pyspark_3.6/bin/python"

# 生效环境变量
source ~/.bashrc
```

<img src="C:\Users\111\Desktop\企业实训资料\大数据基础环境\大数据基础环境\2-PySpark调用.assets\image-20230523114609237.png" alt="image-20230523114609237" style="zoom:50%;" />

<img src="C:\Users\111\Desktop\企业实训资料\大数据基础环境\大数据基础环境\2-PySpark调用.assets\image-20230523115054855.png" alt="image-20230523115054855" style="zoom:67%;" />



​	**方法二：**

​	输出相同,但偶尔会报点红,不影响。强迫症建议选择第一种。

![image-20230523114348856](C:\Users\111\Desktop\企业实训资料\大数据基础环境\大数据基础环境\2-PySpark调用.assets\image-20230523114348856.png)