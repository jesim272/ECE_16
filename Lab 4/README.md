Jesi Miranda-Santos


A14989720

# Lab 4
#
## Introduction
#
The objective of this lab was to connect the BLE modules and IMU sensor such that we can read sensor values. In addition to reading the sensor values, we stored the data in an external file by writing to it and read from it as well. In this lab, we also plotted the sensor values using the code that was provided to us.
#
### Objective 1
#

1. The goal of this objective was better understand the robust interface the the BLE modules use and, in doing so, understand how objective oriented programming is efficient. Moreover, we added onto the code provided by sending *AT+NAME?* instead of *Connected* and reading a response up to the ";" character.

2. Initially, we tested the OO solution provided and compared it to the one we wrote in Lab 3. After testing the new, we moved on to modify the *Bt_basic.py",* rename **BT_basic_handshake.py**, by changing *"AT+NAME?"* in place of *"Connected"* and print the statement *"Connection established and confirmed"* after connection to BLE module was successful. Additionally, data received was read until the **";"** was encountered. In this lab we also created a *"Library"* file with an empty .py file so that the Library may be used when creating other .py files.
   
 By doing so we had to changed the Spyder settings. This was done by going to **Tools>PYTHONPATH Manager"** and clicking **"Path"**, where we selected our *base* folder. We restarted Spyder and tested using the line:
 ```   
   from Libraries.Bt import Bt
 ```
  
### Objective 2
#
1. The goal of this objective was to add the IMU sensor to the BLE module. We had to integrate this sensor with the rest of the code that we have written and print the sensor values to the Serial Monitor and also to the python script, where we printed the values.

2. We downloaded the i2cdev libraries and included them into the Arduion IDE by following the following steps **Sketch->Include Library->Add .ZIP Libarary...**, we were included all the contents of **MPU6050** and **I2Cdev**. Downloading the provided code, we plotted the three accelerometer values. 

   ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%204/Objective%202/BLEDataTransmit/Objective2a.png "Objecive2a.png")

   Depending on how the IMU moves, the values will either intersect or remain fairly constant. The blue line moves with respect to the z-axis, the red with respect to the y-axis, and the green with respect to the x-axis. The colors depend on the number of lines to plot. 
   
   ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%204/Objective%202/BLEDataTransmit/Objective2b.png "Objective2b.png")
    
    As can be seen, the data sent to the python file i as desired in terms of formatting: *<current_time>,\<x-axis IMU val>;*. Here the functions, 
    ```
    dtostrf() and sprintf()
   ```
   were used to convert the data values into strings, where was what the python script printed out.
   
  #
  #### Objective 3
  #
  1.  The objective of this lab was to visualize the IMU data on the Arduin side using the Serial Plotter, and send the data vai the BLE module to the computer, where is will be plotted using the python script.
  2. We downloaded the python files provided to us in the powerpoint. Next, we configured the Spyder to be able to plot the data. We followed the following steps: **Tools>Preferences> click "IPython Console" > click "Graphics" tab" > change "Backend" to "Automatic" > "Apply" > close and restart Spyder.
  After doing this, we downloaded code provided again and tested. We modified the file get_data() to be able to print the data being sent by the Arduino via the BLE module. The link shows the working program and the data of the IMU being plotted. In this objective, we only plotted the x-axis value of the IMU. 
   
  link: https://www.youtube.com/watch?v=EiL8tjI_nPk
  
  #
  #### Objective 4
  #
  1. The goal of this objective was to be able to plot and write/read to a file to data that was being plotted in Objective 3
  2. Using objective 3, we just added code to be able to write to a file and read from the file. Once again, we updated get_data() function to include the read/write to file functionality. Here is the picture where the program read from file that was created.
  
  ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%204/Objective%204/Objective4.png "Objective4.png")
