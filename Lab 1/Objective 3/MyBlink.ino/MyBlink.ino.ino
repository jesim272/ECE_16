#include <AltSoftSerial.h>
AltSoftSerial BTserial;                    //Object to class AltSoftSerial
 
char c=' ';                               //Empty character
boolean NL = true;                        //Newline
 
void setup()
{
    Serial.begin(9600);                   //Set Baud rate to 9600
    while(!Serial){};                     //Do nothing if Serial is available
    BTserial.begin(9600);                 //Set baud rate for Bluetooth communication
    Serial.println("BTserial started");   //Print to serial monitor that the baud rate was set
}

void loop()
{
    // Read from the Bluetooth module and send to the Arduino Serial Monitor
    if (BTserial.available())
    {
            c = BTserial.read();                
            Serial.write(c);                    //sends to Arduino
    }
  
    // Read from the Serial Monitor and send to the Bluetooth module
    if (Serial.available())
    {
            c = Serial.read();
 
            // do not send line end characters to the HM-10
            if (c!=10 & c!=13 )
            {  
                 BTserial.write(c);             //Sends to Bluetooth module
            }
            
            // Copy the user input to the main window, as well as the Bluetooth module
            // If there is a new line print the ">" character.
            if (NL) {
              Serial.print("\r\n>");      //add newline in the monitor
              NL = false;
            }
            Serial.write(c);              
            if (c==10) {                  //set NL true if newline was entered at input
              NL = true;
            }
    }
}
