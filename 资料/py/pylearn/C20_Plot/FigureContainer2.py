from matplotlib import pyplot as plt
import matplotlib
import numpy as np

x = np.linspace(0,10,400)
fig = plt.figure()
plt.plot(x,np.sin(x),label="sin(x)")
plt.plot(x,np.cos(x),label="cos(x)")
plt.xlabel("Time")
plt.ylabel("Amp")
plt.title("sin & cos")
plt.legend()

for x in fig.axes:
    x.grid(True)

line1 = matplotlib.lines.Line2D([0,1],[0,1],
                                transform=fig.transFigure,figure=fig,color='r')
fig.lines.append(line1)

fig.patch.set_color('gray')
fig.patch.set_alpha(0.2)

print(type(fig.images))
print(type(fig.legends))

plt.show()


