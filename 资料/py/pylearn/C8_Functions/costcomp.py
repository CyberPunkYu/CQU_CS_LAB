# 电费计算: (期末读数-期初读数)*单价
def costCompute(iStart,iEnd):    #形式参数，形参
    iConsume = iEnd - iStart
    return iConsume*0.85

fElecFee1 = costCompute(1201,1786)  #实际参数， 实参
fElecFee2 = costCompute(1322,1423)
print("Electric Power Cost of Mr Zhang:",fElecFee1)
print("Electric Power Cost of Mr Lee:",fElecFee2)
