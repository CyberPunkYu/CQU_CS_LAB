# 强化训练

## 面试题

```
year  month amount
1991,1,1.1
1991,2,1.2
1991,3,1.3
1991,4,1.4
1992,1,2.1
1992,2,2.2
1992,3,2.3
1992,4,2.4

讲表格转化为下面结果
year m1  m2  m3   m4
1991 1.1 1.2 1.3 1.4
1992 2.1 2.2 2.3 2.4


SELECT
  year,
  MAX(CASE WHEN month = 1 THEN amount END) AS m1,
  MAX(CASE WHEN month = 2 THEN amount END) AS m2,
  MAX(CASE WHEN month = 3 THEN amount END) AS m3,
  MAX(CASE WHEN month = 4 THEN amount END) AS m4
FROM
  tes1
GROUP BY
  year;

```

```sql
CREATE TABLE tes1 (
year int,
month int,
amount FLOAT
)row format delimited fields terminated by ",";

load data local inpath '/home/data/year.txt' into table tes1;
```

## 源代码

```SQL
SELECT
  year,
  MAX(CASE WHEN month = 1 THEN amount END) AS m1,
  MAX(CASE WHEN month = 2 THEN amount END) AS m2,
  MAX(CASE WHEN month = 3 THEN amount END) AS m3,
  MAX(CASE WHEN month = 4 THEN amount END) AS m4
FROM
  tes1
GROUP BY
  year;
```

![](C:\Users\111\Desktop\企业实训资料\大数据基础环境\大数据基础环境\workImg\tes1.png)

## 日志处理

时间                                     接口                          ip地址

2016-11-09 11：22：05  /api/user/login         110.23.5.33

2016-11-09 11：23：10  /api/user/detail         57.3.2.16

.....

2016-11-09 23：59：40  /api/user/login         200.6.5.166

数据集：

```
2016-11-09 14:22:05	/api/user/login	110.23.5.33   1
2016-11-09 11:23:10	/api/user/detail	57.3.2.16
2016-11-09 14:59:40	/api/user/login	200.6.5.166   1
2016-11-09 14:22:05	/api/user/login	110.23.5.34   1
2016-11-09 14:22:05	/api/user/login	110.23.5.34	  1
2016-11-09 14:22:05	/api/user/login	110.23.5.34   1
2016-11-09 11:23:10	/api/user/detail	57.3.2.16
2016-11-09 23:59:40	/api/user/login	200.6.5.166
2016-11-09 14:22:05	/api/user/login	110.23.5.34   1
2016-11-09 11:23:10	/api/user/detail	57.3.2.16
2016-11-09 23:59:40	/api/user/login	200.6.5.166
2016-11-09 14:22:05	/api/user/login	110.23.5.35   1
2016-11-09 14:23:10	/api/user/detail	57.3.2.16
2016-11-09 23:59:40	/api/user/login	200.6.5.166   
2016-11-09 14:59:40	/api/user/login	200.6.5.166   1
2016-11-09 14:59:40	/api/user/login	200.6.5.166   1
```

```sql
create table ip(
time string,
interface string,
ip string)
row format delimited fields terminated by '\t';
load data local inpath '/home/data/ip.dat' into table ip;

select ip, count(ip) cip from ip
where interface = "/api/user/login" and time between '2016-11-09 14:00:00' and '2016-11-09 15:00:00'
group by ip
order by cip DESC
limit 3;
```

求11月9号下午14点（**14-15点**），访问**api/user/login**接口的，top3的ip地址以及次数

## 源代码

```
select ip, count(ip) cip from ip
where interface = "/api/user/login" and time between '2016-11-09 14:00:00' and '2016-11-09 15:00:00'
group by ip
order by cip DESC
limit 3;
```

## 结果

![](C:\Users\111\Desktop\企业实训资料\大数据基础环境\大数据基础环境\workImg\tes2-1.png)

![](C:\Users\111\Desktop\企业实训资料\大数据基础环境\大数据基础环境\workImg\tes2.2.png)

## 三连冠

找出全部夺得3连冠的队伍

```sql
team,year
活塞,1990
公牛,1991
公牛,1992
公牛,1993
火箭,1994
火箭,1995
公牛,1996
公牛,1997
公牛,1998
马刺,1999
湖人,2000
湖人,2001
湖人,2002
马刺,2003
活塞,2004
马刺,2005
热火,2006
马刺,2007
凯尔特人,2008
湖人,2009
湖人,2010
小牛,2011
热火,2012
热火,2013
马刺,2014
勇士,2015
骑士,2016
勇士,2017
勇士,2018
猛龙,2019
湖人,2020
雄鹿,2021
勇士,2022
掘金,2023

create table ball(
team string,
year int
)row format delimited fields terminated by ',';

load data local inpath "/home/data/qiapi.dat" into table ball;

查询代码：


```

提示：rank值的除了排名外，还有什么含义

```sql

```





## 源代码

```
SELECT team, count(*) AS TripleCount FROM(
SELECT team FROM(
SELECT team, year, ROW_NUMBER() 
OVER (PARTITION BY team ORDER BY year) AS row_num
FROM ball
) subquery
GROUP BY team, year - row_num
HAVING COUNT(*) >= 3
) subquery2
GROUP by team;
```

## 结果

![](C:\Users\111\Desktop\企业实训资料\大数据基础环境\大数据基础环境\workImg\tes3-1.png)

![](C:\Users\111\Desktop\企业实训资料\大数据基础环境\大数据基础环境\workImg\tes3-2.png)































