"""
Draw mandelbrot set with matplotlib.
Escape time computed by Cython.
chenbo@cqu.edu.cn,   Dec 2018.

Usage:
    left-click mouse: Zoom in
    right-click mouse: Zoom out
    key escape:  Reset
    key up,key down: Switch color map.
"""

from matplotlib import pyplot as plt
from matplotlib import cm
import numpy as np
from MandelbrotComp import getEscapeTime

def computeMandelbrot(xCenter,yCenter,semiWidth,N):
    xFrom,xTo,yFrom,yTo = xCenter-semiWidth,xCenter+semiWidth,\
                          yCenter-semiWidth,yCenter+semiWidth
    y,x = np.ogrid[yFrom:yTo:N*1j,xFrom:xTo:N*1j]
    c = x + y*1j
    print("c.shape:",c.shape,"x.shape:",x.shape,"y.shape:",y.shape)
    return np.frompyfunc(getEscapeTime,1,1)(c).astype(np.float)

def drawMandelbrot(ax,xCenter,yCenter,semiWidth,N,cmap):
    "(xCenter,yCenter)-中心点，semiWidth-矩形半宽，N*N像素."
    ax.set_axis_off()
    ds = computeMandelbrot(xCenter,yCenter,semiWidth,N)
    ax.imshow(ds,cmap=cmap)

def refresh():
    print("x,y =",para.x,para.y,"semiWidth =", para.semiWidth)
    c = cm.get_cmap(para.cmaps[para.idxColorMap%len(para.cmaps)])
    drawMandelbrot(para.ax, para.x, para.y,
                   para.semiWidth, N=700,cmap=c)
    para.fig.canvas.draw()

def on_key_release(event):
    if event.key == 'up':
        para.idxColorMap+=1
    elif event.key == 'down':
        para.idxColorMap-=1
    elif event.key == 'escape':
        para.x, para.y = -0.5, 0.0
        para.semiWidth = 1.5
    else:
        return
    refresh()

def on_button_release(event):
    para.x = (para.x - para.semiWidth) + \
             2*para.semiWidth*event.xdata/para.figWidth
    para.y = (para.y - para.semiWidth) + \
             2*para.semiWidth*event.ydata/para.figHeight
    if event.button == 1:
        para.semiWidth /= 3.0
    elif event.button == 3:
        para.semiWidth *= 3.0
    refresh()

class Para:
    pass

para = Para()
para.x, para.y = -0.5, 0.0
para.semiWidth = 1.5
para.idxColorMap = 0
para.cmaps = ['rainbow', 'jet', 'nipy_spectral', 'gist_ncar','flag',
              'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
              'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
              'gist_rainbow']
para.fig = plt.figure(figsize=(7,7),dpi=100)
para.figWidth,para.figHeight = 700,700
para.fig.canvas.mpl_connect('key_release_event',on_key_release)
para.fig.canvas.mpl_connect('button_release_event',on_button_release)
plt.subplots_adjust(0,0,1,1,0.0,0)
para.ax = plt.subplot(111)
refresh()
plt.show()
