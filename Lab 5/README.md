Jesi Miranda-Santos


A14989720

# Lab 5
#
## Introduction
#
 The objective of this lab was to introduce use to the concept of filtering and how we can use it to clean a signal input from an IR sensor to read our heart beat. Moreover, we integrated the filter with our previous code.
#
### Objective 1
#

## Part A
1. The goal of this objective was to build a simple IR sensors and to read input from the analog pin, which was the receiver.

2. After following the initial steps to building the IR sensor, we plotted our incoming signal. Here is the signal:
    
    ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%205/Images/Heartrate1a.png "Heartrate1a.png")
    
    ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%205/Images/IRcircuit1a.png "IRcircuit1a.png")

   Due to hardware issues, the signal does not look related to how the signal should actually be. In this case, it should be noisy and and have a lot of background signal being received, which will make the signal look very hard to pick out a heart beat.
  
 ## Part B
 1. The goal of this objective was to attempt to clean up the signal from Part A by adding a OpAmp to the circuit.
   
 2. After adding the OpAmp to the circuit, we can see that the signal being received was much better. However, there is still a good amount o background noise being read.
 
   ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%205/Images/Heartrate1b.png "Heartrate1b.png")  
     
   ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%205/Images/IRcircuit1b.png "IRcircuit2b.png")  
   
   The OpAmp amplifies the incomming signal and from the image above, it is clearly seen that we can detect a heart beat. Yet, there is still a good amound of background signal that we need to filter out.
   
    
### Objective 2
#
1. The goal of this objective was to integrate the IR sensor being received with the python script and plot it over in Spyder.

2. Instead of sending IMU data like before, we modified the Arduino code to receive IR data, which was sampled at 20HZ and live plotted.
  
  ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%205/Images/Heartrate2.png "Heartrate2.png")   
  
  
  #
  #### Objective 3
  #
  1.  The goal of this objective was to create a filter and filter the signal being provided from the files in the PowerPoint.  
  2. We downloaded the files provided, **FilterWrapperBasic.py** and **filter_test.py** in the PowerPoint and created a functional filter class. After creating the filter class, we tested it and plotted the incoming signal and the filtered signal. 
     ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%205/Images/filter_test.png "Filter_test.png")
     
     The filter very much helps clean the signal and output a nice sinusoidal wave. 
  #
  #### Objective 4
  #
  1. The goal of this objective was to live plot the IR signal and filter it using a Low-Pass filter and a High-Pass filter. Moreover, we had to read from a file and filter that file, and reread from the filtered file. 
  2. We downloaded a csv file "Heartrate_test.csv" and read from the file, filtered the file and live plotted, and wrote the filtered signal in another file (**"Heartrate_LPF.csv"**). Additionally, we re-read from the filtered file and passed it through a high-pass filter and wrote that filtered signal into another file (**"Heartrate_HPF.csv"**) 
   After filtering the file given, we proceeded to live plot the IR sensor and cascade the signal into a Low-Pass filter and then to a High-Pass filter, and then plotting it. 
    
   ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%205/Images/Heartrate_live.png "Heartreate_live.png")

I tried moving the IR emitter and receiver elsewhere in the body but the signal did not have same response as in the finger.

Here is the video link of the working demo:
   https://www.youtube.com/watch?v=dcFSRMLijEg 
