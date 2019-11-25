import numpy as np

a = [1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1]
a = list(a)
## there are 8 steps
print(a)
count = 0
step = []
for x in range(0,len(a)):
    if(a[x] != 0):
        count += 1
    if(a[x] == 0):
        if (count >= 2 and count <= 7):
            step = np.append(step, count)
        count = 0
            
print("There are this many steps: ", end = ' ')
print(len(step))
x =  "HR: " + str(len(a)) + "," + "Steps: " + str(len(step)) + ';'
print(x)
print(len(x))
print(x[len(x)-2 : len(x)-1])
    #detect a one and start from there
    #if array of 4 all ones
    #   increment by 4
    #elif array of 6 all ones
    #   increment by 6
    
    