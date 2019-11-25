"""
Send commands to the BLE module
"""

# Import custom libraries
from Libraries.Bt import Bt                                 ##changed "from Bt_basic_handshake import Bt"
                                                                  ##to from Libraries.Bt import Bt


# Set peripheral MAC as well as HM-10 serial port
ble_peripheral_MAC = "D8A98BB5847E"                 # Use the MAC address of your peripheral HM-10
serial_port = 'COM5'                                #Changed from COM3                  


# Initialization of BLE
def initialize_ble():
    global bt
    bt = Bt(ble_peripheral_MAC=ble_peripheral_MAC, serial_port=serial_port)
    bt.ble_setup()


# -----------------------------------------------------------------------------------------
# This is where the main code starts
#------------------------------------------------------------------------------------------
try:
    # Take care of some initializations
    initialize_ble()
    
    # Monitor for any text received over BLE
    count = 0
    while True:
        response = bt.ble_read_line(";")                   #reads until ';'  
                                                          #changed from bt.ble_read() to bt.ble_read_buffer();
                                                          #changed to bt.ble_read_line(';');
        if response:                                      # response does not contain ';' character             
            print(response)                               # printing format ex: 2.00, 1432  (notice no ; at end)   ##***test using ',' in loop***
            if (response == '*'):
                bt.ble_write("Number: " + str(count))
                print("Sent: " + str(count))
                count = count + 1
            
                   
    # Close the BLE connection
    bt.ble_close()                     

    
# Catch the user pressing Ctlr+C or when an error occurs                      
except (KeyboardInterrupt, Exception):
    bt.ble_close()                      # Try to close the BLE connection cleanly (may fail)