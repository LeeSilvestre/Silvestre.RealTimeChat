# Silvestre.RealTimeChat
Simple Real-TIme Chat Application using Python Sockets and Tkinter + Threading

SOLUTION

For the server.py:

1. I initially imported the necessary modules for my program.
2. I then set up some constants. The IP address of the server, port number for communication, and the maximum number of clients the server can handle simultaneously.
3. I then created a socket for communication. I bind the socket to the specified IP address and port.
4. I then set up a graphical user interface using Tkinter.
5. I did GUI styling.
6. I then created a label to display server status.
7. I then created a text box to display server information.
8. I then created a fuction to update information in the GUI.
9. I then created a function to lsiten for messages from clients.
10. I then created a function to send a message to all connected clients.
11. I then created a function to handle a new client connection.
12. I then created the main function to start the server and handle client connections.
13. I used threading to start the main function in a separate thread.

For the server.py, the server listens for incoming connections from clients. Each connected client has a separate thread to handle communication. It keeps track of active clients and broadcasts messages to all connected clients. The GUI displays server status and information about connections.

For the client.py:

1. I initially imported the necessary modules for my program.
2. I then set up some constants. The IP address of the server and the port number for communication.
3. I then set up GUI styling.
4. I then created a socket for communication.
5. I then created a function to add a message to the GUI.
6. I then created a function to connect to the server.
7. i then created a function to send a message to the server.
8. I then set up the GUI using Tkinter.
9. I then created the GUI layout.
10. I then created a function to listen for messages from the server.
11. I then created the main function to start the client GUI.

For the client.py, the client conencts to the server, providing a username. It uses separate threads to listen for messages from the server and handle user interaction. The GUI allows the user to input a username, send messages, and displays messages from other users.
