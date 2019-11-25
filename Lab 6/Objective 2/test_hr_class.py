from Libraries.HR_basic import Hr
import matplotlib.pyplot as plt
import numpy as np
if (__name__ == "__main__"):
    
    #Create an object (instance) of class HR
    hr = Hr(train_file = "C:\\Users\\Jesi\\Desktop\\ECE_16\\Lab 6\\Objective 1\\ir_data_train.csv", plot = False)
    #create the data_time_va and data_ir_va/ reshape them / normalize/ creat GMM object
    
    #stored the entire data set for time and ir values
    d_t, d_ir = hr.train("C:\\Users\\Jesi\\Desktop\\ECE_16\\Lab 6\\Objective 1\\ir_data_train.csv")
    
    #ploting to check
    #hr.plot_histo(d_ir[0:np.size(d_ir)].reshape(-1,1))
    #hr.plot_labels(d_t[0:np.size(d_t)].reshape(-1,1), d_ir[0:np.size(d_ir)].reshape(-1,1))

    ##--------------------- process 5 seconds -------------------------------------------------
    #a,b are intializers to the arrray start and endpoints (determine to cover 5 sec of data)
    a, b = 0, 99
    t1, ir = [ ], [ ]
    #iterateing throught 5 seconds of data and storing in array
    for i in range(0,int(np.size(d_t)/100)):
        #stores 5 blocks of data into t_hr1 and hr1 (single value)
        t_hr1, hr1 = hr.process(d_t[a:b], d_ir[a:b])
        ##reshaping the data to plot
        d_t = d_t.reshape(-1,1)
        d_ir = d_ir.reshape(-1,1)   
        #storing time into an np array
        t1 = np.append(t1, d_t)
        #storing ir value into an np array
        ir = np.append(ir, d_ir)
        a += 100
        b += 100
    
    #processed the remaining data set
    t_hr1, hr1 = hr.process(d_t[a:np.size(d_t)], d_ir[a:np.size(d_ir)])
    #store the remaining data into the array
    t1 = np.append(t1, t_hr1)
    ir = np.append(ir, hr1)
    
    #plot the entire data set that was processed
    hr.plot_histo(d_ir[0:np.size(t1)].reshape(-1,1))
    hr.plot_labels(d_t[0:np.size(t1)].reshape(-1,1), d_ir[0:np.size(ir)].reshape(-1,1))
 
    
    #--------------------testing validation set ---------------------
    d_t, d_ir = hr.train("C:\\Users\\Jesi\\Desktop\\ECE_16\\Lab 6\\Objective 1\\ir_data_validation.csv")
    
    a, b = 0, 99
    t1, ir = [ ], [ ]
    #iterateing throught 5 seconds of data and storing in array
    for i in range(0,int(np.size(d_t)/100)):
        #stores 5 blocks of data into t_hr1 and hr1 (single value)
        t_hr1, hr1 = hr.process(d_t[a:b], d_ir[a:b])
        ##reshaping the data to plot
        d_t = d_t.reshape(-1,1)
        d_ir = d_ir.reshape(-1,1)   
        #storing time into an np array
        t1 = np.append(t1, d_t)
        #storing ir value into an np array
        ir = np.append(ir, d_ir)
        a += 100
        b += 100
    
    #processed the remaining data set
    t_hr1, hr1 = hr.process(d_t[a:np.size(d_t)], d_ir[a:np.size(d_ir)])
    #store the remaining data into the array
    t1 = np.append(t1, t_hr1)
    ir = np.append(ir, hr1)
    
    #plot the entire data set that was processed
    hr.plot_histo(d_ir[0:np.size(t1)].reshape(-1,1))
    hr.plot_labels(d_t[0:np.size(t1)].reshape(-1,1), d_ir[0:np.size(ir)].reshape(-1,1))

    