"""
Send commands to the BLE module
"""

import serial
from time import sleep

serial_port = "COM3"             # You need to put the correct port


# Read from serial ser and return the string that was read
def read_BLE(ser):
  msg = ''
  # need to decode
  while ser.in_waiting:                             #while there are bytes
      msg = msg + ser.read(1).decode('utf-8')       #concatenate until no bytes
  return msg                  #return entire message that was decoded


# Write the string, command, to serial ser; return nothing
def write_BLE(command, ser):
  ser.write(command.encode('utf-8'))            #encode string and send to BLE
  return


# Open the serial port and when successful, execute the code that follows
with serial.Serial(port=serial_port, baudrate=9600, timeout=1) as ser:
            
            command =  "AT+NAMEjesiBLE2" #input("Enter command: ")
            # Set the name of the HM-10 module
            # Print the response from the BLE module
            write_BLE(command, ser)                #setting name
            sleep(0.5)                        #add a delay using the sleep function
            # Ask for the name from the HM-10 module
            # Print the response from the BLE module
            print(read_BLE(ser))      #reading the name set
            
            command = "AT+NAME?"
            write_BLE(command, ser)
            sleep(0.5)
            print(read_BLE(ser))