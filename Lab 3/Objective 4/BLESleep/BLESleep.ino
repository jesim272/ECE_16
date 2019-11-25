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
boolean NL = false;           //delete
boolean NL2 = true;
unsigned long starttime;
boolean flag = false;
int count = 0;                    //delete
int count2 = 0;         //for earsing commands on OLED
int num = 0;            //for incrementing * count
const int buttonPin = 4;                // Pushbutton pin
int flag1 = 0;            //using
int value = 0;
int number1 = 0;        //delete

void setup()
{
  Serial.begin(9600);
  set_Display();
  Serial.println("Display set");
  while (!Serial) {};

  // Initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT_PULLUP);

  BTserial.begin(9600);
  Serial.println("BTserial started");
}

void loop()
{
  // Read from the Bluetooth module and send to the OLED
  if (BTserial.available())
  {
    if (!checkButton()) {
      delay(150);
    }
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
      count++;
    }
    if (c == '?') {
      NL2 = false;
      if (count2 >= 8) {
        set_Dis();
        display.display();
        count2 = 0;
      }
    }

    if ((millis() - starttime > 1000) && flag)      //flag for being connected
    {
      BTserial.write('*');
      //Serial.println('*');
      starttime = millis();
      num++;
      set_Dis();
      display.print("Number: ");
      display.print(num);
      delay(100);
      display.display();
    }

  }
}

boolean checkButton() {

  if (!digitalRead(buttonPin)) {     // Off unless button is pressed
    ++flag1;                          //Flag used to determine if button is pressed
    value++;                         // set value to 1
    delay(250);                      //delay by 1/8 of a second for processing time
    if (flag1 == 1) {
      BTserial.write("AT");
      delay(150);
      BTserial.write("AT+ADTY3");
      delay(150);
      BTserial.write("AT+SLEEP");
      delay(150);

      //Serial.print("Button flag: ");
      //Serial.println(flag);
    }


    if (!(value % 2)) {              //check if button was presse again, else remain in state

      // in prior state
      value = 0;                     //Set value to 0
      //endtime += millis() - starttime; //end time
      flag1 = 0;                       //reset times_pushed
      BTserial.write("AT+fffffffffffffffffffffffffffffffffffff\
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffff\
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffff\
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffff\
        ffffffffffffffffffffffffffffffffffffffffffffffffffffffff");
      delay(150);
      BTserial.write("AT+ADTY0");
      delay(150);
      BTserial.write("AT+RESET");
      delay(150);

      //Serial.print("Button flag off: ");
      //Serial.println(flag);
      delay(150);
    }
    // Serial.println("Button still in state");
    return true;
  }
  else {
    //Serial.println("Button not pressed since");
    return false;                     //Return false if button is not pressed
  }
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
