import scipy.signal as sig
import matplotlib.pyplot as plt
import numpy as np
import statistics as stat

pfiles = ["C:\\Users\Jesi\Desktop\\ECE_16\\Lab 8\\pedometer_training_active(lab8_2).csv",
          "C:\\Users\\Jesi\\Desktop\\ECE_16\\Lab 7\\Objective 3\\pedometer_training_resting.csv"]
t, ir, imu = np.loadtxt(pfiles[0], delimiter=",", skiprows=1, unpack=True)


plt.figure(1)
f, p = sig.welch(imu, fs = 20)
plt.plot(f,p)
#convert to list
p = list(p)
f = list(f)
#1.6 to 2.6 hZ count as step
# 2.0 e 18 < height < 2.6 e18  
print(f)
print(p)


plt.plot(f,p)

plt.show()