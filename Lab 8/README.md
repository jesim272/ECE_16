Jesi Miranda-Santos (Primary)   A14989720  
Diego Ramos (Secondary)   A14935625

# Lab 8
#
## Introduction
#
 This goal of this lab was to continue developing the pedometer class by including a heuristic to count the number of steps. Additionally,
 we established two-way communication wtih the Arduino by sending the heart rate and step count via the BLE module. Lastly, we implemented
  a vibrating motor to give feedback for every 5 steps that a user takes.
#
### Objective 1
#

1. The goal of this objective was to include a pedometer heuristics and precisely count the number of steps a user takes. We processed 
5 seconds worth of data and determined what was an appropriate range for arm swing when walking. Any peak within that range will count as 
a step.

2. We started by uncommenting process() and implementing our own function to count the number of steps. We took 5 second of IMU data, filtered it, and based on certain peaks we, determined which peaks were walking-hand-swing peaks from regular peaks. We printed out the number of steps on the Python console.

Video link: https://www.youtube.com/watch?v=vtkxMkuhsww
#
### Objective 2
#
1. The goal of this objective was to establish two-way communication with Python and Arduino by sending the HR and pedometer information from the Python to the Arduino and printing it out in the OLED.  
   
2. To send the HR and OLED information to the Ardiuno, simply integrate the line of code 
```
 "HR:" <hr data>+ "," + "Steps:" + <step count> + ";"
```     
 On the Python, side we are done. On the Arduino side, we had to simply change the "," to be replaced by "\n". Also, we had to 
 call the function *show_message()* to display the text recieved from the Python side. 
 
 Video line: https://www.youtube.com/watch?v=7HL3QrnQIQ8
#
### Objective 3
#
  1.  The goal of this objective was implement the vibrating motor or every 5 steps that the user takes. This motor's purpose is to act as a feedback/alert mechanism 
  
  2. After properly conecting the vibrating motor, we integrating the motor code with the rest of the Arduino code to vibrate twice every time the step counter reaches a multiple of 5. We used the code provided from the PowerPoint slide. Additionally, we added the line of code in the loop:
  ```
  digitalWrite(vibMot, HIGH)
  ```
  in the loop, to make the motor turn off since it begins by always vibrating. We also converting the incoming string of the step count into an integer (up to 4 digits). Based on this, if count was a multiple of 5, we called the function *vibMotor()* to vibrate the motor twice. 
  
  Video Link: https://www.youtube.com/watch?v=ySgADWSOu_o
#
### Objective 4
#
  1.  Pedometer improvements:
    We plan on using the average numbero of peaks in 5 seconds to determine if there was a step or not. For instance, if the average of steps in 5 seconds is 4, then we can eliminate hand swings and integrate the frequency of steps. In other words, if 4 steps at least is not detected in 5 seconds, then it was probably not a step.
  
 2. Heart rate improvements:
   We plan on using the frequency of peaks to determine if there was a heart beat or not. Also, we plan on integrating a range for which the heart beat is reasonable. For instance, if user is resting, the peak of the heart beat will be expected to be within a certain range but if the heart rate increase (together with frequency of peaks) the range will change and meausure the average height peak. It will be something similar to the pedometer, which works pretty well.
   
#
### Final Notes
#
 Soldered board Image:
 
  ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%208/Images/Soldered_board.jpg "Soldered Board.png")
  
  
Diego:

Jesi:
