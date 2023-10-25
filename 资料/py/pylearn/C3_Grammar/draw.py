import turtle
t = turtle.Pen()                #创建一支画笔
iCirclesCount = 30          
for x in range(iCirclesCount):  #循环30次      
    t.circle(100)               #画一个直径为100的圆
    t.left(360/iCirclesCount)   #向左转 360 / 30 = 12度