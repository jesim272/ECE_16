/********************************************************************************
** Read from BLE and display on OLED
** Send symbol to BLE when connected
** The BLE toggles between sleep and awake when the button is pressed
** Updated handshake
*********************************************************************************/
/*Last updated 5/27/19 */
// BT Library
#include <AltSoftSerial.h>

// Display Libraries
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#include <U8x8lib.h>
#define OLED_RESET    -1  // Reset pin # (or -1 if sharing Arduino reset pin)
U8X8_SSD1306_128X32_UNIVISION_HW_I2C u8x8(/* reset=*/ OLED_RESET);

// IMU Libraries
#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include "Wire.h"

#define SCREEN_WIDTH 128   // OLED display width, in pixels
#define SCREEN_HEIGHT 32   // OLED display height, in pixels
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);
AltSoftSerial BTserial;

// Variables
char out_text[32];                                 // Character buffer
char in_text[64];                                  // Character buffer
char time_buf[10] = "" ;                        //Time buffer (empty)
char x_axis_buff[10] = "";                      //IMU x-axis buffer (empty)
char IMU_val[64] = "";
char c;
boolean asleep = false;
boolean confirmedCentral = false;

// IMU data variables
int16_t ax, ay, az, tp, gx, gy, gz;

// Timing variables
unsigned long startTime = 0.0;
unsigned long endTime = 0.0;
const int sample_rate = 20;
const unsigned long period_us = 1e6 / sample_rate;           // We are using microseconds for accuracy, 1s=1e6us


// Define pin numbers
const int interruptPin = 2;
volatile bool imuDataReady = false;
const int buttonPin = 4;                        // Button pin
const int ledPin = 13;                          //LED pin
int vib_mot = 3;                          //Motor Pin
bool mod5 = false;
int value = 0;
float time_interval = 0.0;
boolean flag = false;
int num_from_Py = 0;
//IR Sensor Pin
const int analogPin = A2;
int ir_value = 0;

// IMU Setup
const int MPU_addr = 0x68;                      // I2C address of the MPU-6050
MPU6050 IMU(MPU_addr);                          // Instantiate IMU object
unsigned long L1;
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
  /*
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
  */
  u8x8.begin();
  u8x8.setPowerSave(0);
  u8x8.setFont(u8x8_font_amstrad_cpc_extended_r);
  u8x8.setCursor(0, 0);

}

// --------------------------------------------------------------------------------
// Function to check the interrupt pin to see if there is data available in the MPU's buffer
// --------------------------------------------------------------------------------
void interruptPinISR() {
  // Indicate data is ready
  imuDataReady = true;
}


// --------------------------------------------------------------------------------
// Show a message on the OLED display
// --------------------------------------------------------------------------------
void showMessage(const char * message, int line = 1, bool clear = true);
void showMessage(const char * message, int line, bool clear) {
  if (clear) {
    u8x8.clearDisplay();
  }
  u8x8.setCursor(0, line);
  u8x8.print(message);
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
    //Serial.print("\r\n>");
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
  static int i = 0;

  char newChar = BTserial.read();

  if (lastChar == 'A' && newChar == 'T') {
    BTserial.write("#");                          // Python uses "#" as a confirmation that the connection was succesful
    confirmedCentral = true;                      // Set Arduino-side flag for successful connection
    delay(50);                                    // Ensure all remaining handshake text has been received
    showMessage(" ");                             // Clear OLED display
    BTserial.flushInput();                        // Purge BLE buffer
    lastChar = 0;
    i = 0;                          // Reset receiveFromBLE() logic
    time_interval = 0.0;
    return false;                                 // Return to main loop
  }
  if (i >= sizeof(in_text) - 1) {
    i = 0;
    Serial.println("Received >64 bytes of data, buffer was reset");
  }
  if (newChar == ';') {

    num_from_Py = ((in_text[i-4] %16)*1000) + ((in_text[i-3] % 16)*100) + ((in_text[i-2] % 16)*10) + (in_text[i-1]%16);     //added; convert last 4 strings into a digit
    //Serial.println(num_from_Py);                                                                         // added
    if( (num_from_Py != 0) && (num_from_Py % 5 == 0)){ Serial.println("inside"); vibMotor(); }                                                      //added ; only vibrate on a non-zero multiple
    in_text[i] = 0;
    i = 0;
    lastChar = 0;
    return true;
  }
  else {
    mod5 = false;
    lastChar = newChar;
    if(lastChar == ','){ newChar = '\n';}
    in_text[i++] = newChar;
    return false;
  }
}




