import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(12,4))
ax1,ax2,ax3 = fig.subplots(1,3)

d = np.linspace(0,10000,100)
ax1.semilogy(d, np.power(d,3))  #x轴常规坐标，y轴取对数坐标
ax1.set(title=r'semilogy: $y=x^3$')

d = np.arange(0.01, 10.0, 0.01)
ax2.semilogx(d, np.sin(2 * np.pi * d))  #y轴常规坐标，x轴取对数坐标
ax2.set(title=r'semilogx: $y=sin(2{\pi}x)$')

d = np.linspace(0,10000,100)
ax3.loglog(d, np.power(d,3), basex=2, basey=2) #x,y轴均取以2为底的对数坐标
ax3.set(title=r'loglog base 2: $y=x^3$')

fig.tight_layout()
for ax in (ax1,ax2,ax3):
    ax.grid()
plt.show()