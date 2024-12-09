# Dylan Brett (100933134)
# TPRG-2131-02
# Dec 9, 2024
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
from random import randint as randint


s = socket.socket()
host = '127.0.0.1'
#host = '10.0.0.180'
port = 5000
s.bind((host, port))
s.listen(5)
print("server active ctrl-c to shut down") # displays if the server has been turned on
sg.theme('DarkAmber') # Add a touch of color

def initiate():
    '''
    initiates the data being sent with a default value
    '''
    data = {"Temperature": 0, "Voltage": 0, "core-clock": 0, "GPU-Clock": 0, "Video-voltage": 0, "Iterations": 0}
    return data
def LED(color, key):
    return sg.Text('\u25EF', text_color=color, key=key)
#def LED_blink():
    
# All the stuff inside your window.
layout = [	 [sg.Text('RPi Data'), LED('Red', '-LED0-')], # change text to ask the user to enter a date
            [sg.Text("Core Temperature:"), sg.Text(f"{initiate()['Temperature']}", key='Temp'), sg.Text("°C")], # show the user the desired date format
            [sg.Text(f"Voltage: {initiate()['Voltage']}V", key= 'Voltage')],
            [sg.Text(f"Core Clock: {initiate()['core-clock']}GHz", key= 'Core')],
            [sg.Text(f"GPU Clock: {initiate()['GPU-Clock']}GHz", key= 'GPU')],
            [sg.Text(f"Video Core Voltage: {initiate()['Video-voltage']}V", key= 'Video')],
            [sg.Text(f"Iteration: {initiate()['Iterations']}", key= 'iteration')],
            [sg.Button('EXIT')] ]
# Create the Window
window = sg.Window('RPi Data', layout) # added my name to the title
Led_state = True # start the Led off as true and keep toggling 
# try to connect to server (if it doesnt connect it will close and print lost connection)
while True:
#     c, addr = s.accept()
#     print ('Got connection from',addr)

    event, values = window.read(100) # waiting for connection displaying default values
    if event in (sg.WIN_CLOSED, 'EXIT'):
        #window.close()
        break
    try:
        c, addr = s.accept()
        print ('Got connection from',addr)
        while True:
            event, values = window.read(100)
    
            if event in (sg.WIN_CLOSED, 'EXIT'):
                window.close()
                break
            
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

                # print out the real time data (in the shell)
                #print(encoded_string) # shows the raw data coming in
                print("Core Temperature:", core)
                print("Core Voltage:", volts, "V")
                print("Core Clock:", core_clock, "GHz")
                print("GPU Core Clock:", Gpu_clock, "GHz")
                print("Video Core Voltage:", video_voltage, "V")
                print(iterations)
                print("") # added a space between updates
                

                window['Temp'].update(f"{data['Temperature']}")
                window['Voltage'].update(f"Voltage: {data['Voltage']}V")
                window['Core'].update(f"Core Clock: {data['core-clock']}GHz")
                window['GPU'].update(f"GPU Clock: {data['GPU-Clock']}GHz")
                window['Video'].update(f"Video Core Voltage: {data['Video-voltage']}V")
                window['iteration'].update(f"Iteration: {data['Iterations']}")
                #window[f'-LED{0}-'].update('\u2B24' if randint(1, 2) == 2 else '\u25EF')
                if Led_state:
                    window[f'-LED{0}-'].update('\u2B24')
                    
                else:
                    window[f'-LED{0}-'].update('\u25EF')
                    
                Led_state = not Led_state # changes the state of the LED in each loop (blinks the LED)
                
                
                #window = sg.Window('RPi Data', layout) # added my name to the title
            except:
                print("all data sent")
                window.close() # when all the data has been sent it will close the window and exit
                exit()

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
window.close()        
        