// --------------------------------------------------------------------------------
// Toggle BLE sleep state
// --------------------------------------------------------------------------------
void BLEConnect() {
  // Disconnect and put to sleep
  if (!asleep) {
    BTserial.print("OK+LOST");              // Just in case it doesn't get written before going to sleep
    delay(50);
    BTserial.print("AT");
    delay(150);
    BTserial.print("AT+ADTY3");
    delay(50);
    BTserial.print("AT+SLEEP");
    delay(50);
    asleep = true;
    confirmedCentral = false;
  }
  // Wake up and re-establish connection
  else {
    Serial.println("Waking up now");
    BTserial.print("AT+galliaestomnilliaestomnisdivisainpartestrfffesquarumunamincoluntbelgaealiamaquitanitersdivisainpartestrfffesquarumunamincoluntbelgaealiamaquitanitertiamquiipsorumlinguaceltaenostragalliappellanturtragalliappellant");
    delay(350);
    BTserial.print("AT+ADTY0");
    delay(50);
    BTserial.print("AT+RESET");
    delay(50);
    BTserial.flushInput();                      // Purge buffer
    asleep = false;
    value = 0;
    flag = false;
  }
}


// --------------------------------------------------------------------------------
// Initialize the IMU
// --------------------------------------------------------------------------------
void initIMU() {

  // Intialize the IMU and the DMP (Digital Motion Processor) on the IMU
  IMU.initialize();
  IMU.dmpInitialize();
  IMU.setDMPEnabled(true);

  // Initialize I2C communications
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(MPU_addr);               // PWR_MGMT_1 register
  Wire.write(0);                      // Set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);

  // Create an interrupt for pin2, which is connected to the INT pin of the MPU6050
  pinMode(interruptPin, INPUT);
  attachInterrupt(digitalPinToInterrupt(interruptPin), interruptPinISR, RISING);
}


// --------------------------------------------------------------------------------
// Read from the IMU
// Currently, this reads 3 acceleration axis, temperature and 3 gyro axis.
// You should edit this to read only the sensors you end up using.
// For this, you need to edit the number of registers being requested and possibly the addresses themselves
// --------------------------------------------------------------------------------
void readIMU() {
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B);                         // Starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);

  Wire.requestFrom(MPU_addr, 14, true);      // Request a total of 14 registers

  // Accelerometer (3 Axis)
  ax = Wire.read() << 8 | Wire.read();      // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)
  ay = Wire.read() << 8 | Wire.read();      // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  az = Wire.read() << 8 | Wire.read();      // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)

  // Temperature
  tp = Wire.read() << 8 | Wire.read();      // 0x41 (TEMP_OUT_H) & 0x42 (TEMP_OUT_L)

  // Gyroscope (3 Axis)
  gx = Wire.read() << 8 | Wire.read();      // 0x43 (GYRO_XOUT_H) & 0x44 (GYRO_XOUT_L)
  gy = Wire.read() << 8 | Wire.read();      // 0x45 (GYRO_YOUT_H) & 0x46 (GYRO_YOUT_L)
  gz = Wire.read() << 8 | Wire.read();      // 0x47 (GYRO_ZOUT_H) & 0x48 (GYRO_ZOUT_L)
}


