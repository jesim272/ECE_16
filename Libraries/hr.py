import numpy as np
from Libraries.ListBuffer import ListBuffer
from sklearn.mixture import GaussianMixture as GM
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.mlab as mlab
import statistics as stats


class Hr:

    #Initializes new instance of heart beat detector. 
    #calls train() to train the GMM with the training data
    #GMM param will be used by the hear rate calculation algorithm
    # Added window_length
    def __init__(self, train_file, window_length=100, plot=False):
        self.window_length = window_length
        self.plot = plot
        self.model = None
        self.train(train_file)
        self.hr = 0
        self.count = 0
        self.avg_hr = []
    def _normalize(self, data):
        return np.nan_to_num((data - np.nanmin(data)) / (np.nanmax(data) - np.nanmin(data)))

    #Accept a file path of the training data as an argument
    #Find the GMM parameter based on training data
    def train(self, train_file):
        """
        Loads the training data and learns the GMM. Optionally plots the results.
        :param train_file: filename for training file containing time and pre-processed ir data.
        :return: None
        """
        # Load training data. train_file must be in the same folder as the script implementing this class.
        train_t, train_ir = np.loadtxt(train_file, delimiter=",", skiprows=1, unpack=True)

        # Reshape training data to be a 2D array
        train_ir = train_ir.reshape(len(train_ir), 1)
        train_t = train_t.reshape(len(train_ir), 1)

        # Unit normalize
        train_ir = self._normalize(train_ir)

        # Create GMM object
        gmm = GM(n_components=2, means_init=np.array([[0.25], [0.85]]))     # mean guesses for normalized data
        #gmm = GM(n_components=2, means_init=np.array([[np.min(train_ir)], [np.max(train_ir)]]))

        # Find parameters for GMM based on training data
        self.model = gmm.fit(train_ir)
        if self.plot:
            histo = self.plot_histo(train_ir)
            histo.axes[0].set_title(f"Histogram for: {train_file}")
            labels = self.plot_labels(train_t, train_ir)
            labels.axes[0].set_title(f"Labels for: {train_file}")
        return 
    
    # Allow to plot data easily, similar to unsupervised_bdr.py
    # Time and data values as np array
    # Plot histogram of data and plot labels from GMM prediction 
    #   on that data
    
    def plot_histo(self, ir):
        # Create new figure
        f = plt.figure()
        # Retrieve Gaussian parameters
        mu0 = self.model.means_[0]
        mu1 = self.model.means_[1]
        std0 = np.sqrt(np.abs(self.model.covariances_[0][0][0]))
        std1 = np.sqrt(np.abs(self.model.covariances_[1][0][0]))
        w0 = self.model.weights_[0]
        w1 = self.model.weights_[1]
        # Create an "x" vector from which to compute normal distribution curves
        x = np.reshape((np.linspace(np.min(ir), np.max(ir), 1000)), [1000, 1])
        # Compute normal curves
        curve_0 = w0 * norm.pdf(x, loc=mu0, scale=std0)
        curve_1 = w1 * norm.pdf(x, loc=mu1, scale=std1)
        # Plot the histogram
        plt.hist(ir, bins=50, density=True)
        # Plot the curves
        plt.plot(x, curve_0 + curve_1, '-r')
        #.plot(x, curve_1, '-b')
        # Label the plots
        plt.xlabel("IR data")
        plt.ylabel("Count (#)")
        plt.title("IR Signal Histogram")
        plt.tight_layout()
        plt.show(block=False)
        
        
        return f
    
    
    def plot_labels(self, t, ir):
        # Create new figure
        f = plt.figure()
        # Calculate the labels
        labels = self.model.predict(ir)
        # Plot data and labels, scaling labels to max of data
        plt.plot(t, ir-0.5, 'b-')
        plt.plot(t, labels * np.max(ir), 'r-')
        # Label plot
        plt.ylabel('Voltage (V)')
        plt.xlabel('Time (s)')
        plt.title('GMM Labels')
        plt.show(block=False)
        return f
    
    #################   OBJECTIVE 3  #############################
    
    
    ## Process the IR data to get a heart rate estimate
    ## t_data: numpy array with timestamps
    ## ir_data: numpy array with IR data
    ## returns: heart rate hr estimate in bpm (returns None if not valid) and the time t_hr for that hr estimate

    def process(self, t_data, ir_data):
        """
        Passes new data first to the GM prediction method and then to other heuristics methods.
        :param t_data: iterable (list or 1D numpy array) containing time data.
        :param ir_data: iterable (list or 1D numpy array) containing ir data.
        :return: calculated heart rate, taking into account previously calculated heart rates, along with timestamp.
        """
        # NEW
        # Slice
        t = t_data[-self.window_length:]
        ir = ir_data[-self.window_length:]

        # Convert to numpy arrays, as required by sklearn.mixture.GaussianMixture
        t = np.array(t)
        ir = np.array(ir)

        # Unit normalize (this helps account for different amounts of pressure on the sensors)
        ir = self._normalize(ir)

        # Use GMM to label beats
        labels = self.model.predict(ir.reshape(len(ir), 1)).flatten()
        # Apply beat heuristics
        # You may want to wrap this in a try/except clause to avoid issues like 0 heartbeat giving a divide by zero error
        # Assign placeholders to return if processing fails.
        hr = self.hr
        t_hr = t_data[-1]
        try:
            t_hr, hr = self.hr_heuristics(t, labels)
        except:
            pass

        return t_hr, hr
        

    ## Process the label data to get a hr estimate
    ## t: numpy array with timestamps
    ## labels: numpy array with corresponding GMM labels of the data
    ## returns: heart rate hr estimate in bpm (returns None if not valid) and the time t_hr for that hr estimate
    
    #-------------------------------------------------------------------
    #------------------------------------------------------------------
    
    def hr_heuristics(self, t, labels):
        """
        Makes sure heart beats detected are well spaced and of normal duration.
        :param t: iterable (list or 1D numpy array) containing timestamps.
        :param labels: iterable (list or 1D numpy array) containing data labels (0/1).
        :return: heart rate extracted from timestamps and labels and timestamp at which it was calculated.
        """
        try:
            
            bpm = None
            #enter the loop when labels populates with 100 new elements
            if(len(labels) == 100 and (self.count % 25) == 0):
                #reset the counter which makes sure there are 100 new elements
                self.count = 0
                # Find where beats start and end
                beats_start = np.diff(labels) == 1
                beats_end = np.diff(labels) == -1
            
                beat_start_times = t[1:][beats_start]
                beat_end_times = t[1:][beats_end]
            
                # Remove beat ends at first time point or beat starts at last
                if beat_end_times[0] < beat_start_times[0]:
                    beat_end_times = beat_end_times[1:]
                if beat_start_times[-1] > beat_end_times[-1]:
                    beat_start_times = beat_start_times[0:-1]
                        
                # Calculate the interval between beats
                between_beats = beat_start_times[1:] - beat_end_times[:-1]
                beat_avg = np.average(1/between_beats)
                
                # Convert the intervals between beats to a heart rate, in bpm
                bpm_estimated = beat_avg * 60
                # Make sure the calculated heart rate is physiological and that all heuristics tests passed
                if 25 < bpm_estimated < 260:
                    #append the array with the heart rate estimated for the 100 samples
                    self.avg_hr = np.append(self.avg_hr, bpm_estimated)
                    #print("avvg array:", end = ' ')
                    #print(self.avg_hr)
                    #set the heart rate to that which was estimated
                    self.hr = int(stats.mean(self.avg_hr))
                    #print("total average: ", end = ' ')
                    #print(int(self.hr))
                    #If avg_hr is populated with 50 hr beats, take the average of those
                    if(len(self.avg_hr) == 50):
                        self.avg_hr = []    #clear buffer
                    else:
                        #if self.avg_hr does not have 50 hr beats, just return previous calculation 
                        self.hr = int(self.hr)
                else:
                    self.hr = int(self.hr)
                # Find the timestamp
                t_hr = np.average(t)
                return t_hr, int(self.hr)
            else: 
                #If labels does not have 100 elements inctrement count and send previous data
                self.count +=1
                t_hr = np.average(t)
                return t_hr, int(self.hr)
        except ValueError:
            return t_hr, int(self.hr)