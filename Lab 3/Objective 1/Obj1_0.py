#List of integer and float
list_1 = [1,2,3,4,5,6,7,8,9,10]
list_2 = [11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0]

#Replacing first 3 elemetns form list_1
list_1[0] = "one"
list_1[1] = "two"
list_1[2] = "three"

#printing list_1 and extra newline
print(list_1)
print()
#creating a tuple and it changes only the first 2 with what 
# tup contains
tup = ("eleven", "twelve", "thirteen")
list_2[:2] = tup

#printing list_2 and extra newline
print(list_2)
print()

# creating an empty list
joint_1 =[]
#using extend to initialize list with list_1
# note that list_1 and list_2 remain the same
joint_1.extend(list_1)
#concatenating list_1 with list_2 and storign in joint_1
joint_1.extend(list_2)
#printing joint_1 with extra newline
print(joint_1)
print()

#concatenating original list and storing in joint_2
joint_2 = list_1 + list_2
#printing joint 2
print(joint_2)

#adding 4 newlines for spacing purposes
for i in range(1,5):
    print()
    
#defining function list_shift 
# this function uses base_list and new_data to creates a list
#that contains the same number of elements from base_line
# and gets the last 4 (in this case) elements from the concatenated
#list
    
#NOTE: the base_list being return will not have the same elements
# as when it entered the function
def list_shift(base_list, new_data):
    #prints base_list
    print("fixed_length_list = ", end = ' ')
    print(base_list)
    #prints new_data
    print("new_data = ", end = ' ')
    print(new_data)
    
    #creates an empty list
    new_base_list = []
    #initialized list with base_list
    new_base_list.extend(base_list) 
    #concatenates new_base_list with new_data
    new_base_list.extend(new_data)
    
    # stores length of new_base_list
    a = (len(new_base_list))
    
    # re-initializes base_list with the last 4 elements of
    #new_base_list which depends on the length of base_list
    base_list = new_base_list[a-(len(base_list)): a]
    
    #prints the new list that appears shifted
    print("list_shift(fixed_length_list, new_data)")
    return base_list


fixed_length_list = [1,2,3,4]
new_data = [5,6,7]

print(list_shift(fixed_length_list, new_data))