void vibMotor(){
  // Short pulses
  digitalWrite(vib_mot, LOW);   // ON
  delay(200);               
  digitalWrite(vib_mot, HIGH);  // OFF
  delay(1000);
  digitalWrite(vib_mot, LOW);   // ON
  delay(200);               
  digitalWrite(vib_mot, HIGH);  // OFF
  delay(1000);  
}

// --------------------------------------------------------------------------------
// Setup: executed once at startup or reset
// --------------------------------------------------------------------------------
void setup() {
  // Initialize the OLED display
  initDisplay();
  showMessage("Initializing ...");
  delay(1000);

  // Initialize the IMU
  initIMU();

  // Initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT);
  // initialize the Motor pin as an output.
  pinMode(vib_mot, OUTPUT);
  //Set PULL-UP Resistor
  pinMode(buttonPin, INPUT_PULLUP);

  // Initialize Serial (needed for setting the mode of the BLE)
  Serial.begin(9600);

  // Initialize the BT Serial (AltSoftSerial)
  BTserial.begin(9600);
  Serial.println("BTserial started");

  // Clear the display
  showMessage(" ");
}


// --------------------------------------------------------------------------------
// Loop: main code; executed in an infinite loop
// --------------------------------------------------------------------------------
void loop() {
  
  digitalWrite(vib_mot, HIGH);  // OFF
  // Check if the button was pressed
  // If it was, establish or re-establish a BT connection
  if (checkButton())
    BLEConnect();

  // Check if Python is sending a message to the Arduino. Also checks for handshake.
  if (BTserial.available()) {
    // Read from the Bluetooth module and send to OLED, Serial
    if (receiveFromBLE()) {
      // If a new message was completed by receiving the ";" character, show it
      showMessage(in_text);
      Serial.println(in_text);
    }
  }

  // Read from the Serial Monitor and send to the Bluetooth module
  if (Serial.available())
    forwardSerialToBLE();

  // If we received a message from the computer, we know we are connected. Start sending data back
  if (confirmedCentral) {                              // This implicitly checks if BLE is asleep (confirmedCentral would be false if asleep==true)
    endTime = micros();
    if (endTime - startTime >= period_us) {
      time_interval += (float)(endTime - startTime);
      startTime = endTime;
      ir_value = analogRead(analogPin);
      Serial.println(ir_value);
      // If the IMU has data, as indicated by the interrupt
      if (imuDataReady) {
        // Read IMU data
        readIMU();
        imuDataReady = false;
        L1 = abs(ax) + abs(ay) + abs(az);
        dtostrf(startTime / 1e6, 6, 2, time_buf);
        dtostrf(ir_value, 6, 2, x_axis_buff);
        dtostrf(L1, 6, 2, IMU_val);       //passes x-axis imu
        sprintf(out_text, "%s, %s, %s;\n", time_buf, x_axis_buff, IMU_val);   // added the newline for phone connection output
        //Serial.println(ir_value);
        BTserial.print(out_text);
        //Serial.print(' ');
        //Serial.print(ax);
        //Serial.print(" ");
        //Serial.print(ay);
        //Serial.print(" ");
        //Serial.println(az);
      }

      /******************************************************************************************
         converting time into string
         using dtostrf(float variable, needed str length for storage (including decimal),
                      number decimals (integer), buffer name);
         using sprintf(buffer name, "string %d", variable_if_needed_for_%d);
       ******************************************************************************************/
      /*
              dtostrf(time_interval / 1e6, 5, 2, time_buf);               // Write the end time to the time data char array
              dtostrf(ax, 6, 0, x_axis_buff);                           // Write the IMU x axis data to the IMU data char array
              sprintf(out_text, "%s,%s;", time_buf, x_axis_buff);     // Combine char arrays and add coma, semicolon
              BTserial.print(out_text);
              // Serial.println(out_text);                         // Enable this for debugging
            }
      */
    }

  }
}

