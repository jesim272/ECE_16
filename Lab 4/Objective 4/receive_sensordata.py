"""
Example of live plotting
"""

# Import custom libraries
from Libraries.ListBuffer import ListBuffer
from Libraries.AnimatedFigure import AnimatedFigure
from Libraries.Bt import Bt      

# Import time library
from time import time

current_time = 0                # Current time
current_new_time = 0
start_time = 0                  # Start time
x_val  = 0

ble_peripheral_MAC = "D8A98BB5847E"                 # Use the MAC address of your peripheral HM-10
                                                    #D8A98BB5847E
serial_port = 'COM5'                                #Changed from COM3
 
# Should we plot our data or not
live_plot = True
# Should we write to file or not
write_flag = False
#Should we read from file or not
read_flag = False

# Initialize buffers
def initialize_buffers():
    
    # Set shared variables to global so we can modify them
    global data_buffer

    # Create empty buffers to store data
    buffer_length = 50 * 30         # Initial estimate for 30 sec of data at 50Hz, that's probably way too long!
    data_buffer = [[]] * 2          # Two sets of data: time and sensor data
    data_buffer[0] = ListBuffer([], maxlen=buffer_length)       # time data
    data_buffer[1] = ListBuffer([], maxlen=buffer_length)       # sensor data

# Initialization of BLE
def initialize_ble():
    global bt
    bt = Bt(ble_peripheral_MAC=ble_peripheral_MAC, serial_port=serial_port)
    bt.ble_setup()

# This is just an example function
# You will want to replace this with the proper function to get data, e.g., from BLE 
def get_data():
    
    global current_new_time, x_val, current_time, start_time, f, read_flag
    data = None
    data = [current_new_time, x_val]
    if(write_flag):
        f.write(str(data[0]) + ',\n')
        f.write(str(data[1]) + '\n')
        return data
    
    elif(read_flag):
        current_time = time()
        if current_time - start_time > 2:
            start_time = current_time
            current_new_time = float((f.readline()).replace(',', ' '))
            x_val = float(f.readline())
            if not (current_new_time or x_val):
                read_flag = False
                f.close()
                return
            print(data[0])
            print(data[1])
            return data
        
    else:
        current_new_time = float(bt.ble_read_line(","))
        x_val = float(bt.ble_read_line(";"))
        data = [current_new_time, x_val] 
        return data          
    
# The main data processing function
# It is called repeatedly
def update_data():
    global data_buffer

    data = None
    while not data:                                 # Keep looping until valid data is captured
        data = get_data()                                                 

    # Add this new data to circular data buffers
    data_buffer[0].add(data[0])                   # time data
    data_buffer[1].add(data[1])                   # sensor data
    return [(data_buffer[0], data_buffer[1])]
    # This format [(x1, y1), (x2, y2), (x3, y3)] is expected by the animation module


"""
This is where the main code starts
"""
try:
    # Take care of some initializations
    initialize_buffers()
    # Take care of some initializations
    initialize_ble()
    
    # Monitor for any text received over BLE
    count = 0
    if(write_flag): f = open("data_write.csv", "w")
    if(read_flag): f = open("data_write.csv", "r")
    # If we are plotting our data
    # Call the animation with our update_data() function
    # This will call our function repeatedly and plot the results
    if live_plot:
        # Create animation object
        # Plot about 1/5 of the data in the buffer
        an = AnimatedFigure(update_data, plot_samples=200, debug=True)
        axes = an.axes
        axes[0].set_title('Data')
        axes[0].set_xlabel('Time (s)')
        axes[0].set_ylabel('IMU X-Axis')
        
        an.animate()            # Only call this after configuring your figure

    # If we don't want to plot at the same time, call the update_data() function repeatedly
    else:
        while True:
            update_data()
            
# Catch the user pressing Ctlr+C            
except (Exception, KeyboardInterrupt) as e:
    #f.close()
    print(e)
    bt.ble_close()                      # Try to close the BLE connection cleanly (may fail)