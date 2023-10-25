import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
 
#np.random.seed(2000)
y = np.random.standard_normal((10, 2))
print(y)
plt.figure(figsize=(7,5))
# plt.plot(y, lw = 1.5)
plt.plot(y, 'ro')
plt.grid(True)
plt.axis('tight')
plt.xlabel('index')
plt.ylabel('value')
plt.title('A simple plot')
plt.show()
