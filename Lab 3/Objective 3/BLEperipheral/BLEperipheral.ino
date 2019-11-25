#include <AltSoftSerial.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128   // OLED display width, in pixels
#define SCREEN_HEIGHT 32   // OLED display height, in pixels
#define OLED_RESET    -1  // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
AltSoftSerial BTserial;

char c = ' ';
boolean NL = true;
boolean NL2 = true;
unsigned long starttime;
boolean flag = false;
int count = 0;          //for earsing commands on OLED
int count2 = 0;
int num = 0;            //for incrementing * count
void setup()
{
  Serial.begin(9600);
  set_Display();
  Serial.println("Display set");
  while (!Serial) {};
  BTserial.begin(9600);
  Serial.println("BTserial started");
}

void loop()
{


  // Read from the Bluetooth module and send to the OLED
  if (BTserial.available())
  {
    c = BTserial.read();
    Serial.write(c);
    display.write(c);
    if (!NL2) {
      display.println();
      NL2 = true;
    }
    if (c == 'A') {
      count2++;
    }
    if (c == 'C') {
      set_Dis();
      display.println("Connected");
      display.display();
      delay(150);
      starttime = millis();       //start time after it is connected
      flag = true;                //flag to send * after 1 sec
      num = 0;
    }
    if (c == '?') {
      NL2 = false;
      //display.println();
      if (count2 >= 8) {
        set_Dis();
        display.display();
        //Serial.println("cleared");
        count2 = 0;
      }
    }
    
    if ((millis() - starttime > 1000) && flag)      //flag for being connected
    {
      BTserial.write('*');
      starttime = millis();
      num++;
      set_Dis();
      display.print("Number: ");
      display.print(num);
      //display.print(c);
      delay(100);
      display.display();
    }
    
  }



  // Read from the Serial Monitor and send to the Bluetooth module
  /* if (Serial.available())
    {
       c = Serial.read();
       // do not send line end characters to the HM-10
       if (c != 10 & c != 13 )
       {
        BTserial.write(c);
       }

       // Copy the user input to the main window, as well as the Bluetooth module
       // If there is a new line print the ">" character.
       if (NL) {
        Serial.print("\r\n>");
        NL = false;
       }
       Serial.write(c);
       if (c == 'A') {
        count++;
       }
       if (c == 'C') {
        set_Dis();
        display.println("Connected");
        display.display();
        delay(150);
        starttime = millis();       //start time after it is connected
        //flag = true;                //flag to send * after 1 sec
       }
       if (c == 10) {
        //NL = true;
        display.println();
        if (count >= 4) {
          set_Dis();
          display.display();
          //Serial.println("cleared");
          count = 0;
        }
       }
       }

    }*/
}

void set_Dis() {
  display.clearDisplay();       //clears display to only print Connected
  display.setTextSize(1);        // Normal pixel scale
  display.setTextColor(WHITE);   // Draw white text
  display.setCursor(0, 0);
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

  display.setTextSize(1);        // Normal pixel scale
  display.setTextColor(WHITE);   // Draw white text
  display.setCursor(0, 0);       // Start at top-left corner
  display.cp437(true);           // Use full 256 char 'Code Page 437' font
}
