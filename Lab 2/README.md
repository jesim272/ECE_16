Jesi Miranda-Santos


A14989720

# Lab 2
#
## Introduction
#
The objective of this lab was to indroduce us into using Bluetooth Low Energy (BLE) module and getting used to the commands to make it work. Additionally, we were introduced to using an OLED, which allowed us to display text and figures on the display screen. We also worked with implementing a push button for a stopwatch and using the Arduino as a pull-up resistor.
#
### Objective 1
#

1. The goal of this objective was to introduce us into using the Bluetooth Low Engergy (BLE) module and learning the commands to interact with it. Moreover, we had the opportunity to use the AT commands to change the BLE module features, such that we can have much more control over what devices we wiould like to connect to. 

2. Below is the image as to how the AT commands were used; I sent the commands through the Serial monitor.


  ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%202/Images/objective1.png "AT commands for BLE module")
  
  
#
### Objective 2
#
1. The goal of this objective was to learn how to manually connect to other devices using the AT commands.
2. To be able to connect to another device, one of the devices must be set as the central while the other must be set as peripheral. This is achieved by using the commands AT+ROLE0 and AT+IMME0, for peripheral, and changing the 0 to a 1 to be set as central.
The images below shows how this was achieved using the Serial monitor.

   ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%202/Images/objective2a.png "My device as a central")
   
   ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%202/Images/objective2b.png "My device as a peripheral")
   
  #
  #### Objective 3
  #
  
  ##### Part a
  1. The goal of this objective was to use the Arduino and establish communication with an external OLED display using I2C protocol. Additionally, we had to display a line of text taken from the Serial monitor and print it to the display.
  2. Following the instructions provided, I connected the board to my computer and on the Arduino application, I downloaded the libraries required: Wire.h, Adafruit GFX, and Adafruit SSD1306 
  Then, I moved on to open an example colde for the OLED display, by following the line of instructions given: 
  **File->Examples->Adafruit SSD1306->ssd1306_128x32_i2c**.
  
  After compiling the code and uploading it to the board, I saw that the OLED was turning on and flashed various designs.
  Reading through the code and understanding how every line works, I proceeded into adding lines of code to read from the Serial Monitor and display the text on the OLED. I added the function *void showMessage()* to do exactly what is stated above. Moreover, in the *setup()*, I included the lines
  `display.setTextSize(1);                                           // Normal 1:1 pixel scale
  display.setTextColor(WHITE);                                      // Draw white text
  display.setCursor((SCREEN_WIDTH - LOGO_WIDTH-4)/2, 0);            // Somewhat in the center
  display.print(F("Ready"));
  display.display();
  delay(1000);
  // Clear the buffer
  display.clearDisplay();
  `
  This block of code initializes the OLED display to be able to display text. Additionally, I included previous code from Lab 1,(the function *readSerial* so that the character array *messsage[64]* contains the text that was written on the Serial Monitor.
  After compiling the code, the OLED displayed the line of text that I inputted.
  
  ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%202/Images/oled_board.png "OLED TExt Display")
  
  ##### Part b
  1. The goal of this objective is to become faimliar and gain expertise in soldering properly and knowing how to solder.
   
   2. Here is a picture of the board that I had to solder. 
  ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%202/Images/objective%203.png "Soldered Board")
  
 
  #
  #### Objective 4
  #
  1. The goal of this objective is to implement and integrate a pushbutton by using the Arduino as a pull-up resistor and display the timer on the OLED
  
  2. Here is a link to the video of the stopwatch working
    https://www.youtube.com/watch?v=XDjoPLlwwWM&feature=youtu.be
