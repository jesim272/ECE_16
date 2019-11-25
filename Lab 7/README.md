Jesi Miranda-Santos (Primary)   A14989720  
Diego Ramos (Secondary)   A14935625

# Lab 7
#
## Introduction
#
 This goal of this lab was to re-integrate the heart rate detector and also to re-integrate the IMU. We also explored more on machine learning 
 by using the KNN method. Additionallly, we added a new library called *Timer.py*. This is used to set the timer for reading data from the 
 IMU
#
### Objective 1
#

1. The goal of this objective was re-integrate our heart rate detector. Additionally, we switched from reading data from a file to reading
data from the BLE. We, moreover, ended up live plotting the data coming in.

2. We started by using the previous python file *process_sensordata.py* and renamed it to *process_hr.py* . We also changed the name
of our class *Hr_basic.py* to *hr.py*. After doing all this, we proceeded to implement the timer and pass in 1 second of data to 
*hr.process*. We live plotted and made sure that the program ran well. Our Hr heuristics still needs to be robust.

Video link: https://www.youtube.com/watch?v=xbU8YIfZYbc 

#
### Objective 2
#
1. The goal of this objective was to re-integraate the IMU and send accelerometer values (ax, ay, az) via the BLE module. We plotted and saved
the data coming in and we found the Power Spectral Density of the data for imu
2. In this objective we modified the python file to be able to accept imu values and store it in a data buffer like the ir value. 
On the Arduino side we modified the code slighly to send the imu value in the format of **"<time>, <ir>, <imu>;" **. After sending 
the imu value to the python, via the BLE, we save the data into csv files. Three files were created to store the accelerometer values
in the x-axis, y-axis, and z-axis. In my opinion, the y-axis and the x-axis gives use a relatively amount of good data when walking. We can
avoid filtering out signals that are extremely large compared to the average peaks for the entire data set. 

  ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%207/Images/welch.PNG "welch.PNG")
  
  Based on the PSD, the y-axis gives use the most relevant data.The frequency of walking is about 1-2 Hz which is clearly seen from the 
  y-axis of the PSD. Based on the PSD graph, it is pretty useful knowing which axis will generate the most useful and relevant data. However,
   all the axis are important to fully charting and finding the rythmic of walking
  
#
### Objective 3
#
  1.  The goal of this objective was implement the method that sends over from Arduino to Python the combination of values from all the 
  three axis. This, in turn, will yield a much more precise graph with with rythm of walking.
  
  2. On the Arduino side, we implemented the line of code 
  ```
  L1 = abs(ax) + abs(ay) + abs(az)
  ```   
  This value was substituted for the previous IMU value, which was just a single axis not all three axes. 
    On the python side, we added a few lines of code in the gathering of data from IMU, we simply did this:
    ```
    data = [float(t.strip()), float(ir.strip()), (3*16384) - abs(float(imu.strip()))]
    ```
       
   We also filtered the data coming from the IMU and and stored in the data buffer that we had previously used to store the individual 
    data axis from IMU. We live plotted the data.
    
   ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%207/Images/L1_norm.png "L1_norm.PNG")
    
   We also ended up calibrating the IMU for objective 4. We had to change the Serial Monitor to the default baudrate 9600.
#
### Objective 4
#
  1.  The goal of this objective was to create a class **pedometer** and implement the KNN algorithm just how we implemented the 
  GMM for **hr.py**. The end goal was to be able to differentiate between data when the user is "resting" or is "active".
  
  2. We downloaded the starter code and added onto it as we did for the **Hr.py** file. We followed the intructions given in the file and 
  those that were given in the Lab 7 Powerpoint slide. We split that data using the function
     ```
     np.array_split(data_active1,self.window_length)
     ```   
     Inisde of *extract_features()*, we once again split the data with the line of code
     ```
     np.array_split(imu, 10)
     ```
     This split the data into 10 more chunks. We Now has an array with arrays of 100 elements, that were no being split into ten arrays.
     So, basically, it was an array of arrays that contained arrays of ten elements. We found the max vlaues of each array and calculated 
     peak mean. 
     
     Back in the class file, we split the training data and validation data, and combined them. Using my data, we ended up getting an accuracy of
     0.9414893617021277. 
  
  
  
#
### Final Notes
#
 
 Diego:


Jesi:
