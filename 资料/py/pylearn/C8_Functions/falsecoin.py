#falsecoin.py
from math import floor
def findFalseCoin(coins,start,n):  
    "在coins列表中下标start开始的n个硬币中查找假硬币"
    if n==1:
        return start      #查找范围里只剩下一枚硬币，直接返回其下标
    nHalf = floor(n/2.0)  #nHalf为硬币数量的一半，下取整
    wL = sum(coins[start:start+nHalf])   #左:start下标开始的nHalf枚硬币的总重量
    wR = sum(coins[start+nHalf:start+nHalf+nHalf]) #右:另外nHalf枚硬币的总重量
    if wL < wR:       #左轻，假硬币在start下标开始的nHalf枚硬币里
        return findFalseCoin(coins,start,nHalf)
    elif wR < wL: 	  #右轻，假硬币在start+nHalf下标开始的nHalf枚硬币里
        return findFalseCoin(coins,start+nHalf,nHalf)
    elif nHalf*2 < n: #左右相等，且剩余一枚硬币未上天平，剩余那枚硬币为假
        return start + n - 1
    else:             #左右相等，且没有剩余硬币，未找到假硬币
        return None


coins = [100,100,100,99,100,100,100,100,100]
r = findFalseCoin(coins,0,len(coins))
print(('假硬币:%d' % r) if r!=None else '没有发现假硬币')
