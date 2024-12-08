# Dylan Brett (100933134)
# TPRG-2131-02
# Dec 7, 2024
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


s = socket.socket()
host = '127.0.0.1'
port = 5000

s.bind((host, port))
s.listen(5)
print("server active ctrl-c to shut down") # displays if the server has been turned on

# try to connect to server (if it doesnt connect it will close and print lost connection)
try:
    c, addr = s.accept()
    print ('Got connection from',addr)
    while True:
        encoded_string = c.recv(1024)
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

except ConnectionResetError: # if the client disconnects then the program will stop sending data
    print("the client has disconnected")
    c.close()
except BrokenPipeError: # when the client disconnects using ctrl-c will stop sending the data
    print("the client has disconnected")
    c.close()
except KeyboardInterrupt: # press ctrl-c to exit the program
    print("")
    print("Server Shutting down")
    c.close()
    exit(1)
        
        



