# ---------------------------------------- Import Libraries ---------------------------------------- #
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as sig
from sklearn.mixture import GaussianMixture as GM
import matplotlib.mlab as mlab
# ---------- Import Your Modules HERE ---------- #


if (__name__ == "__main__"):
    
    ##########
    # Step 1 #
    ##########
    # ---------- Load training data ---------- #
    # Load training data
    #Using 2 for skiprows because my first value is really off
    data_time_tr, data_ir_tr = np.loadtxt("C:\\Users\\Jesi\\Desktop\\ECE_16\\Lab 6\\Objective 1\\ir_data_train.csv", delimiter=",", skiprows=2, unpack=True)
    ##########
    # Step 2 #
    ##########
    # ---------- Plot 5 sec of Raw Data ---------- #
    plt.figure()
    #data_time[:100 ], data_ir_tr[:100]
    ti = []
    element = 1
    for i in data_time_tr:
        t_interval = i - data_time_tr[1]
        if (t_interval <= 5) and (t_interval >= 0):
            element += 1
            ti.append(i) 
        if(t_interval > 5):
            break
    y_ir = data_ir_tr[1: element]
    plt.xlabel("Time")
    plt.ylabel("IR Signal")
    plt.title("IR Raw Signal (5 sec)")
    plt.plot(ti,y_ir)
    # PLOT HERE
    plt.show()

    
    ##########
    # Step 3 #
    ##########
    # ---------- Plot Histogram ---------- #
    # Plot the histogram of your training dataset, here.
    plt.figure()
    plt.hist(data_ir_tr, 50)
    plt.xlabel("IR reading (training data)")
    plt.ylabel("Count (#)")
    plt.title("IR Signal Histogram")
    

    ##########
    # Step 4 #
    ##########
    # ---------- Find GMM ---------- #
    # Create GMM object
    means_init = [[np.min(data_ir_tr)], [np.max(data_ir_tr)]]
    gmm = GM(n_components=2, means_init= means_init)
    # Fit 2 component Gaussian to the data
    #changed param
    X = data_ir_tr.reshape(-1,1)   #Create a 2D - array   
    gmm_fit = gmm.fit(X)                                # Pass correct parameters. Remember that this expects a 2D array.
    # Retrieve Gaussian parameters
    mu0 = gmm_fit.means_[0]
    mu1 = gmm_fit.means_[1]
    sig0 = np.sqrt(gmm_fit.covariances_[0])
    sig1 = np.sqrt(gmm_fit.covariances_[1])
    w0 = gmm_fit.weights_[0]
    w1 = gmm_fit.weights_[1]

    # ---------- Plot Gaussians sum over histogram ---------- #
    # Create an "x" array from which to compute the Gaussians
    #changed param
    x = np.reshape((np.linspace(np.min(data_ir_tr), np.max(data_ir_tr), 1000)), [1000, 1])
    
    plt.figure()
    plt.hist(data_ir_tr, bins=50, density=True)
    plt.xlabel("IR reading")
    plt.ylabel("Count (#)")
    plt.title("IR Signal Histogram (Gaussian sum)")
    plt.plot(x, w0 * mlab.normpdf(x, mu0, sig0) + w1 * mlab.normpdf(x, mu1, sig1))
    plt.show() 
    
    # ---------- Plot two Gaussians over histogram ---------- #
    # Add the appropriate code
    plt.figure()
    plt.hist(data_ir_tr, bins=50, density=True)
    plt.xlabel("IR reading")
    plt.ylabel("Count (#)")
    plt.title("IR Signal Histogram (Gaussian Individual)")
    plt.plot(x, w0 * mlab.normpdf(x, mu0, sig0))
    plt.plot(x, w1 * mlab.normpdf(x, mu1, sig1))
    plt.show()

    
    ##########
    # Step 5 #
    ##########
    # ---------- Load validation data ---------- #
    # Load validation data
    data_time_va, data_ir_va = np.loadtxt("C:\\Users\\Jesi\\Desktop\\ECE_16\\Lab 6\\Objective 1\\ir_data_validation.csv", delimiter=",", skiprows=1, unpack=True)
    Y = data_ir_va.reshape(-1, 1)   #Create a 2D - array 
    # ---------- Predict Labels for training data ---------- #
    # Predict training labels
    train_pred_lbl = gmm_fit.predict(X)                     # Pass correct parameters
    # ---------- Predict Labels for validation data ---------- #
    # Predict validation labels
    validation_pred_lbl = gmm_fit.predict(Y)                # Pass correct parameters
    # ---------- Plot Training Set predictions ---------- #
    plt.figure()
    
    #changed param
    plt.plot(data_time_tr,1.1*train_pred_lbl, 'g')
    plt.plot(data_time_tr, data_ir_tr/15, 'b')
    plt.xlabel("IR reading")
    plt.ylabel("Count (#)")
    plt.title("Training Set Predication (class label)")
    
    plt.show()
    
    # ---------- Plot Validation Set predictions ---------- #
    plt.figure()
    plt.plot(data_time_va, validation_pred_lbl*1.1, 'g')
    plt.plot(data_time_va, data_ir_va/15, 'b')
    plt.xlabel("IR reading")
    plt.ylabel("Count (#)")
    plt.title("Validation Set Predication (class label)")
    plt.show()