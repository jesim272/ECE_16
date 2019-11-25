Jesi Miranda-Santos (Primary)   A14989720  
Diego Ramos (Secondary)   A14935625

# Lab 6
#
## Introduction
#
 This lab focuses on machine learning, and the main goal was for us to use machine learning in order to "teach" the program how to determine whether a signal spike in the (filtered) heartbeat data is actually a heartbeat or not (like random noise). We approach this by applying unsupervised machine learning and implementing statistical and mathematical methods like Gaussian Matrix Models in order to give the program/computer heuristic characteristics in order to achieve the goal of identifying a heartbeat without user assistance/input.

#
### Objective 1
#

1. The goal of this objective was to create an unsupervised machine learning algorithm that filtered our data from a csv file. Additionally, we classified each datapoint as being part of a heartbeat or not. It was not a robust algorithm nor a robust method; however, this is the start.

2. We first started by utilizing last weeks lab to gather 30 to 45 seconds of heartbeat data and store it in a csv file; we then split 
70% of it into a "train" file and the rest into a "validation" file, both in csv, which we will need to both teach the program how to 
identify and label a heartbeat and when we verifying that the alogrithm is performing how it is supposed to perform.

*Step 1*:
  Here we import the "ir_data_train.csv" file and split the time and ir columns into two arrays: data_time_tr and data_ir_tr
 
 
*Step 2*:
  Step 2 is fairly easy since we are just plotting the first 5 seconds of our "ir_data_train data," but we are plotting it using 
  data_time_tr and data_ir_tr as the x and y axes, respectively.
  
  ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%206/Images/Objective%201/IRdata.PNG "IRdata.PNG")
  
*Step 3*:
  Step 3 was about getting our IR data and making a historgram of 50 bins from that data and plotting it.
  Of course we expected multiple classes, since we were tasked to make a histogram of 50 bins (bins and classes mean the same, according
  to various websites), but we also expect multiple classes to have different values. This is because it is not an even distribution of 
  ir values, i.e. the peaks in the heartbeats will occur less often than other ir values.


*Step 4*:
  In this step we are creating two Gaussians using the ir training data, and from those two make a Gaussian Mixture Model. 
  We plot each Gaussians' historgram and we plot both historgrams combined. We had to reshape the training data since it we needed a
  1D np array to be able to use the data in the GaussianMixture class


*Step 5*:
  Step 5 has us implement the predict() function in order to figure out the labels for which will indicate whether a heart beat is
  detected or not; we will do this utilizing both the train data and the validation data. We will then plot each individual set of data,
  with the labels, which will show the peaks that are heart beats.

   ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%206/Images/Objective%201/hist_individual.PNG "hist_individual.PNG")
    
   ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%206/Images/Objective%201/hist_sum.PNG "hist_sum.PNG")
    
   ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%206/Images/Objective%201/labeled_tr.PNG "labeled_tr.PNG")
    
   ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%206/Images/Objective%201/labeled_val.PNG "labeled_val.PNG")
    
#
### Objective 2
#
1. The goal of this objective was to build off from Objective 1 and create class; hence, we are just packaging the basic ML heartbeat detector. Addtionally, we are plotting the filtered signals along with some labeles that indicate whic hare heartbeats and which are not.

2. In this objective we are given most of the code for the class "HR_basic," and utilizing objective 1's code we will modify and 
complete the class in order to be able to determine anytime, and in any other related program, the heart beat

We test this new class by opening a new file, "test_hr_class," and we test both the training and the validation data and plot the results,
both histogram and labels.
The GMM does classify the data but it is not really accurate; utilizing the training data does work properly.
  
  ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%206/Images/Objectiev%202/class_test_hist.png "class_test_hist.PNG")
  
  ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%206/Images/Objectiev%202/class_test_labels.PNG "class_test_labels.PNG")
  
  
  
#
### Objective 3
#
  1.  The goal of this objective was to refine the algorithm from Objective 2, which means that we implemented two more functions that got somewhat rid of noise and gave use a more refined signal of a heart beat. We did not add too many changes to the code in Objective 2 but we did end up adding some code in the test_hr_class.py. More specifically, we added code such that we only processed 5 seconds of data.
  
  2. This objective builds upon the previous objective's Hr_basic class and the test_hr_class and asks us to add two new functions called "process()"
and "hr_heuretics()" in order to have the program better estimate and adapt to what a heart beat should look like, regardless of the data
that is inputted. Basically dealing with the error we got in objective 2 when attempting to plot the validation data and its labels.

We then test the final code, again in the test_hr_class, by updating the code with the process() function.

Based on initial observations, the program does work way better than objective 2's code, but it isnt perfect. Which, according to the lab
requires tweaking.

 ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%206/Images/Objective%203/process_tr_test.PNG "process_tr_test.PNG")
 
  ![Images](https://github.com/UCSD-Product-Engineering/ece16-sp19-jesim272/blob/master/ECE_16/Lab%206/Images/Objective%203/process_va_test.PNG "process_va_test.PNG")
  
  
  
  
  
#
### Final Notes
#
 
 Diego:
  This lab was one of my least favorites, mainly because I am not the most fond of programming, I would consider myself more of a hardware, hands-in person, and having to extensively pogram a computer to identify heartbeats was a really painful task. Luckily, my partner is good at programming and really helped out, along with other peers we worked with, and we were able to complete the lab.
As expected, we constantly kept encountering problems with the program, mainly trying to figure out why the plots were not plotting and
why did some data seemed incorrect, like reading the heartbeats from the IR sensor would sometimes give inaccurate signals because we moved our hand/finger while measuring the IR readings. It mostly felt like the lab was about debugging, which is an obvious unavoidable part of programming, but it still seemed to prove a bit more difficult than anticipated, which left us-- my partner, peers and me-- to come together and figure out the lab.


Jesi:
 I personally did not enjoy this part of the laab because it was a lot of debugging and very very very time consuming. Also the instructions where somewhat confusing. I spent too much time researching the functions used and too much time trying to figure out how to properly out the signal. My heartbeat was at a pretty consistent pace at the beginning but after need to resample and obatin new data, my heart beat was pretty slow. This decrease in heart rate was due to the lab, I kind of died a little.
