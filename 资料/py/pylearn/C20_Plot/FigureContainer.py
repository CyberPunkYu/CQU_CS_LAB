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
plt.show()