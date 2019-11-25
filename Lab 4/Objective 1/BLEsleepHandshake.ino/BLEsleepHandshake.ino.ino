/********************************************************************************
** Read from BLE and display on OLED
** Send symbol to BLE when connected
** The BLE toggles between sleep and awake when the button is pressed
** Updated handshake
*********************************************************************************/

// BT Library
#include <AltSoftSerial.h>
// Display Libraries
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#define SCREEN_WIDTH 128   // OLED display width, in pixels
#define SCREEN_HEIGHT 32   // OLED display height, in pixels
#define OLED_RESET    -1  // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
AltSoftSerial BTserial;

// Variables
char text[64];                                  // Character buffer
char c;
boolean asleep = false;
boolean confirmedCentral = false;


// Timing variables
unsigned long startTime = 0;
unsigned long endTime = 0;
const unsigned long period_us = 1e6;            // We are using microseconds for accuracy, 1s=1e6us


// Define pin numbers
const int buttonPin = 4;                        // Button pin
int value = 0;
boolean flag = false;
// --------------------------------------------------------------------------------
// Button logic: return true of the button is pressed, otherwise return false
// For more stable code, we can debounce the button
// --------------------------------------------------------------------------------
boolean checkButton() {
  static int buttonState = HIGH;                 // Pushbutton status
  if (digitalRead(buttonPin) != buttonState) {
    buttonState = !buttonState;
    if (buttonState == HIGH) {
      value++;
      flag = true;
      return true;
    }
  }
  return false;
}


// --------------------------------------------------------------------------------
// Initialize the OLED display
// --------------------------------------------------------------------------------
void initDisplay() {
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



// --------------------------------------------------------------------------------
// Show a message on the OLED display
// --------------------------------------------------------------------------------
void showMessage(char message[]) {
  display.setCursor(0, 0);     // Start at top-left corner
  display.clearDisplay();
  display.println(message);
  display.display();
}



// --------------------------------------------------------------------------------
// Forward data from Serial to the BLE module
// This is useful to set the modes of the BLE module
// --------------------------------------------------------------------------------
void forwardSerialToBLE() {
  static boolean NL = true;

  c = Serial.read();
  if (c != 10 & c != 13 )  // do not send line end characters to the HM-10
    BTserial.write(c);
  // Copy the user input to the main window; if there is a new line print the ">" character.
  if (NL) {
    Serial.print("\r\n>");
    NL = false;
  }
  Serial.write(c);
  if (c == 10)
    NL = true;
}


// --------------------------------------------------------------------------------
// This function reads characters from the HM-10
// It's main goal is to detect if the central is sending "AT+..." indicating the handshake is not completed
// If a "T" is received right after an "A", we send back the handshake confirmation
// The function always returns the new character
// --------------------------------------------------------------------------------
char receiveFromBLE() {
  static char lastChar;

  char newChar = BTserial.read();
  switch (newChar) {
    case 'A':                                       // Starting AT Command reading
      lastChar = newChar;
      break;
    case 'T':                                       // AT was received
      if (lastChar == 'A') {
        BTserial.write("PeripheralConnected");
        Serial.print("PeripheralConnected");
        delay(50);
        BTserial.flushInput();           // Purge buffer
        confirmedCentral = true;
        lastChar = 0;
      }
      newChar = 0;                                  // This will clear the display
      break;
    default:                                        // Receiving data
      lastChar = newChar;
  }
  return newChar;
}




// --------------------------------------------------------------------------------
// Toggle BLE sleep state
// --------------------------------------------------------------------------------
void BLEConnect() {
  // Disconnect and put to sleep
  if (!asleep) {
    BTserial.print("AT");
    delay(150);
    BTserial.print("AT+ADTY3");
    delay(50);
    BTserial.print("AT+SLEEP");
    asleep = true;
    confirmedCentral = false;
  }
  // Wake up and re-establish connection
  else {
    BTserial.print("AT+ADTY0");
    if ((value % 2 == 0) && flag) {
      BTserial.print("AT+galliaestomnisdivisainpartestresquarumunamincoluntbelgaealiamaquitanitertiamquiipsorumlinguaceltaenostragalliappellantur");
      delay(350);
      BTserial.print("AT+ADTY0");
      delay(50);
      BTserial.print("AT+RESET");
      delay(350);
      BTserial.flushInput();           // Purge buffer
      asleep = false;
      value = 0;
      flag = false;
    }
  }
}


// --------------------------------------------------------------------------------
// Setup: executed once at startup or reset
// --------------------------------------------------------------------------------
void setup() {
  // Initialize the OLED display
  initDisplay();
  showMessage("Initializing ...");
  delay(1000);

  // Initialize Serial (needed for setting the mode of the BLE)
  Serial.begin(9600);

  // Initialize the BT Serial (AltSoftSerial)
  BTserial.begin(9600);
  Serial.println("BTserial started");
  pinMode(buttonPin, INPUT_PULLUP);
  // Clear the display
  showMessage(" ");
}


// --------------------------------------------------------------------------------
// Loop: main code; executed in an infinite loop
// --------------------------------------------------------------------------------
void loop() {

  // Check if the button was pressed
  // If it was, establish or re-establish a BT connection
  if (checkButton())
    BLEConnect();

  // If we are asleep, do nothing until the button is pressed again
  if (!asleep) {

    // Read from the Bluetooth module and store in a char array
    int i = 0;
    while (BTserial.available()) {
      text[i++] = receiveFromBLE();
      delay(10);                        // Allow time for new characters to come in
    }

    // If a new message was received, show it
    if (i > 0) {
      showMessage(text);
      Serial.println(text);
    }

    // Read from the Serial Monitor and send to the Bluetooth module
    if (Serial.available())
      forwardSerialToBLE();

    // If we received a message from the computer, we know we are connected. Start sending data back
    if (confirmedCentral) {
      endTime = micros();
      if (endTime - startTime >= period_us) {
        startTime = endTime;
        BTserial.print("*;");               // Added the ';' termination character
        Serial.println("*;");
      }
    }
  }

}
