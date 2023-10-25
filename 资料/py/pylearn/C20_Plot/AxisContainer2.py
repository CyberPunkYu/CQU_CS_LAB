from matplotlib import pyplot as plt
import numpy as np

x = np.linspace(0,4*np.pi,500)
fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(111)
ax.plot(x,np.sin(x),label="sin(x)")
ax.plot(x,np.cos(x),label="cos(y)")
ax.legend()

xa = ax.xaxis
for x in xa.get_ticklabels():
    x.set_color("g")
    x.set_rotation(45)
    x.set_fontsize(16)

for x in xa.get_ticklines():
    x.set_color("r")
    x.set_markersize(10)
    x.set_markeredgewidth(3)

print("len(xa.get_ticklines(minor=True):",len(xa.get_ticklines(minor=True)))
plt.show()