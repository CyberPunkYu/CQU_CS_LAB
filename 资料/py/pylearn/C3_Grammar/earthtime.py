#earthtime.py
import time                       #导入time模块

curTime = time.time()             #获取当前时间,从1970年1月1日0零时起经过的秒数,类型为float
totalSeconds = int(curTime)       #总秒数 = 当前时间转换成整数，忽略毫秒微秒部分  
curSecond = totalSeconds % 60     #当前秒数 = 总秒数对60取余
totalMinutes = totalSeconds // 60 #总分钟 = 总秒数整除60
curMinute = totalMinutes % 60     #当前分钟 = 总分钟对60取余
totalHours = totalMinutes // 60   #总小时 = 总分钟整除60
curHour = totalHours % 24         #当前小时 = 总小时对24取余

print("现在是林格尼治时间",curHour,"时",curMinute,"分",\
curSecond,"秒,","1970年1月1日零时到现在经过了",totalSeconds,"秒.")