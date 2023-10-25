# -*- coding: utf-8 -*-

from turtle import *
import random
import turtle
length = 10
angle  = 90
setup(1280,720)
up()

goto(-640,-360)
down()
def draw_path(path):
    for symbol in path:
        if symbol == 'f':
            colormode(255)
            color(random.randint(0,255),random.randint(0,255),random.randint(0,255))
            fd(length)
        elif symbol == '+':
            lt(angle)
        elif symbol == '-':
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
    'x':'+yf-xfx-fy+',
    'y':'-xf+yfy+fx-'
}
path = 'x'
speed(0)
for i in range(7):
    path = apply_path(rules,path)
draw_path(path)
ts = turtle.getscreen()
ts.getcanvas().postscript(file="work4.eps") #.eps文件即postscript脚本

done()