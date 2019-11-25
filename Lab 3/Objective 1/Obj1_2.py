name = "Jesi"                       # initialize string name with "Jesi"
byte_name = name.encode('utf-8')    # econde string to byte array
byte_name_bad = byte_name + b'\xef' # append non-utf-8 character

#error handling for byte_name_bad
try:
    byte_name_bad = byte_name_bad.decode()
# ran into error. Error message displayed:
# 'utf-8' codec can't decode byte 0xef in position 4: unexpected
# end of data
except ValueError:
    byte_name_bad = " "
    
    
# error handling for byte_name
try:
    byte_name = byte_name.decode()
    print(byte_name)
except:
    byte_name = " "