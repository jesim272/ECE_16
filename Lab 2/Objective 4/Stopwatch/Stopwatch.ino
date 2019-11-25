#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128   // OLED display width, in pixels
#define SCREEN_HEIGHT 32   // OLED display height, in pixels
#define OLED_RESET    -1  // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);


int buttonPin = 4;       //Initialize buttonPin to Pull-up resistor Pin
int value;               //Declare value as global
int flag;        //check the number of times button has been pushed(delete)

unsigned long starttime, endtime, new_time;

void setup() {
  pinMode(4, INPUT_PULLUP);                     //Set pin 4 as pull-up resistor
  Serial.begin(9600);                           //Serial communication
  set_Display();
}

void loop() {

  if (checkButton()) {
    display.clearDisplay();
    display.setCursor(0, 0);
    display.print("Time: ");
    display.print(new_time / 1000L);
    display.display();
    delay(150);
  }

}

//Function checks if the button was pressed
boolean checkButton() {

  if (!digitalRead(buttonPin)) {     // Off unless button is pressed
    ++flag;                          //delete
    delay(250);                      //delay by 1/8 of a second for processing time
    value++;                         // set value to 1
    if (flag == 1) {
      starttime =  millis();          //start time when button is pressed
    }

    if (!(value % 2)) {              //check if button was presse again, else remain in state
                                      // in prior state
      value = 0;                     //Set value to 0
      endtime += millis() - starttime; //end time
      flag = 0;                       //reset times_pushed
    }
    return true;
  }
  else {

    if (value == 1) {
      display.clearDisplay();
      display.setCursor(0, 0);
      new_time = millis() - starttime + endtime;                //stores the seconds incremented
      display.print("Time: ");
      display.print(new_time / 1000L);
      display.display();
    }
    return false;                     //Return false if button is not pressed
  }
}



void set_Display() {
  //Set up OLED display for printing to Display
  // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3C for 128x32
    Serial.println(F("SSD1306 allocation failed"));
    for (;;); // Don't proceed, loop forever
  }

  // Show initial display buffer contents on the screen --
  // the library initializes this with an Adafruit splash screen.
  display.display();
  delay(1000);                  // Pause for 1 seconds
  display.clearDisplay();       // Clear the buffer

  display.setTextSize(2);        // 2x pixel scale
  display.setTextColor(WHITE);   // Draw white text
  display.setCursor(0, 0);       // Start at top-left corner
  display.cp437(true);           // Use full 256 char 'Code Page 437' font
}

