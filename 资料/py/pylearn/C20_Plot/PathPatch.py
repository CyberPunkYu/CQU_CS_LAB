import matplotlib.pyplot as plt
import numpy as np
from matplotlib import path,lines,patches

def addLabel(x,y, text):
    ax.text(x, y-0.15, text, ha="center", family='sans-serif', size=14)

fig, ax = plt.subplots()

c = patches.Circle([0.2,0.2], 0.1, edgecolor="r",facecolor="g")
addLabel(0.2,0.2, "Circle")

r = patches.Rectangle([0.2-0.04,0.5-0.06], 0.05, 0.1, fc="orange")
addLabel(0.2,0.5, "Rectangle")

path_data = [ (path.Path.MOVETO, [0.018, -0.11]),
              (path.Path.CURVE4, [-0.031, -0.051]),
              (path.Path.CURVE4, [-0.115, 0.073]),
              (path.Path.CURVE4, [-0.03, 0.073]),
              (path.Path.LINETO, [-0.011, 0.039]),
              (path.Path.CURVE4, [0.043, 0.121]),
              (path.Path.CURVE4, [0.075, -0.005]),
              (path.Path.CURVE4, [0.035, -0.027]),
              (path.Path.CLOSEPOLY, [0.018, -0.11])]
codes, verts = zip(*path_data)
h = path.Path(verts + np.array([0.2,0.8]), codes)
h = patches.PathPatch(h,facecolor='r')
addLabel(0.2,0.8, "PathPatch"),

p = patches.RegularPolygon([0.5,0.2], 5, 0.1,fc="purple")
addLabel(0.5,0.2, "Polygon")

e = patches.Ellipse([0.5,0.5], 0.2, 0.1,fc='brown')
addLabel(0.5,0.5, "Ellipse")

a = patches.Arrow(0.5 - 0.05, 0.8 + 0.05, 0.1,-0.1,
                       width=0.1,fc=(0.0,0.9,0.9))
addLabel(0.5,0.8, "Arrow")

w = patches.Wedge([0.8,0.2], 0.1, 30, 270, fc="cyan")
addLabel(0.8,0.2, "Wedge")

fb = patches.FancyBboxPatch([0.8-0.025, 0.5-0.05], 0.05, 0.1,
    boxstyle=patches.BoxStyle("Round", pad=0.02),fc='blue')
addLabel(0.8,0.5, "FancyBboxPatch")

for x in (c,r,h,p,e,a,fb,w):
    ax.add_patch(x)

x, y = np.array([[-0.06, 0.0, 0.1], [0.05, -0.05, 0.05]])
line = lines.Line2D(x + 0.8, y + 0.8, lw=5., alpha=0.9,color='black')
ax.add_line(line)   #2D线
addLabel(0.8,0.8, "Line2D")

plt.axis('off')
plt.tight_layout()
plt.show()