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

# This server runs on Pi, sends Pi's your 4 arguments from the vcgencmds, sent as Json object.

# details of the Pi's vcgencmds - https://www.tomshardware.com/how-to/raspberry-pi-benchmark-vcgencmd
# more vcgens on Pi 4, https://forums.raspberrypi.com/viewtopic.php?t=245733
# more of these at https://www.nicm.dev/vcgencmd/

import socket
import os, time
import json


# Runs on PC, directly from Thonny
# The client
print("Client ready ctrl-c to exit")
s = socket.socket()
host = '127.0.0.1' # Localhost (server IP)
port = 5000




def RPi_temp():
    '''
    This def gets the Temperature of the RPis core
    '''
    #gets the Core Temperature from Pi, ref https://github.com/nicmcd/vcgencmd/blob/master/README.md
    core = os.popen('vcgencmd measure_temp').readline() #gets from the os, using vcgencmd - the core-temperature
    core_temp = core.strip('temp=') # remove unwanted text using .strip (already rounded to one decimal place)
    return core_temp

def RPi_volts():
    '''
    This def gets the Voltage of the RPis core
    '''
    # ref https://github.com/nicmcd/vcgencmd/blob/master/README.md
    volts = os.popen('vcgencmd measure_volts core').readline() #gets from the os, using vcgencmd
    core_volts = round(float(volts.strip('volt=').replace('V', '')), 1) # remove unwanted text using .strip and .replace and round to one decimal place
    return core_volts

def Core_clock():
    '''
    This def gets the Clock speed of the RPis core
    '''
    # ref https://github.com/nicmcd/vcgencmd/blob/master/README.md
    clock = os.popen('vcgencmd measure_clock arm').readline() #gets from the os, using vcgencmd
    core_clock = float(clock.replace('frequency(48)=', '')) # remove unwanted text using .replace and convert to a float
    core_GHz = round(core_clock/1000000000, 1)
    return core_GHz

def Gpu_core():
    '''
    This def gets the GPU clock speed of the RPis core
    '''
    # ref https://github.com/nicmcd/vcgencmd/blob/master/README.md
    Gpu = os.popen('vcgencmd measure_clock core').readline() #gets from the os, using vcgencmd
    Gpu_core = float(Gpu.replace('frequency(1)=', '')) # remove unwanted text using .replace and convert to a float
    Gpu_GHz = round(Gpu_core/1000000000, 1) # Change to GHz and round to one decimal place
    return Gpu_GHz

def VideoCore_voltage():
    '''
    This def gets the Video Core Voltage of the RPis core
    '''
    # ref https://github.com/nicmcd/vcgencmd/blob/master/README.md
    video = os.popen('vcgencmd measure_volts core').readline() #gets from the os, using vcgencmd
    video_voltage = round(float(video.strip('volt=').replace('V', '')), 1) # remove unwanted text using .strip and .replace and round to one decimal place
    return video_voltage

# loop to keep connecting to clients
while True:
    # try and except to see if the client disconnects
    try:
        s.connect((host, port))
        
        # loop to keep sending data
        while True:
            # real time values of server
            core = RPi_temp()
            volts = RPi_volts()
            core_clock = Core_clock()
            Gpu_clock = Gpu_core()
            video_voltage = VideoCore_voltage()
            
            # dictionary for the real time values (with a key and its value)  
            jsonResult = {"Temperature": core, "Voltage": volts, "core-clock": core_clock, "GPU-Clock": Gpu_clock, "Video-voltage": video_voltage}
            jsonResult = json.dumps(jsonResult) # used to serialize the Python object and write it to the JSON file
            jsonbyte = bytes(jsonResult, "utf-8") # encodes the data (send as bytes)
            s.send(jsonbyte) # sends data as a byte type
            time.sleep(1) # used to slow down or speed up the data being sent
            #print(jsonbyte) # optional printout to see data flow (i used it for testing(logging))
            
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
    finally:
        print("lost connection") # if the connection is lost the client will exit
        s.close()
        exit(1)
    
