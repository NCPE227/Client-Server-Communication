import socket
import os
from tqdm import tqdm
import threading

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 #Send 4096 bytes per step
HOST = socket.gethostbyname(socket.gethostname())#hostname
PORT = 65432  #server port
#SAVE_LOCATION = os.path.abspath('Documents')

#Initialize server socket
server = socket.socket()
server.bind((HOST, PORT)) #bind server host and port

#Function to handle client requests
def CLIENT_HANDLER(connection, address):
    print(f"{address} is connected.")

    connected = True
    while connected:
        #Use client's socket to receive the decoded file
        received = connection.recv(BUFFER_SIZE).decode()
        request, filename, filesize = received.split(SEPARATOR)
        filename = os.path.basename(filename) #Remove absolute path
        filesize = int(filesize) #integer conversion for filesize, due to encoding/decoding

        #Handle 2 different request options
        if request == 'upload': #upload will take a file from the client and write it to the server
            print(f'Received \'{request}\' request with filename \'{filename}\'')

            with open(filename, 'wb') as f:
                #Create a server side progress bar
                progress = tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024, mininterval=0)
                while True:
                    #Receive 1024 bytes from the client
                    bytes_read = connection.recv(BUFFER_SIZE)
                    if not bytes_read:    
                        break #file has been read when no more bytes are transmitted
                
                    f.write(bytes_read) #write the received bytes to a file with the same name
                    progress.update(len(bytes_read)) #update the progress bar
                    if bytes_read == filesize:
                        break
        
            ack = 'finished uploading'
            connection.send(ack.encode())

        elif request == 'download': #download will send a file to the client and allow it to write
            print(f'Received \'{request}\' request with filename \'{filename}\'')
        
            #Send the filename and filesize to the client
            filesize = os.path.getsize(filename)
            connection.send(f"{SEPARATOR}{filename}{SEPARATOR}{filesize}".encode())

            #Start sending the file
            progress = tqdm(range(filesize), f'Sending {filename}', unit='B', unit_scale=True, unit_divisor=1024, mininterval=0) 
            with open(filename, 'rb') as f:
                while True:
                    #Read bytes from the file
                    bytes_read = f.read(BUFFER_SIZE)
                    if not bytes_read: #no more bytes to read
                        break
                
                    connection.sendall(bytes_read) #send bytes from server to client
                
                    #Update the progress bar
                    progress.update(len(bytes_read))
                #Cleanse progress bar
                progress = 0

            ack = 'finished downloading'
            connection.send(ack.encode())

        else:
            server.send('Sorry, that was a bad request. Please try again.')


    connection.close() #close server

#Function to start the server and assign incoming connections to threads
def start():
    server.listen(5)
    print(f"Listening as {HOST}:{PORT}") #printout to confirm connection

    while True:
        #Accept the connection from a client
        connection, address = server.accept()
        thread = threading.Thread(target=CLIENT_HANDLER, args=(connection, address))
        thread.start()

start()
