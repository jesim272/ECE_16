/**************************************************************************
  This is an example for our Monochrome OLEDs based on SSD1306 drivers

  Pick one up today in the adafruit shop!
  ------> http://www.adafruit.com/category/63_98

  This example is for a 128x32 pixel display using I2C to communicate
  3 pins are required to interface (two I2C and one reset).

  Adafruit invests time and resources providing this open
  source code, please support Adafruit and open-source
  hardware by purchasing products from Adafruit!

  Written by Limor Fried/Ladyada for Adafruit Industries,
  with contributions from the open source community.
  BSD license, check license.txt for more information
  All text above, and the splash screen below must be
  included in any redistribution.
 **************************************************************************/

#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 32 // OLED display height, in pixels


// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
#define OLED_RESET     4 // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

#define LOGO_HEIGHT   16
#define LOGO_WIDTH    16
static const unsigned char PROGMEM logo_bmp[] =
{ B00000000, B11000000,
  B00000001, B11000000,
  B00000001, B11000000,
  B00000011, B11100000,
  B11110011, B11100000,
  B11111110, B11111000,
  B01111110, B11111111,
  B00110011, B10011111,
  B00011111, B11111100,
  B00001101, B01110000,
  B00011011, B10100000,
  B00111111, B11100000,
  B00111111, B11110000,
  B01111100, B11110000,
  B01110000, B01110000,
  B00000000, B00110000
};

void setup() {
  
  Serial.begin(9600);

  // SSD1306_SWITCHCAPVCC = generate display voltage from 3.3V internally
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3C for 128x32
    Serial.println(F("SSD1306 allocation failed"));
    for (;;); // Don't proceed, loop forever
  }

  // Show initial display buffer contents on the screen --
  // the library initializes this with an Adafruit splash screen.
  display.display();
  delay(2000);                  // Pause for 2 seconds
  display.clearDisplay();       // Clear the buffer

 

  testdrawbitmap();                                                 // Draw a small bitmap image

  display.setTextSize(1);                                           // Normal 1:1 pixel scale
  display.setTextColor(WHITE);                                      // Draw white text
  display.setCursor((SCREEN_WIDTH - LOGO_WIDTH-4)/2, 0);            // Somewhat in the center
  display.print(F("Ready"));
  display.display();
  delay(1000);
  // Clear the buffer
  display.clearDisplay();
}

char message[64];                                                  //initialize character limit for array 

void loop() {
  
  if (readSerial()) {                                             //If any input in Serial Monitor
    showMessage(message);                                         //then show the message inputted
  }
}


//-------------------------------------------------------------added functions----------------------------------------------------------------
boolean readSerial() {
  // If there are any bytes to read 
  if (Serial.available()) {
    memset(message, 0, sizeof(message));                          // Clear the buffer
    Serial.readBytesUntil('\n', message, 64);                     //storing bytes in message array
    return true;
  }
  return false;
}

//Function displays text written on the Serial Monitor
void showMessage(char message[]) {
  display.clearDisplay();                                        //Clears buffer for new text
  display.setTextSize(2);                                        // 2x pixel scale
  display.setTextColor(WHITE);                                   // Draw white text
  display.setCursor(0, 0);                                       // Start at top-left corner
  display.cp437(true);                                           // Use full 256 char 'Code Page 437' FONT

  for (int i = 0; i < strlen(message); i++) {                    //Iterate through each character in message
    display.print(message[i]);                                   //Print every character in the message
  }
  display.display();                                             //Display entire message all at once
  delay(2000);  
}

//-----------------------------------------------------------------------------------------------------------------------------------------------

//Function draws a small bitmap image
void testdrawbitmap(void) {
  display.clearDisplay();

  display.drawBitmap(
    (display.width()  - LOGO_WIDTH ) / 2,
    (display.height() - LOGO_HEIGHT) / 2,
    logo_bmp, LOGO_WIDTH, LOGO_HEIGHT, 1);
  display.display();
  delay(1000);
}

