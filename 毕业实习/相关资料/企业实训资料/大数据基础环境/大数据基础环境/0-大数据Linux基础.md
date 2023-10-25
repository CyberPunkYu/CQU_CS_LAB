# 虚拟机环境搭建

## 1. 安装Vmware及Centos7

软件安装版本

<img src=".\image\image-20220621084053997.png" alt="image-20220621084053997" style="zoom:50%;" />

镜像地址：https://mirrors.tuna.tsinghua.edu.cn/centos/7/isos/x86_64/

### 1.1 创建虚拟机

<img src=".\image\image-20220621084140018.png" alt="image-20220621084140018" style="zoom:40%;" />



<img src=".\image\image-20220621084213060.png" alt="image-20220621084213060" style="zoom:40%;" />

### 1.2 挂载系统



<img src=".\image\image-20220621084301042.png" alt="image-20220621084301042" style="zoom:40%;" />

<img src=".\image\image-20220621084337292.png" alt="image-20220621084337292" style="zoom:40%;" />

### 1.3 指定存储路径

<img src=".\image\image-20220621084508141.png" alt="image-20220621084508141" style="zoom: 40%;" /><img src=".\image\image-20220621084526134.png" alt="image-2022062108452613" style="zoom:40%;" />



### 1.4 配置虚拟机

#### 1.4.1 根据电脑性能选择合适的内存

<img src=".\image\image-20220621085150534.png" alt="image-20220621085150534" style="zoom:40%;" />

#### 1.4.2 挂载系统

<img src=".\image\image-20220621085326271.png" alt="image-20220621085326271" style="zoom:40%;" />

#### 1.4.3 设置网络模式

<img src=".\image\image-20220621085354876.png" alt="image-20220621085354876" style="zoom:40%;" />



### 1.5 开启虚拟机

<img src=".\image\image-20220621090507604.png" alt="image-20220621090507604" style="zoom:40%;" />

​	选择第一个进行安装

<img src=".\image\image-20220621090536067.png" alt="image-20220621090536067" style="zoom:40%;" />

​	选择系统语言，下一步

<img src=".\image\image-20220621090723204.png" alt="image-20220621090723204" style="zoom:40%;" />

​	点击DATE&TIME，在地图位置点击中国，选择时区为shanghai，点击左上角的Done按钮完成设置

<img src=".\image\image-20220621091541816.png" alt="image-20220621091541816" style="zoom:33%;" />



​	选择 INSTALLATION DESTINATION

<img src=".\image\image-20220621091942315.png" alt="image-20220621091942315" style="zoom:33%;" />

​	选择自动义分区，然后按左上角的蓝色Done按钮。

<img src="G:\Note\课程安排\大数据基础环境\0-大数据Linux基础.assets\image-20230531172239104.png" alt="image-20230531172239104" style="zoom:67%;" />



​	点击Accept Changes。返回上一页，点击右下角蓝色按钮Begin installation

<img src=".\image\image-20220621092737718.png" alt="image-20220621092737718" style="zoom:33%;" />



​	点击ROOT PASSWORD,输入两遍密码，确认后即可看到程序正在运行安装了

<img src=".\image\image-20220621091244943.png" title=" style=&quot;zoom:50%;" style="zoom:50%;" />

​	安装完成，重启

<img src=".\image\image-20220621092906555.png" alt="image-20220621092906555" style="zoom:33%;" />



### 1.6 配置静态IP

#### 1.6.1 虚拟网络设置

​	建议在关机状态下修改网络，点击编辑，选择倒数第二个选项“虚拟网络编辑器”，出现下面的“虚拟\网络编辑器”窗口。

​	选择NAT模式，注意子网IP前三位与NAT设置的网关IP、DHCP网段一致。

<img src=".\image\image-20220621095103352.png" alt="image-20220621095103352" style="zoom:40%;" />



<img src=".\image\image-20220621095543490.png" alt="image-20220621095543490" style="zoom:50%;" />



