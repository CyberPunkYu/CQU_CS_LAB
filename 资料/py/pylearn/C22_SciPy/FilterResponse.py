from scipy import signal
from matplotlib import pyplot as plt
import numpy as np

def butterBandPassFilter(lowcut, highcut, samplerate, order):
    "生成巴特沃斯带通滤波器"
    semiSampleRate = samplerate*0.5
    low = lowcut / semiSampleRate
    high = highcut / semiSampleRate
    b,a = signal.butter(order,[low,high],btype='bandpass')
    print("bandpass:","b.shape:",b.shape,"a.shape:",a.shape,"order=",order)
    print("b=",b)
    print("a=",a)
    return b,a

def butterBandStopFilter(lowcut, highcut, samplerate, order):
    "生成巴特沃斯带阻滤波器"
    semiSampleRate = samplerate*0.5
    low = lowcut / semiSampleRate
    high = highcut / semiSampleRate
    b,a = signal.butter(order,[low,high],btype='bandstop')
    print("bandstop:","b.shape:",b.shape,"a.shape:",a.shape,"order=",order)
    print("b=",b)
    print("a=",a)
    return b,a

iSampleRate = 2000

plt.figure(figsize=(12,5))
ax0 = plt.subplot(121)
for k in [2, 3, 4]:
    b, a = butterBandPassFilter(3,70,samplerate=iSampleRate,order=k)
    w, h = signal.freqz(b, a, worN=2000)
    ax0.plot((iSampleRate*0.5/np.pi)*w,np.abs(h),label="order = %d" % k)

ax1 = plt.subplot(122)
for k in [2, 3, 4]:
    b, a = butterBandStopFilter(48, 52, samplerate=iSampleRate, order=k)
    w, h = signal.freqz(b, a, worN=2000)
    ax1.plot((iSampleRate*0.5/np.pi)*w,np.abs(h),label="order = %d" % k)

for a in [ax0,ax1]:
    a.plot([0, 0.5 * iSampleRate], [np.sqrt(0.5), np.sqrt(0.5)],
             '--', label='sqrt(0.5)')
    a.set_xlabel('Frequency (Hz)')
    a.set_ylabel('Gain')
    a.grid(True)
    a.legend(loc='best')

plt.show()