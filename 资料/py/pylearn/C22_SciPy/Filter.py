import numpy as np
from matplotlib import pyplot as plt
from scipy import signal


def butterBandPassFilter(lowcut, highcut, samplerate, order):
    "生成巴特沃斯带通滤波器"
    semiSampleRate = samplerate*0.5
    low = lowcut / semiSampleRate
    high = highcut / semiSampleRate
    b,a = signal.butter(order,[low,high],btype='bandpass')
    return b,a

def butterBandStopFilter(lowcut, highcut, samplerate, order):
    "生成巴特沃斯带阻滤波器"
    semiSampleRate = samplerate*0.5
    low = lowcut / semiSampleRate
    high = highcut / semiSampleRate
    b,a = signal.butter(order,[low,high],btype='bandstop')
    return b,a

iSampleRate = 2000					#采样频率,每秒2000个样本
x = np.fromfile("ecgsignal.dat",dtype=np.float32)

#进行带通滤波
b,a = butterBandPassFilter(3,70,iSampleRate,order=4)
x = signal.lfilter(b,a,x)

#进行带阻滤波
b,a = butterBandStopFilter(48,52,iSampleRate,order=2)
x = signal.lfilter(b,a,x)


iSampleCount = x.shape[0]			#采样数
t = np.linspace(0,iSampleCount/iSampleRate,iSampleCount)

xFFT = np.abs(np.fft.rfft(x)/iSampleCount)  #快速傅里叶变换
xFreqs = np.linspace(0, iSampleRate/2, int(iSampleCount/2)+1)

plt.figure(figsize=(10,6))
ax0 = plt.subplot(211)             #画时域信号
ax0.set_xlabel("Time(s)")
ax0.set_ylabel("Amp(μV)")
ax0.axis([np.min(t),np.max(t),-2000,2000])
ax0.plot(t,x,color='g')

ax1 = plt.subplot(212)             #画频域信号-频谱
ax1.set_xlabel("Freq(Hz)")
ax1.set_ylabel("Power")
ax1.plot(xFreqs, xFFT,color='orange')
plt.show()