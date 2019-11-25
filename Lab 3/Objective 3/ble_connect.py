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

            command =  "AT"
            # Print the response from the BLE module
            write_BLE(command, ser)
            sleep(0.05)               #add a delay using the sleep function
                                        # Print the response from the BLE module
            print(read_BLE(ser))

            command = "AT+IMME1"
            write_BLE(command, ser)
            sleep(0.1)
            print(read_BLE(ser))

            command = "AT+IMME?"
            write_BLE(command, ser)
            sleep(0.1)
            print(read_BLE(ser))

            command = "AT+NOTI1"   #turns on notification
            write_BLE(command, ser)
            sleep(0.1)
            print(read_BLE(ser))

            command = "AT+NOTI?"
            write_BLE(command,ser)
            sleep(0.1)
            print(read_BLE(ser))

            sleep(0.1)
            command = "AT+ROLE1"
            write_BLE(command, ser)
            sleep(0.1)
            print(read_BLE(ser))

            sleep(0.1)
            command = "AT+ROLE?"
            write_BLE(command, ser)
            sleep(0.1)
            print(read_BLE(ser))

            command = "AT+ADDR?"
            write_BLE(command, ser)
            sleep(0.1)
            print(read_BLE(ser))

            response = ""
            con_established = "OK+CONNAOK+CONN"
            
            i = 0
            itera = 0
            #Enters while loop until connected
            while True:
                command = "AT+COND8A98BB5847E"
                write_BLE(command, ser)
                itera += 1
                sleep(0.4)
                response = read_BLE(ser)
                print(response)
                if((con_established in response) and (itera >=4)):
                    break
                
            while True:         
               write_BLE("Connected", ser)
               sleep(0.5)
               #once connected keep reading from BLE
               while (read_BLE(ser) in "*"):
                   i += 1
                   write_BLE("Number: ", ser)
                   print("Number: ", end = ' ')
                   print(i)
                   sleep(0.1)
