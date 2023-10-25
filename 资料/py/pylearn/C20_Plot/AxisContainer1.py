from matplotlib import pyplot as plt
import numpy as np

x = np.linspace(0,4*np.pi,500)
fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(111)
ax.plot(x,np.sin(x),label="sin(x)")
ax.plot(x,np.cos(x),label="cos(y)")
ax.legend()
plt.show()