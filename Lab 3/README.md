Jesi Miranda-Santos


A14989720

# Lab 3
#
## Introduction
#
The objective of this lab was to get us familiaar with interfacing with the HM-10 module in Python with our laptop and Arduino. Moreover, we refreshed our understanding in programming in Python, which we used to write a script to connect the HM-10 connected in our laptop to the HM-10 connected to the Arduino using Serial communication such that when they connect an increment begins based on the data being sent from the Arduino to the HM-10 connected to the laptop. We also re-implemented the button switch to put the HM-10 to sleep and wake up after a certain response.
#
### Objective 1
#

1. The goal of this objective was to refresh our understanding in programming in Python so that we may be prepared to write a script for the HM-10 connected to our laptop so that it may connect with the HM-10 connected to the Arduino.

2. We were able to refresh our skills by following the link provided on the PowerPoint :
  https://gist.github.com/adriangb/948ab7f4ff8b53356a7fba2e59717106
  Here, we use Spyder to compile and test the code. Moreover, we used most of the functions to write a script for interacting with the HM-10 module and learning how to interact with BTserial. 
  
### Objective 2
#
1. The goal of this objective was to establish communication with the HM-10 module while being connected to the laptop. Additionally, we used PySerial to send commands to the HM-10 and print out the response.
2. We connected the HM-10 to our laptops and had to download some drivers to be able to ensure a connection. We downloaded the files from this site:
  https://learn.adafruit.com/adafruits-raspberry-pi-lesson-5-using-a-console-cable?view=all#software-installation-windows
  After downloading the drivers, we used Spyder to connect to the HM-10 and ran a test script to make sure that a connection was estalbished. On the script, we had to finish writing the functions **read_BLE()** and **write_BLE()**. The **write_BLE()** function encoded the string being sent to the HM-10 while the **read_BLE()** decoded the string and printed out the response to the command sent.
  
   
  #
  #### Objective 3
  #
  1. The goal of this objective was to use the BLE modules to communicate between the HM-10 conencted to the computer to the HM-10 connected to the Arduino. The goal was also to print out an increment, which  began right after the BLE_module connected to the Arduino(which sent the text *"Connected"*), and printed to the OLED *"Number: ").
  
  2. We used the AT_commands that were provided in Lab 2 to be able to connect to the two BLE modules. We had to set the HM-10 connected to the laptop as the **central**, while the HM-10 connected to the Arduino was set to **peripheral**. I personally used *Lab 2* to make sure how the BLE modules connect. The only part that I looked for was chagning the roles, using the command **AT+ROLE0** (for central) and **AT+ROLE1** (for peripheral). I also changed the immediate connection by using the command **AT+IMME0** (for central) and **AT+IMME1** (for peripheral). These states have to be set as such for the HM-10 modules to successfully connect. 
  Additionally, we modified the Python and Arduino script so that the BLE modules can responsd to commands. The Python script had a loop that ran the command **AT+CONN** to connect to the HM-10 module connected to the Arduino. After connection was established the HM-10 modules connected to the Arduino sent *"*"* and the HM-10 module connected to the one on connected to the laptop.
  video link: https://www.youtube.com/watch?v=jD7F_QUBghQ 
  #
  #### Objective 4
  #
  1. The goal of this objective is to implement and integrate a pushbutton by using the Arduino as a pull-up resistor and display the timer on the OLED
  
  2. Here is a link to the video of the button turning off the HM-10
    https://www.youtube.com/watch?v=sciXQZdu1IE 
   