<img src=".\image\image-20220621095605144.png" alt="image-20220621095605144" style="zoom:50%;" />

<img src=".\image\image-20220621095621186.png" alt="image-20220621095621186" style="zoom:50%;" />



#### 1.6.2 配置静态IP

​	使用root用户，登录虚拟机

<img src=".\image\image-20220621095856489.png" alt="image-20220621095856489" style="zoom:50%;" />



​	使用命令，打开ifcfg-ens33文件，修改配置

```shell
vi /etc/sysconfig/network-scripts/ifcfg-ens33
```



<img src=".\image\image-20220621101308056.png" alt="image-20220621101308056" style="zoom:67%;"/>



​	按esc退出编辑模式后 :wq!  强制退出并保存

​	重启网卡

```shell
service network restart	

curl www.baidu.com   #抓取百度页面内容 
```

![image-20220621103554818](.\image\image-20220621103554818.png)



### 1.7 关闭防火墙

```shell
systemctl status firewalld.service #查看firewall状态
systemctl stop firewalld.service  #停⽌firewall
systemctl disable firewalld.service  #禁⽌firewall开机启动
```



### 1.8 连接Xshell

​	新建会话，输入主机的IP地址，配置用户身份验证

<img src=".\image\image-20220621105057950.png" alt="image-20220621105057950" style="zoom:40%;" />

<img src=".\image\image-20220621105631736.png" alt="image-20220621105631736" style="zoom:50%;" />

<img src=".\image\image-20220621105730846.png" alt="image-20220621105730846" style="zoom:67%;" />



### 1.9 修改hostname以及映射

```shell
vi /etc/hostname  #修改主机名
```

<img src=".\image\image-20220621110525781.png" alt="image-20220621110525781" style="zoom:50%;" />



```shell
vi /etc/hosts #添加IP与主机的映射
```

<img src=".\image\image-20220621110638847.png" alt="image-20220621110638847" style="zoom:50%;" />

```shell
reboot  #重启，主机名修改生效
```

<img src=".\image\image-20220621110911576.png" alt="image-20220621110911576" style="zoom:60%;" />





# Linux常用命令

## 1. 常用快捷键

1）ctrl + c：停止进程
2）ctrl+l：清屏
3）善于用tab键
4）上下键：查找执行过的命令,或者是history命令



## 2. 文件目录类命令

### 2.1 pwd

pwd（功能描述：显示当前工作目录的绝对路径）

<img src=".\image\image-20220621123932609.png" alt="image-20220621123932609" style="zoom:67%;" />



### 2.2 ls 列出目录的内容

```shell
ls/ll [选项] [目录或是文件]
```

选项：
-a ：all,全部的文件，连同隐藏的文档( 开头为 . 的文件) 一起列出来(常用)
-l ： 长数据串列列出，包含文件的属性与权限等等数据；(常用)



### 2.3 mkdir 创建一个新的目录
```shell
mkdir [-p] 要创建的目录
```
选项：
-p：创建多层目录



### 2.4 rmdir 删除一个空的目录
```shell
rmdir 要删除的空目录，remove 即移除
```

### 2.5 touch 创建空文件
```shell
touch ⽂件名称
```

### 2.6 cd 切换目录
```shell
cd 绝对路径
cd 相对路径
cd ~或者cd （功能描述：回到自己的家目录）
cd - （功能描述：回到上一次所在目录）
cd .. （功能描述：回到当前目录的上一级目录）
cd . （功能描述：回到当前目录）
```

### 2.7 cp 复制文件或目录
```shell
cp source dest （功能描述：复制source文件到dest）
cp -r sourceFolder targetFolder （功能描述：递归复制整个文件夹）
#注意：r即recursive递归，这⾥是递归拷⻉，将该⽬录以及所有子目录（包括再多的⼦⽬录）下的所有⽂件即⽂件夹都拷⻉
```

