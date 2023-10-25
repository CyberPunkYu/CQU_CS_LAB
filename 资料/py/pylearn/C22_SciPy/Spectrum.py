#Spectrum.py
import numpy as np
from matplotlib import pyplot as plt

iSampleRate = 2000					#采样频率,每秒2000个样本
x = np.fromfile("ecgsignal.dat",dtype=np.float32)
iSampleCount = x.shape[0]			#采样数
t = np.linspace(0,iSampleCount/iSampleRate,iSampleCount)

xFFT = np.abs(np.fft.rfft(x)/iSampleCount)  #快速傅里叶变换
xFreqs = np.linspace(0, iSampleRate/2, int(iSampleCount/2)+1)

plt.figure(figsize=(10,6))
ax0 = plt.subplot(211)             #画时域信号
ax0.set_xlabel("Time(s)")
ax0.set_ylabel("Amp(μV)")
ax0.plot(t,x)

ax1 = plt.subplot(212)             #画频域信号-频谱
ax1.set_xlabel("Freq(Hz)")
ax1.set_ylabel("Power")
ax1.plot(xFreqs, xFFT)
plt.show()