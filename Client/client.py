import socket
from tqdm import tqdm
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 #Send 4096 bytes per step
HOST = '127.0.0.1' #hostname
PORT = 65432  #server port

#Create socket for client and connect to host and port
client = socket.socket()
client.connect((HOST, PORT))
print('Connected to ', HOST, ':', PORT, ' Successfully')

#Ask the user to request one of the program's functions
function = input('Upload File, Download File, or Quit? ').lower()

#Program will quit if the users enters quit when selecting a function
while function != 'quit':
    if function == 'upload':
        print(f'You chose {function}.')
        
        #Ask for filename and get the size
        filename = input('Insert the name of the file you wish to upload: ')
        filesize = os.path.getsize(filename) #This would be handled on the server side for download
        
        #Send the function request, filename, and filesize to the server
        client.send(f'{function}{SEPARATOR}{filename}{SEPARATOR}{filesize}'.encode())

        #Start sending the file
        progress = tqdm(range(filesize), f'Sending {filename}', unit='B', unit_scale=True, unit_divisor=1024, mininterval=0) 
        with open(filename, 'rb') as f:
            while True:
                #Read bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read: #no more bytes to read
                    break
                
                client.sendall(bytes_read) #send bytes from client to server
                
                #Update the progress bar
                progress.update(len(bytes_read))
        
        #Stops the bar from repeating itself
        progress = 0
        
        #Receive an acknowledgement message
        received = client.recv(BUFFER_SIZE).decode()
        print(received)

        #Ask the user to request one of the program's functions
        function = input('Upload File, Download File, or Quit? ').lower()

    elif function == 'download':
        print(f'You chose {function}.')
        filename = input('Insert the name of the file you wish to download: ')

        #Send request to the server
        client.send(f'{function}{SEPARATOR}{filename}{SEPARATOR}{0}'.encode())

        
        #Use client's socket to receive the decoded file
        received = client.recv(BUFFER_SIZE).decode()
        request, filename, filesize = received.split(SEPARATOR)
        filename = os.path.basename(filename) #Remove absolute path
        filesize = int(filesize) #integer conversion for filesize, due to encoding/decoding
        
        with open(filename, 'wb') as f:
            #Create a server side progress bar
            progress = tqdm(range(filesize), f'Receiving {filename}', unit='B', unit_scale=True, unit_divisor=1024, mininterval=0)
            while True:
                #Receive 1024 bytes from the client
                bytes_read = client.recv(BUFFER_SIZE)
                if not bytes_read:    
                    break #file has been read when no more bytes are transmitted
                
                f.write(bytes_read) #write the received bytes to a file with the same name
                progress.update(len(bytes_read)) #update the progress bar

        #Stops the bar from repeating itself
        progress = 0

        #Receive an acknowledgement message
        received = client.recv(BUFFER_SIZE).decode()
        print(received)

        function = input('Upload File, Download File, or Quit? ').lower()

    else:
        print(f'Sorry, {function} is not a supported request.')
        function = input('Upload File, Download File, or Quit? ').lower()
        
client.close() #close the client socket
        
