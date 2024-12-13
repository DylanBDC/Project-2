# Project-2

Description:

The server file was designed to display any RPI data that connects to the server using the client for up to 50 iterations (displayed as iterations in the GUI). After the 50 iterations, the server waits for a new connection until it shuts down. When the server is closed ('EXIT'), the client will remain shown, but the connection status LED will stop blinking, which shows that it has lost connection (it also prints a lost connection message in the terminal).
The client of this program was designed to display the connection status to the server and collect data to be sent to the server for display. When the server isn't active (initially), the client will not activate and will exit. When the client sends all the data, it will close and print a server message saying that all the data has been sent and allow another client to join.


How to use:

First, run the server and then run the client. The client should connect to the server fast and start sending data displayed in the GUI (ensure the right Address and port are used)


Cited:

https://stackoverflow.com/questions/74578705/how-to-update-text-in-pysimplegui
https://www.datacamp.com/tutorial/json-data-python?utm_source=google&utm_medium=paid_search
https://www.digitalocean.com/community/tutorials/python-remove-character-from-string
https://www.datacamp.com/tutorial/python-trim
