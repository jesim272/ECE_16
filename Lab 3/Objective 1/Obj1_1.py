AT_com =["AT", "AT+IMME1", "AT+NOTI1", "AT+ROLE1"]

for command in AT_com:
    print(command)
    
O_com = [ "CONNECTION FAILURE", "BANANAS", "CONNECTION SUCCESS", "APPLES"]

text = "SUCCESS"


##the first two lines compares character by character
print("SUCCESS" in "SUCCESS")  #prints true
print("SUCCESS" in "ijoisafjiojiojSUCCESS")   #prints true

#These two lines compares the strings themselves not the characters
print("SUCCESS" == "ijoisafjiojiojSUCCESS")     #print true
print("SUCCESS" == text)                #print true


i = 0                       #i is a counter increment
number = 0                  #number refers to number of elements
                            #that contain "SUCCESS"
length = len(O_com)         #length of O_com list

#iterates though O_com list
while (i < length):
    #prints words that do not have "SUCCESS"
    if(text not in O_com[i]):       
        print(O_com[i])
    #count words that have "SUCCESS" but doesn't print
    elif((text in O_com[i])):
        number += 1
    #guarantees that all words without "SUCCESS" were printed
    if((number >= 1) and (i == length-1)):
        print("This worked")
        break
    i +=1
 