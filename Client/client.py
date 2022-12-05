import socket
from tqdm import tqdm
import os

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 #Send 4096 bytes per step
#HOST = '127.0.0.1' #hostname
#PORT = 65432  #server port

#Function to connect to a server
def CONNECT(SERVER_IP, PORT):
    client = socket.socket()
    client.connect((SERVER_IP, int(PORT)))
    print(print('Connected to ', SERVER_IP, ':', PORT, ' Successfully'))
    return client

#Function to upload files to the server
def UPLOAD(client, filename, filesize):
    #Send the function request, filename, and filesize to the server
    client.send(f'{function}{SEPARATOR}{filename}{SEPARATOR}{filesize}'.encode())

    #Start sending the file
    progress = tqdm(range(filesize), f'Sending {filename}', unit='B', unit_scale=True, unit_divisor=1024, mininterval=0) 
    with open(filename, 'rb') as f:
        #Read bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
                
        client.sendall(bytes_read) #send bytes from client to server
                
        #Update the progress bar
        progress.update(len(bytes_read))
    progress.close()

    #Receive an acknowledgement message
    received = client.recv(BUFFER_SIZE).decode()
    print(received)

#Function to download files from the server
def DOWNLOAD(client, filename):
    #Send request to the server
    client.send(f'{function}{SEPARATOR}{filename}{SEPARATOR}{0}'.encode())

    #Use client's socket to receive the decoded file
    received = client.recv(BUFFER_SIZE).decode()
    request, filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename) #Remove absolute path
    filesize = int(filesize) #integer conversion for filesize, due to encoding/decoding

    #Create a server side progress bar
    progress = tqdm(range(filesize), f'Receiving {filename}', unit='B', unit_scale=True, unit_divisor=1024, mininterval=0)    
    with open(filename, 'wb') as f:
        #Receive 1024 bytes from the client
        bytes_read = client.recv(BUFFER_SIZE)
                
        f.write(bytes_read) #write the received bytes to a file with the same name
        progress.update(len(bytes_read)) #update the progress bar
    progress.close()

    #Receive an acknowledgement message
    received = client.recv(BUFFER_SIZE).decode()
    print(received)

#Function to show directory
def DIR():
    print('files in \"', os.getcwd(), '\"')
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    for f in files:
        print(f)

#Delete a given file
def DELETE(filename):
    if os.path.exists(filename):
        os.remove(filename)
        print(f'Successfully deleted \"{filename}\".')
    else:
        print(f'\"{filename}\" does not exist.')

#Get user input for connection to server
ip = input('Enter server IP (ex. 127.0.0.1): ') 
port = input('Select Port (ex. 65432): ')

#Run connect function using user input
#Will only work if server is running
client = CONNECT(ip, port)

#Ask the user to request one of the program's functions
function = input('UPLOAD, DOWNLOAD, DIR, DELETE, or QUIT? ').lower()

#Program will quit if the users enters quit when selecting a function
while function != 'quit':
    if function == 'upload':
        print(f'You chose {function}.')

        #Ask for filename and get the size
        filename = input('Insert the name of the file you wish to upload: ')
        filesize = os.path.getsize(filename) #This would be handled on the server side for download
        
        #Run UPLOAD
        UPLOAD(client, filename, filesize)

        #Ask the user to request one of the program's functions
        function = input('UPLOAD, DOWNLOAD, DIR, DELETE, or QUIT? ').lower()

    elif function == 'download':
        print(f'You chose {function}.')
        
        #Ask for user to input the name of the file they want from the server
        filename = input('Insert the name of the file you wish to download: ')
        
        #Run DOWNLOAD
        DOWNLOAD(client, filename)

        function = input('UPLOAD, DOWNLOAD, DIR, DELETE, or QUIT? ').lower()

    elif function == 'dir':
        print(f'You chose {function}.')
        DIR()
        function = input('UPLOAD, DOWNLOAD, DIR, DELETE, or QUIT? ').lower()

    elif function == 'delete':
        print(f'You chose {function}.')
        filename = input('Insert the name of the file you wish to delete: ')
        DELETE(filename)
        function = input('UPLOAD, DOWNLOAD, DIR, DELETE, or QUIT? ').lower()     

    else:
        print(f'Sorry, {function} is not a supported request.')
        function = input('UPLOAD, DOWNLOAD, DIR, DELETE, or QUIT? ').lower()
        
client.close() #close the client socket
        
