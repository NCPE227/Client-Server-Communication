import socket
import os

HOST = '127.0.0.1' #hostname
PORT = 65432  #server port
path = 'C:\\Users\\perry\\Documents\\GitHub\\Client-Server-Communication'

client = socket.socket()
client.connect((HOST, PORT))

function = input('Upload File, Download File, or Quit? ').lower()

while function != 'quit':
    client.send(function.encode())
        
    data = client.recv(1024).decode()  #receive response
    print('Received from server: ' + data)  #show in terminal
    
    ver = data.split()
    if ver[0] == 'Good':
        function = input('Filename: ').lower()
    elif ver[0] == 'Bad':
        function = input('Upload File, Download File, or Quit? ').lower()
    elif ver[0] == 'Thanks':
        function = input('Upload File, Download File, or Quit? ').lower()
   
client.close()  #close the connection


