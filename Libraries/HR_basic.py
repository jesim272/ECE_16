import numpy as np
from Libraries.ListBuffer import ListBuffer
from sklearn.mixture import GaussianMixture as GM
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.mlab as mlab



class Hr:

    #Initializes new instance of heart beat detector. 
    #calls train() to train the GMM with the training data
    #GMM param will be used by the hear rate calculation algorithm
    def __init__(self, train_file, plot=False):
        self.plot = plot
        self.model = None
        self.train(train_file)
        
    def _normalize(self, data):
        return np.nan_to_num((data - np.nanmin(data)) / (np.nanmax(data) - np.nanmin(data)))

    #Accept a file path of the training data as an argument
    #Find the GMM parameter based on training data
    def train(self, train_file):
        # Load training data. train_file must be in the same folder as the script implementing this class.
        train_t, train_ir = np.loadtxt(train_file, delimiter=",", skiprows=1, unpack=True)
        # Reshape training data to be a 2D array
        train_ir = np.array(train_ir).reshape(-1,1)
        train_t = np.array(train_t).reshape(-1,1)
        # Unit normalize
        train_ir = self._normalize(train_ir)
        # Create GMM object
        means_init = [[np.min(train_ir)], [np.max(train_ir)]]
        gmm = GM(n_components=2, means_init= means_init)
        # Find parameters for GMM based on training data
        self.model = gmm.fit(train_ir)
        if self.plot:
            #Call process(self, t_data, ir_data)
            #self.process(t_data = train_t, ir_data = train_ir)
            #Call to functions with param
            self.plot_histo(ir = train_ir)
            self.plot_labels(t = train_t, ir = train_ir )
        return train_t, train_ir
    
    # Allow to plot data easily, similar to unsupervised_bdr.py
    # Time and data values as np array
    # Plot histogram of data and plot labels from GMM prediction 
    #   on that data
    
    def plot_histo(self, ir):
        # Retrieve Gaussian parameters
        mu0 = self.model.means_[0]
        mu1 = self.model.means_[1]
        sig0 = np.sqrt(self.model.covariances_[0])
        sig1 = np.sqrt(self.model.covariances_[1])
        w0 = self.model.weights_[0]
        w1 = self.model.weights_[1]
    #   # Create an "x" vector from which to compute normal distribution curves
        x = np.reshape((np.linspace(np.min(ir), np.max(ir), 1000)), [1000, 1])
    #   # Compute normal curves
        curve1 = w0*mlab.normpdf(x,mu0, sig0)
        curve2 = w1*mlab.normpdf(x,mu1,sig1)
    #   # Plot histograms and sum of curves
        plt.hist(ir, bins=50, density=True)
        plt.xlabel("IR reading")
        plt.ylabel("Count (#)")
        plt.title("IR Signal Histogram (Gaussian sum)")
        plt.plot(x, curve1 + curve2, 'r')
        plt.show(block=False)
    #
    def plot_labels(self, t, ir):
        labels = self.model.predict(ir)
    #    # Plot t, ir and labels
        plt.plot(t, labels, 'g')
        plt.plot(t, ir-0.2, 'b')
        plt.xlabel("IR reading")
        plt.ylabel("Count (#)")
        plt.title("IR Signal ")
        plt.show(block=False)
    #
    
    
    #################   OBJECTIVE 3  #############################
    
    
    ## Process the IR data to get a heart rate estimate
    ## t_data: numpy array with timestamps
    ## ir_data: numpy array with IR data
    ## returns: heart rate hr estimate in bpm (returns None if not valid) and the time t_hr for that hr estimate

    def process(self, t_data, ir_data):
        # Reshape and normalize your data
        t_data = t_data.reshape(-1,1)
        ir_data = ir_data.reshape(-1,1)
        # Unit normalize
        ir_data = self._normalize(ir_data)
        # Use GMM to label beats
        labels = self.model.predict(ir_data)
    #   # Apply beat heuristics
    #   # You may want to wrap this in a try/except clause to avoid issues like 0 heartbeat giving a divide by zero error
        try:
            t_hr, hr = self.hr_heuristics(t_data, labels)
            return t_hr, hr
        except ValueError:
            return None
            
    #
    ## Process the label data to get a hr estimate
    ## t: numpy array with timestamps
    ## labels: numpy array with corresponding GMM labels of the data
    ## returns: heart rate hr estimate in bpm (returns None if not valid) and the time t_hr for that hr estimate
    
    #-------------------------------------------------------------------
    #------------------------------------------------------------------
    
    def hr_heuristics(self, t, labels):
        
        try:
            #calculate and store values that have only 1's
            differen = t[1:][np.diff(labels) == 1]
            #prints the differences of time
            #print(np.diff(differen, axis = 0))
            #prints the average time
            time_avg = np.average(np.diff(differen, axis = 0))
            hr = 60 / time_avg
            t_hr = np.average(t)
            return t_hr, hr
        except ValueError:
            return None