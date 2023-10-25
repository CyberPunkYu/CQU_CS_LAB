# -*- coding: utf-8 -*-
"""
utils
"""
import math
def CalDistance(x,y):
    return math.sqrt(x**2+y**2)

def CalLength(citys, paths,start,end):
    length=0
    n=1
    for i in range(len(paths)):
        if i==0:
            length+=CalDistance(start[0]-citys['x'][paths[i]],start[1]-citys['y'][paths[i]])
            n+=1
        elif n<len(paths):
            length+=CalDistance(citys['x'][paths[i]]-citys['x'][paths[i+1]],citys['y'][paths[i]]-citys['y'][paths[i+1]])
            n+=1
        else:
            length+=CalDistance(citys['x'][paths[i]]-end[0],citys['y'][paths[i]]-end[1])
    return length