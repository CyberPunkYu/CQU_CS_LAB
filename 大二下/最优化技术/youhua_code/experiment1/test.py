import matplotlib.pyplot as plt
import numpy as np
import math

def  calFunc(x):  #函数
  return 8*(math.exp(1-x))+7*math.log(x,10)

print(calFunc(1))
# print(calFunc(2))
# print(calFunc(5))
# print(calFunc(6))