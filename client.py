#client-one.py
import socket
import os

HOST = '127.0.0.1' #hostname
PORT = 65432  #server port
path = 'C:\\Users\\perry\\Documents\\GitHub\\Client-Server-Communication'

#Set up a system to ask the user to make a request

def Communication(query):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((HOST, PORT))

        #Upload a file to the server
        if query == 'upload':
            print('You selected upload.')
            filename = input('Input desired filename to upload to server: ')

            #Get file from computer and send it to the server.
            client.send(filename.encode('utf-8'))
            filepath = os.path.join(path, filename)
            filepath = os.path.join(path, filename)
            f = open(filepath, 'rb')
            l = f.read(1024)
            while l:
                client.send(l)
                l = f.read(1024)
            f.close()

        #Download a file from the server
        elif query == 'download':
            print('You selected download.')
            filename = input('Input desired filename to download from server: ')

            #Send requested filename to server for download
            client.send(filename.encode('utf-8'))
            filepath = os.path.join(path, filename)
            f = open(filepath, 'ab')
            while True:
                data = client.recv(1024)
                if not data:
                    break
                f.write(data)
            f.close()

while True:
    print('Upload or Download?')
    query = input('Enter an option: ').lower()

    if (query == 'upload') | (query == 'download'):
        Communication(query)
        break

    else:
        print('\"', query, '\" is not an acceptable option.')
        print('Please select from Upload or Download.')

            


