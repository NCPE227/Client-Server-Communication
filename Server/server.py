import socket
import os
from tqdm import tqdm
import threading

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 #Send 4096 bytes per step
HOST = '0.0.0.0' #hostname
PORT = 65432  #server port
#SAVE_LOCATION = os.path.abspath('Documents')

def CLIENT_HANDLER(connection, address):
    connected = True
    while connected:
        '''#Accept the connection from a client
        connection, address = server.accept()
        print(f'Client connected from {connection}:{address}')
        #Printout to confirm connection
        print(f"{address} is connected.")'''

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
                
                #Receive 1024 bytes from the client
                bytes_read = connection.recv(BUFFER_SIZE)
                    
                f.write(bytes_read) #write the received bytes to a file with the same name
                progress.update(len(bytes_read)) #update the progress bar

            progress.close()
            ack = 'finished uploading'
            connection.send(ack.encode())

        elif request == 'download': #download will send a file to the client and allow it to write
            print(f'Received \'{request}\' request with filename \'{filename}\'')
            
            #Send the filename and filesize to the client
            filesize = os.path.getsize(filename)
            connection.send(f"{SEPARATOR}{filename}{SEPARATOR}{filesize}".encode())
            #print(filesize)

            #Start sending the file
            progress = tqdm(range(filesize), f'Sending {filename}', unit='B', unit_scale=True, unit_divisor=1024, mininterval=0) 
            with open(filename, 'rb') as f:
                #while True:
                #Read bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                    
                connection.sendall(bytes_read) #send bytes from server to client
                    
                #Update the progress bar
                progress.update(len(bytes_read))

                #print(f"bytes read {len(bytes_read)}   filesize {filesize}"W
            
            progress.close()
            ack = 'finished downloading'
            connection.send(ack.encode())

        else:
            server.send('Sorry, that was a bad request. Please try again.')
        
    connection.close()

#Function to start the server and assign incoming connections to threads
def start():

    while True:
        #Accept the connection from a client
        connection, address = server.accept()
        thread = threading.Thread(target=CLIENT_HANDLER, args=(connection, address))
        thread.start()

#Initialize server socket
server = socket.socket()
server.bind((HOST, PORT)) #bind server host and port
server.listen(5)
print(f"Listening as {HOST}:{PORT}") #printout to confirm connection
start()

server.close() #close server