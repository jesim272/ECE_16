from sklearn.neighbors import KNeighborsClassifier as KNN
import numpy as np
from Libraries.ListBuffer import ListBuffer
import statistics as stat

class Pedometer:

    # initial_steps is useful if you ever have to restart the pedometer
    def __init__(self, train_file_active, train_file_inactive, window_length=100, initial_steps=0):
        self.window_length = window_length
        self.steps = initial_steps
        self.knn = self.train(train_file_active, train_file_inactive)

        
    def extract_features(self, t, imu):
        # Split into 10 chunks
        c = []
        res1 = []
        imu = np.array_split(imu, 10)
        #(10,10)
        for a in range(0,10):
            for b in range(0,10):
                c = np.append(c, np.max(imu[a][b]))
            res1 = np.append(res1, np.max(c))
            
        # Get the maxima of each chunk. The list comprehension is equivalent to a for-loop but cleaner!
        # Return the average of these maxima
        result = stat.mean(res1)
        print(result)
        return result

    
    def train(self, train_file_active, train_file_inactive):
        """
        ---------------------- DATA LOADING ----------------------
        """
        # Load the data into numpy arrays. The data must only have two columns. Skip the labels row.
        t_active1, ir_tr, data_active1 = np.loadtxt(train_file_active, delimiter=",", skiprows=1, unpack=True)
        t_inactive2,ir_va, data_inactive2 = np.loadtxt(train_file_inactive, delimiter=",", skiprows=1, unpack=True)
        
        # For both the active data and the inactive data, split it into windows of size window_length
        # Let's assume there are "num_window" windows
        
        data_active = np.array_split(data_active1,self.window_length)
        data_inactive = np.array_split(data_inactive2,self.window_length)
        
        # Extract features for each of these windows for both the active and active set
        # Do this by calling self.extra_features()
        # The result will be an array of num_window features for the active set, and a similar array for the inactive set
        
        data_active = self.extract_features(t_active1, data_active)
        data_inactive = self.extract_features(t_inactive2, data_inactive)
        
        # For both the active and the inactive set, split the features 50/50 into a training set and a validation set
        # The result will be an array of num_window//2 features for the active training set,
        # num_window//2 features for the active validation set, and something similar for the inactive set
        
        #slits data 50/50 if odd number of elements remove the last one to make even
        if(len(data_active1) % 2 != 0):
            data_active_tr = data_active1[:(int((len(data_active1))/2))]
            data_active_val = data_active1[(int((len(data_active1))/2)):len(data_active1)-1]
        else:
            data_active_tr = data_active1[:(int((len(data_active1))/2))]
            data_active_val = data_active1[(int((len(data_active1))/2)):]
            
        if(len(data_inactive2) % 2 != 0):
            data_inactive_tr = data_inactive2[:(int((len(data_inactive2))/2))]
            data_inactive_val = data_inactive2[(int((len(data_inactive2))/2)):len(data_inactive2)-1]
        else:
            data_inactive_tr = data_inactive2[:(int((len(data_inactive2))/2))]
            data_inactive_val = data_inactive2[(int((len(data_inactive2))/2)):]   
        """
        ---------------------- TRAINING ----------------------
        """

        # Create training data
        # (1) Merge your array of features for the active training set and the inactive training set into one array.
        #     Reshape to a 2D array (of many rows and 1 column). Let's call this array X.
        X = np.append(data_active_tr, data_inactive_tr).reshape(-1,1)
        # (2) Create the correct labels for these features in a separate array Y. It will have the same dimensions as X.
        #     When the data came from the actve set, the corresponding label should 0. When it came from the inactive set, the
        #     corresponding label should be 1.
        Y = list(np.append((np.zeros(len(data_active_tr), dtype = int)), (np.ones(len(data_inactive_tr), dtype = int))))
        # Instantiate KNN
        knn = KNN(n_neighbors = 3)

        # Train the KNN with X and Y
        knn.fit(X,Y)

        """
        ---------------------- VALIDATION ----------------------
        """

        # Create the validation data in a similar way as was done with the training data.
        # This will result in an array X_val and Y_val, with the data and labels respectively.
        X_val = np.append(data_active_val, data_inactive_val).reshape(-1,1)
        Y_val = np.array(np.append((np.zeros(len(data_active_val), dtype = int)), (np.ones(len(data_inactive_val), dtype = int))))
        # Run KNN to predict the labels for validation data
        Y_predicted = knn.predict(X_val)
        # Find the accuracy by comparing Y_val with Y_predicted
        accuracy = (Y_predicted == Y_val).mean()
        # Print the accuracy to the terminal
        print(accuracy)
        # Return he KNN parameters
        return knn

            
# def process(self, t_data, imu_data):
#
#     # Return if we don't have enough data yet or were not given enough data
#     if len(t) < self.window_length:
#         return self.steps
#            
#     # Slice into just one window
#     t = t_data[-self.window_length:]
#     imu = imu_data[-self.window_length:]
#
#     # Use the KNN to determine if the instantaneous state is active or inactive
#     # call self.is_active(...)
#
#     # Implement your own step counter heuristic
#     # You can create new functions if you want
#
#     return self.steps
#
# def is_active(self, t, imu):
#
#     # Extract features for KNN
#     # call self.extract_features(...)
#            
#     # Classify using KNN
#            
#     # Return the result (labels) of the classification
#     return result
#
