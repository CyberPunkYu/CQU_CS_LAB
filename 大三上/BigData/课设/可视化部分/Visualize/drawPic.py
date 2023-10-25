from pyspark import SparkConf, SparkContext
from visualize import visualize
import re

DANMUPATH = '' # B站弹幕数据
COMMENTPATH = '' # B站评论数据
ZHIHUPATH = '' # 知乎评论数据

# SparkContext的初始化需要一个SparkConf对象，SparkConf包含了Spark集群配置的各种参数。
conf = SparkConf().setAppName("ex2").setMaster("spark://master:7077")
conf = SparkConf().setAppName("ex2").setMaster("local")
# 任何Spark程序都是SparkContext开始的,初始化后，就可以使用SparkContext对象所包含的各种方法来创建和操作RDD和共享变量。
sc = SparkContext(conf=conf)


# 处理并转化数据
def getData(path1, path2, path3):
    f1 = open(path1, 'r', encoding='utf-8')
    f2 = open(path2, 'r', encoding='utf-8')
    f3 = open(path3, 'r', encoding='utf-8')

    # 读取数据处理文件中的每一行内容
    info1 = [line.strip() for line in f1.readlines()]
    info2 = [line.strip() for line in f2.readlines()]
    info3 = [line.strip() for line in f3.readlines()]
    info = info1 + info2 + info3

    # 筛选并提取其中的数字部分
    data = []
    for i in info:
        if len(i): # 去除空行
            tmp1 = re.findall("[-+]?\d*\.\d+|\d+", i) # 正则表达式提取数字
            data.append(tmp1[0])

    # 切片原理将所有数据分到相应类别中
    avg = [float(i) for i in data[0::5]] # 平均数
    avg = [float('{:.4f}'.format(i)) for i in avg]
    tal = [float(i) for i in data[1::5]] # 总数
    tal = [float('{:.2f}'.format(i)) for i in tal]
    pos = [int(i) for i in data[2::5]] # 积极
    neg = [int(i) for i in data[3::5]] # 消极
    ten = [float(i) for i in data[4::5]] # 趋向
    ten = [float('{:.4f}'.format(i)) for i in ten]

    return avg, tal, pos, neg, ten

# 可视化展示
def draw():
    # 横坐标，20-1代表2020年第一季度
    key = ['20-1', '20-2', '20-3', '20-4', 
           '21-1', '21-2', '21-3', '21-4', 
           '22-1', '22-2', '22-3', '22-4']
    key_full = ['2020/1/1', '2020/4/1', '2020/7/1', '2020/10/1', 
                '2021/1/1', '2021/4/1', '2021/7/1', '2021/10/1', 
                '2022/1/1', '2022/4/1', '2022/7/1', '2022/10/1']
    # 河流图纵坐标
    cat = ['Positive', 'Negative']
    # 1为b弹幕数据，2为b评论数据，3为z评论数据
    avg1, tal1, pos1, neg1, ten1 = getData(DANMUPATH + "2020_danmu.txt", DANMUPATH + "2021_danmu.txt", DANMUPATH + "2022_danmu.txt")
    print("load bilibili_danmu_data successfully")
    avg2, tal2, pos2, neg2, ten2 = getData(COMMENTPATH + "2020.txt", COMMENTPATH + "2021.txt", COMMENTPATH + "2022.txt")
    print("load bilibili_comment_data successfully")
    avg3, tal3, pos3, neg3, ten3 = getData(ZHIHUPATH + "2020_zhihu.txt", ZHIHUPATH + "2021_zhihu.txt", ZHIHUPATH + "2022_zhihu.txt")
    print("load zhihu_comment_data successfully")

    river_data1 = []
    river_data2 = []
    for i in range(len(pos1)):
        river_data1.append([key_full[i], pos2[i], cat[0]])
        river_data2.append([key_full[i], pos3[i], cat[0]])
        river_data1.append([key_full[i], neg2[i], cat[1]])
        river_data2.append([key_full[i], neg3[i], cat[1]])
 
    v = visualize()
    v.drawLine(key, avg1, avg2, avg3) # B站弹幕和评论以及知乎评论
    v.drawRiver(cat, river_data1, "B站") # B站评论
    v.drawRiver(cat, river_data2, "知乎") # 知乎评论
    v.drawPie(key, ten2, "B站") # B站评论
    v.drawPie(key, ten3, "知乎") # 知乎评论

if __name__ == '__main__':
    draw()