### 2.8 rm 移除文件或目录
```shell
rmdir deleteEmptyFolder （功能描述：删除空目录），缺点：只能删除空目录
rm -rf deleteFile （功能描述：递归删除目录中所有内容）慎用
```

### 2.9 mv 移动文件与目录或重命名
```shell
mv oldNameFile newNameFile （功能描述：重命名）
mv /temp/movefile /targetFolder （功能描述：递归移动文件）
```
### 2.10 查看文件内容
```shell
cat [选项] 要查看的文件
more 要查看的文件
tail [-f] 文件 #f选项为时事追踪文档的更新
```



## 3. 用户管理命令

### 3.1 useradd 添加新用户

```shell
useradd 用户名 （功能描述：添加新用户）
```
### 3.2 passwd 设置用户密码
```shell
passwd 用户名 （功能描述：设置用户密码）
```

<img src=".\image\image-20220627143432425.png" alt="image-20220627143432425" style="zoom:70%;" />



### 3.3 判断用户是否存在

```shell
id 用户名
cat /etc/passwd   #查看系统中创建了哪些用户
```

<img src=".\image\image-20220627143623531.png" alt="image-20220627143623531" style="zoom:80%;" />



### 3.4 su切换用

```shell
su 用户名 #如果切换为root用户，可省略用户名
```

<img src=".\image\image-20220627144019334.png" alt="image-20220627144019334" style="zoom:80%;" />



## 4. 文件权限类

### 4.1 chmod改变权限

```shell
chmod [{ugoa}{+-=}{rwx}] [文件或目录] [mode=421 ] [文件或目录]

#文件: r-查看；w-修改；x-执⾏文件
#目录: r-列出目录内容；w-在目录中创建和删除；x-进入目录

chmod -R 777 /home/app/spark   #常用
```



### 4.2 chown改变所有者

```shell
chown [最终用户] [文件或目录] （功能描述：改变文件或者目录的所有者）

chown hadoop:hadoop /home/app/spark   #常用修改用户组
```



## 5. 搜索查找

### 5.1 find查找文件与目录

```shell
find [搜索范围] [匹配条件]
```

<img src=".\image\image-20220627144704339.png" alt="image-20220627144704339" style="zoom:80%;" />



### 5.2 grep 过滤查找及“|”管道符

```shell
grep+参数+查找内容+源⽂文件

#管道符，“|”，表示将前一个命令的处理结果输出传递给后面的命令处理
-c：只输出匹配⾏的计数。
-I：不区分⼤小写(只适⽤用于单字符)。
-h：查询多文件时不显示⽂件名。
-l：查询多文件时只输出包含匹配字符的文件名。
-n：显示匹配⾏及⾏号。
-s：不显示不存在或无匹配文本的错误信息。
-v：显示不包含匹配文本的所有⾏
```

<img src=".\image\image-20220627145122050.png" alt="image-20220627145122050" style="zoom:80%;" />



## 6. 进程线程

### 6.1 ps查看系统中所有进程

```shell
ps -aux  #查看系统中所有进程

USER：该进程是由哪个用户产生的
PID：进程的ID号
%CPU：该进程占用CPU资源的百分比，占用越高，进程越耗费资源；
%MEM：该进程占用物理内存的百分⽐，占⽤用越高，进程越耗费资源；
VSZ：该进程占用虚拟内存的⼤小，单位KB；
RSS：该进程占用实际物理内存的大小，单位KB；
TTY：该进程是在哪个终端中运⾏的。其中tty1-tty7代表本地控制台终端，tty1-tty6是本地的字符界面
终端，tty7是图形终端。pts/0-255代表虚拟终端。
STAT：进程状态。常见的状态有：R：运⾏行行、S：睡眠、T：停⽌止状态、s：包含子进程、+：位于后台
START：该进程的启动时间
TIME：该进程占用CPU的运算时间，注意不是系统时间
COMMAND：产⽣生此进程的命令名
```



