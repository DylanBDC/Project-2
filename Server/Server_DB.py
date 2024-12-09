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
import PySimpleGUI as sg
import time


s = socket.socket()
host = '127.0.0.1'
port = 5000

s.bind((host, port))
s.listen(5)
print("server active ctrl-c to shut down") # displays if the server has been turned on

def __init__():
    '''
    initiates the data being sent with a default value
    '''
    data = {"Temperature": 0, "Voltage": 0, "core-clock": 0, "GPU-Clock": 0, "Video-voltage": 0, "Iterations": 0}
    return data

sg.theme('DarkAmber') # Add a touch of color
# All the stuff inside your window.
layout = [	 [sg.Text('RPi Data')], # change text to ask the user to enter a date
            [sg.Text(f"Core Temperature: {__init__()['Temperature']}°C", key='Temp')], # show the user the desired date format
            [sg.Text(f"Voltage: {__init__()['Voltage']}V", key= 'Voltage')],
            [sg.Text(f"Core Clock: {__init__()['core-clock']}GHz", key= 'Core')],
            [sg.Text(f"GPU Clock: {__init__()['GPU-Clock']}GHz", key= 'GPU')],
            [sg.Text(f"Video Core Voltage: {__init__()['Video-voltage']}V", key= 'Video')],
            [sg.Text(f"Iteration: {__init__()['Iterations']}", key= 'iteration')],
            [sg.Button('EXIT')] ]
# Create the Window
window = sg.Window('RPi Data', layout) # added my name to the title

# try to connect to server (if it doesnt connect it will close and print lost connection)
while True:
#     c, addr = s.accept()
#     print ('Got connection from',addr)
    
    try:
        c, addr = s.accept()
        print ('Got connection from',addr)
        while True:
            event, values = window.read(1)
    
            if event in (sg.WIN_CLOSED, 'EXIT'):
                window.close()
            try:
                encoded_string = c.recv(1024)
                decoded_string = encoded_string.decode('utf-8') # decode the string
                data = json.loads(decoded_string) # converts the json string into a python object
                # access the dictionary values
                core = data["Temperature"]
                volts = data["Voltage"]
                core_clock = data["core-clock"]
                Gpu_clock = data["GPU-Clock"]
                video_voltage = data["Video-voltage"]
                iterations = data["Iterations"]

                # print out the real time data
                #print(encoded_string) # shows the raw data coming in
                print("Core Temperature:", core)
                print("Core Voltage:", volts, "V")
                print("Core Clock:", core_clock, "GHz")
                print("GPU Core Clock:", Gpu_clock, "GHz")
                print("Video Core Voltage:", video_voltage, "V")
                print(iterations)
                print("") # added a space between updates
                

                window['Temp'].update(f"Core Temperature: {data['Temperature']}°C")
                window['Voltage'].update(f"Voltage: {data['Voltage']}V")
                window['Core'].update(f"Core Clock: {data['core-clock']}GHz")
                window['GPU'].update(f"GPU Clock: {data['GPU-Clock']}GHz")
                window['Video'].update(f"Video Core Voltage: {data['Video-voltage']}V")
                window['iteration'].update(f"Iteration: {data['Iterations']}")
                
                
                #window = sg.Window('RPi Data', layout) # added my name to the title
            except:
                print("all data sent")
                window.close()
                break

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
        
        



