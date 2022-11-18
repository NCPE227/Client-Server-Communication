import socket
import os
import tqdm

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096 #Send 4096 bytes per step
HOST = '127.0.0.1' #hostname
PORT = 65432  #server port

#Initialize server socket
server = socket.socket()
server.bind((HOST, PORT)) #bind server host and port
server.listen(5)
print(f"[*] Listening as {HOST}:{PORT}") #printout to confirm connection

#Accept the connection from a client
connection, address = server.accept()
#Printout to confirm connection
print(f"[+] {address} is connected.")

#Use client's socket to receive the decoded file
received = connection.recv(BUFFER_SIZE).decode()
request, filename, filesize = received.split(SEPARATOR)
filename = os.path.basename(filename) #Remove absolute path
filesize = int(filesize) #integer conversion for filesize, due to encoding/decoding

#Handle 2 different request options
if request == 'upload': #upload will take a file from the client and write it to the server
    #Receive a file from the client
    progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as f:
        while True:
            # read 1024 bytes from the socket (receive)
            bytes_read = connection.recv(BUFFER_SIZE)
            if not bytes_read:    
                # nothing is received
                # file transmitting is done
                break
            f.write(bytes_read) #write the file
            progress.update(len(bytes_read)) #update our progress bar

elif request == 'download': #download will send a file to the client and allow it to write
        
        #Send the filename and filesize to the client
        server.send(f"{SEPARATOR}{filename}{SEPARATOR}{filesize}".encode())

        #Start sending the file
        progress = tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024) 
        with open(filename, "rb") as f:
            while True:
                #Read bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read: #no more bytes to read
                    break
    
                server.sendall(bytes_read)
                
                #Update the progress bar
                progress.update(len(bytes_read))
        data = server.recv(BUFFER_SIZE) #get an acknowledgement message from the server

else:
    server.send('Sorry, that was a bad request. Please try again.')