### 6.2 top查看系统健康状态

```shell
top [选项]

-d 秒数：指定top命令每隔几秒更更新。默认是3秒。
-i：使top不显示任何闲置或者僵死进程。
-p：通过指定监控进程ID来仅监控某个进程的状态。

执⾏top命令之后，与top命令进⾏交互
P： 以CPU使用率排序，默认就是此项
M： 以内存的使用率排序
N： 以PID排序
q： 退出top
top -d 1
top -i
```



### 6.3 pstree查看进程树

```shell
yum install psmisc -y
pstree [选项]

pstree -u #显示进程的所属⽤用户
pstree -p #显示进程的PID
```



### 6.4 kill终止进程

```shell
kill -9 pid进程号
```

### 6.5 netstat显示网络统计信息

```shell
yum install net-tools -y

netstat -anp

netstat -anp | grep 22 #查看22端口的使用情况
```

<img src=".\image\image-20220627150259468.png" alt="image-20220627150259468" style="zoom:70%;" />





## 7. 压缩与解压缩

### 7.1 gzip/gunzip压缩

```shell
yum install gzip -y
gzip+文件  #压缩文件，只能将文件压缩为*.gz文件，执⾏后，原来文件消失，生成压缩文件
gunzip+文件.gz #解压缩文件命令，执⾏后，压缩文件消失，生成解压后的文件

# 注意点：只能压缩文件，不能压缩目录，不保留原来的文件
```

### 7.2 zip/unzip压缩

```shell
yum install unzip -y

zip + 参数 + XXX.zip + 将要压缩的内容  #压缩文件和目录的命令，window/linux通用且可以压缩目录且保留源文件
#参数 -r 压缩⽬目录
unzip +压缩包 +-d + 指定解压目的路径 

```



### 7.3 tar打包

```shell
tar -zxvf 压缩包  -C 目标路径
```



# VI/VIM编辑器



## 1. 一般模式

​	以 vi 打开⼀一个档案就直接进入一般模式了(这是默认的模式)。在这个模式中， 你可以使用『上下左右』按键来移动光标。

​	常用语法：

​	1）yy：功能描述：复制光标当前一行  
​	2）p （功能描述：箭头移动到目的行贴粘在光标所在行的下一行）
​	3）u （功能描述：撤销上一步）
​	4）dd （功能描述：删除光标当前行）
​	5）shift+^ （功能描述：移动到行头）
​	6）shift+$ （功能描述：移动到行尾）
​	7）1+shift+g （功能描述：移动到页头，数字，先按1，再同时按shift+g，注意不是同时按1+shift+g）
​	8）shift+g （功能描述：移动到页尾）
​	9）数字N+shift+g （功能描述：移动到目标行）



## 2. 编辑模式

​	在一般模式中可以进行删除、复制、贴上等等的动作，但是却无法编辑文件内容的！ 要等到你按下『i,I, o, O, a,A, r, R』等任何一个字母之后才会进入编辑模式。而如果要回到一般模式时， 则必须要按下『Esc』这个按键即可退出编辑模式

​	常用语法：
​	1）进⼊入编辑模式
​	（1）i 当前光标前（最常用）
​	（2）a 当前光标后
​	（3）o 当前光标行的下一行
​	2）退出编辑模式，即进入一般模式
​		按『Esc』键

## 3. 指令模式

​	在一般模式当中，输入『 : / ?』3个中的任何一个按钮，就可以将光标移动到最底下那一行，在这个模式当中， 可以提供你『搜寻资料料』的动作，而读取、存盘、大量取代字符、离开 vi 、显示行号等动作是在此模式中达成的。

​	常用语法：

​	1）:w！ 保存退出

​	2）:q!	强制退出不保存

​	3）:wq! 强制退出并保存

​	4）esc退出编辑模式后，按shift+z+z     推出并保存快捷键