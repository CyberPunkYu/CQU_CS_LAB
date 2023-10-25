# -*- coding: utf-8 -*-

from turtle import *
import turtle
length = 5
angle  = 90
setup(1280,720)
up()
goto(300,-100)

down()
def draw_path(path):
    for symbol in path:
        if symbol == 'f':
            import random
            colormode(255)
            color(random.randint(0,255),random.randint(0,255),random.randint(0,255))
            fd(length)
        elif symbol == '-':
            lt(angle)
        elif symbol == '+':
            rt(angle)

def apply_path(rules,path):
    lit = [x for x in path]
    for i in range(len(lit)):
        symbol = lit[i]
        if symbol == 'x':
            lit[i] = rules[symbol]
        elif symbol == 'y':
            lit[i] = rules[symbol]
    path = ''.join(lit)
    return path

rules = {
    'x':'x+yf+',
    'y':'-fx-y'
}
path = 'fx'
speed(10000)
for i in range(13):
    path = apply_path(rules,path)
draw_path(path)
ts = turtle.getscreen()
ts.getcanvas().postscript(file="work2.eps") #.eps文件即postscript脚本
done()