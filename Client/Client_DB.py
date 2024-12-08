# Dylan Brett (100933134)
# TPRG-2131-02
# Nov 30, 2024
# This program is strictly my own work. Any material
# beyond course learning materials that is taken from
# the Web or other sources is properly cited, giving
# credit to the original author(s). I havent used any
# code from other sources other than referncing the course material

#Cited
# https://www.datacamp.com/tutorial/json-data-python?utm_source=google&utm_medium=paid_search
# https://www.digitalocean.com/community/tutorials/python-remove-character-from-string
# https://www.datacamp.com/tutorial/python-trim

import socket
import json
import time

# Runs on PC, directly from Thonny
# The client
print("Client ready ctrl-c to exit")
s = socket.socket()
host = '127.0.0.1'  # ip of raspberry PI, running the server
port = 5000

# try to connect to server (if it doesnt connect it will close and print lost connection)
try:
    s.connect((host, port))
    while True:
        encoded_string = s.recv(1024)
        decoded_string = encoded_string.decode('utf-8') # decode the string
        data = json.loads(decoded_string) # converts the json string into a python object
        # access the dictionary values
        core = data["Temperature"]
        volts = data["Voltage"]
        core_clock = data["core-clock"]
        Gpu_clock = data["GPU-Clock"]
        video_voltage = data["Video-voltage"]

        # print out the real time data
        #print(encoded_string) # shows the raw data coming in
        print("Core Temperature:", core)
        print("Core Voltage:", volts, "V")
        print("Core Clock:", core_clock, "GHz")
        print("GPU Core Clock:", Gpu_clock, "GHz")
        print("Video Core Voltage:", video_voltage, "V")
        print("") # added a space between updates

except s.gaierror:
    print('error resolving host')
    s.close()
    
except KeyboardInterrupt:
    print("client exiting...") # exit the program if ctrl-c
    
finally:
    print("lost connection") # if the connection is lost the client will exit
    s.close()
    exit(1)
    
