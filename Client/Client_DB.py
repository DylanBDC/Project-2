# Dylan Brett (100933134)
# TPRG-2131-02
# Dec 13, 2024
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
import PySimpleGUI as sg
import threading
from pathlib import Path


# Runs on Pi, directly from Thonny
# The client
print("Client ready ctrl-c to exit")
s = socket.socket()
host = '127.0.0.1' # Localhost (server IP)
#host = '10.160.41.223'
port = 5000
sg.theme('DarkAmber')

layout = [	 [sg.Text('Connection status'), sg.Text('\u25EF', text_color='Red', key='-LED0-')],
             [sg.Button('EXIT')]]

window = sg.Window('RPi Data', layout)

#def IS_RPI():
try:
    cpuinfo = Path('/proc/cpuinfo').read_text()
    if 'BCM' in cpuinfo:
        print('is a RPi') # RPi proc is the BCM2835 (should pretty much only be for the RPi)
    else:
        print('not a RPi')
        exit(1)
except FileNotFoundError:
    print('not a RPi')
    exit(2)
        
#def connection_status():
    #while True:
        
    #print(cpuinfo)
    
def RPi_temp():
    '''
    This def gets the Temperature of the RPis core
    '''
    #gets the Core Temperature from Pi, ref https://github.com/nicmcd/vcgencmd/blob/master/README.md
    core = os.popen('vcgencmd measure_temp').readline() #gets from the os, using vcgencmd - the core-temperature
    core_temp = round(float(core.strip('temp=').replace("'C", "")), 1) # remove unwanted text using .strip (already rounded to one decimal place)
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
# def LED_blink():
#     Led_state = True
#     while True:
#         
#         time.sleep(1)
#         Led_state = not Led_state # changes the state of the LED in each loop (blinks the LED)
#         
# blinkthread = threading.Thread(target=LED_blink)
# blinkthread.start()


# def connection_status():
#     
#     while (connection):
            
            
Led_state = True
# try and except to see if the client disconnects
try:
    s.connect((host, port))
    print("connecting")
    print(s.connect)
    #print(IS_RPI())
    iterations=0 #count
    
    # loop to keep sending data
    for i in range(5): # using 5 for now instead of 50
        
        # real time values of server
        event, values = window.read(100)
        if event in (sg.WIN_CLOSED, 'EXIT'):
            window.close()
            break
        core = RPi_temp()
        volts = RPi_volts()
        core_clock = Core_clock()
        Gpu_clock = Gpu_core()
        video_voltage = VideoCore_voltage()
        iterations= iterations+1
        if Led_state:
            window[f'-LED{0}-'].update('\u2B24')
                    
        else:
            window[f'-LED{0}-'].update('\u25EF')
            
        Led_state = not Led_state
        # dictionary for the real time values (with a key and its value)  
        jsonResult = {"Temperature": core, "Voltage": volts, "core-clock": core_clock, "GPU-Clock": Gpu_clock, "Video-voltage": video_voltage, "Iterations": iterations}
        jsonResult = json.dumps(jsonResult) # used to serialize the Python object and write it to the JSON file
        jsonbyte = bytes(jsonResult, "utf-8") # encodes the data (send as bytes)
        s.sendall(jsonbyte) # sends data as a byte type
        time.sleep(2) # used to slow down or speed up the data being sent (set to 2 second intervals)
        #print(jsonbyte) # optional printout to see data flow (i used it for testing(logging))
        
        if iterations == 5:
            print('All 50 iterations sent')
            window[f'-LED{0}-'].update('\u25EF')
        #window.close() 
except (ConnectionResetError, BrokenPipeError): # if the client disconnects then the program will stop sending data
    print("lost connection")
    window[f'-LED{0}-'].update('\u25EF')
    s.close()
except KeyboardInterrupt: # press ctrl-c to exit the program
    print("")
    print("Client Shutting down")
    s.close()
    exit(1)
except OSError:
    print("Cant connect")
    s.close()
    exit(1)
except:
    print("couldnt connect")
# finally:
#     #print("50 iterations sent") # if the connection is lost the client will exit
#     s.close()
#     exit(0)
  
