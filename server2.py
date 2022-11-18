import socket

HOST = "127.0.0.1"  #localhost
PORT = 65432  #port server is listening to

files = list() #create a list to hold the files that have been sent to the server

server = socket.socket()
server.bind((HOST, PORT))
print('Socket bound to port ', PORT)
server.listen(2)
print('Socket listening...')
connection, address = server.accept()  # accept new connection

while True:
    # receive data stream. it won't accept data packet greater than 1024 bytes
    data = connection.recv(1024).decode()
    if not data:
        # if data is not received break
        break
    print("from connected user: " + str(data))
    
    #Evaluate the request to see if it contains a valid request
    if (data == 'upload') | (data == 'download'):
        lastreq = data
        request = 'Good request. You chose \"{}\". Please enter a filename next.'.format(data)
    
    #Handle the second pass or the bad requests
    else:
        orig = data
        data = data.split('.') #split at a period to separate filename from it's extension
        print(data)
       
        if (data[-1] == 'txt') | (data[-1] == 'mp4') | (data[-1] == 'jpeg') | (data[-1] == 'png') | (data[-1] == 'png'):
            request = 'supported file type detected'
            
            if lastreq == 'upload':
                files.append(orig)
                request = 'Thanks for uploading data!'
            
            elif lastreq == 'download':
                for i in range(len(files)):
                    if orig == files[i]:
                        request = files[i]
                        break
                    else:
                        request = 'File not found on server.'
                    
        else:
            request = 'Bad request. You chose \"{}\", which is an invalid option. Choose Upload or Download.'.format(data)

    connection.send(request.encode())  #send data to the client

connection.close()  # close the connection