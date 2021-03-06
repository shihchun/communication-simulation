import matplotlib.pyplot as plt
import numpy as np
import simulation.multipath

# reference: http://matplotlib.org/users/mathtext.html

t = [0]*10000
a0 = [0j]*len(t)
a1 = [0j]*len(t)

#模擬的時間為0~250ms
for i in range(len(t)):
    t[i] = i/len(t)*0.25

#先來看看這個模型的振幅
for j in range(3):
    if j==0:
        fd = 10
        wm = 2 * np.pi * 10  #模擬wm = 2*pi*100 即 maximum doppler frequency 為10Hz
    elif j==1:
        fd = 50
        wm = 2 * np.pi * 50  #模擬wm = 2*pi*100 即 maximum doppler frequency 為50Hz
    else:
        fd = 100
        wm = 2 * np.pi * 100 #模擬wm = 2*pi*100 即 maximum doppler frequency 為50Hz
    for i in range(len(t)):
        a0[i] = simulation.multipath.rayleigh(wm,t[i],2)[0]# path 1
        a0[i] = abs(a0[i])
        a0[i] = 10*np.log(a0[i])
        a1[i] = simulation.multipath.rayleigh(wm,t[i],2)[1]# path 2
        a1[i] = abs(a1[i])
        a1[i] = 10*np.log(a1[i])

    plt.figure(r'$\omega_m=2*{0}\pi\/\/\/(path1)$'.format(fd))
    plt.title(r'$\omega_m=2\cdot{0}\pi(rad/s)\/\/\/or\/\/\/fd={0}(Hz)\/\/\/(path1)$'.format(fd))
    plt.xlabel('time (sec)')
    plt.ylabel('Rayleigh envelop in dB')
    plt.plot(t,a0)
    plt.xlim(0, 0.25)

    plt.figure(r'$\omega_m = 2*{0}\pi\/\/\/(path2)$'.format(fd))
    plt.title(r'$\omega_m = 2\cdot{0}\pi(rad/s)\/\/\/or\/\/\/fd={0}(Hz)\/\/\/(path2)$'.format(fd))
    plt.xlabel('time (sec)')
    plt.ylabel('Rayleigh envelop in dB')
    plt.plot(t,a1)
    plt.xlim(0,0.25)

#接下來看看這個模型的統計特性
t = [0]*100000
a0 = [0]*len(t)
a0_real = [0]*len(t)
a0_image = [0]*len(t)
a0_abs = [0]*len(t)
#取 0~10秒的點來進行觀察
#你會發現取0~100秒才會真的接近高斯分布
#取0~10秒的機率分布會很難看
for i in range(len(t)):
    t[i] = i/len(t)*100
for i in range(len(t)):
    a0[i] = simulation.multipath.rayleigh(wm,t[i],1)[0]# path 1 的振幅
    a0_real[i] = a0[i].real
    a0_image[i] = a0[i].imag

plt.figure('統計特性')
n,bins,c = plt.hist(a0_real,100,normed=True,label='pdf of channel fading real part')
y = [0]*len(bins)
std = 1/np.sqrt(2)
mu = 0
for i in range(len(y)):
    y[i] = 1/(np.sqrt(2*np.pi)*std)*np.exp(-((bins[i]-mu)**2)/(2*std**2))

plt.plot(bins,y,label='gaussian distribution (mean = 0, variance = 1/2)')
plt.ylabel('pdf')
plt.legend()
plt.show()




