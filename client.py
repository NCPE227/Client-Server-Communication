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
print('Connected to ', HOST, ' : ', PORT, ' Successfully')

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
        client.send(f"{function}{SEPARATOR}{filename}{SEPARATOR}{filesize}".encode())

        #Start sending the file
        progress = tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024) 
        with open(filename, "rb") as f:
            while True:
                #Read bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read: #no more bytes to read
                    break
    
                client.sendall(bytes_read)
                
                #Update the progress bar
                progress.update(len(bytes_read))
        data = client.recv(BUFFER_SIZE) #get an acknowledgement message from the server

    elif function == 'download':
        print('You chose {}.').format(function)
        filename = input('Insert the name of the file you wish to download: ')
        data = client.recv(BUFFER_SIZE).decode() #receive the filename and filesize of the desired file in the server
        progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
        
        #Open file and write it to the local directory
        with open(filename, "wb") as f:
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = client.recv(BUFFER_SIZE)
                if not bytes_read:    
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))

    else:
        print('Sorry, {} is not a supported request.').format(function)
        function = input('Upload File, Download File, or Quit? ').lower()
        
client.close() #close the client socket
        
