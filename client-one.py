import threading
import socket
import os
from time import perf_counter
from time import sleep

#Init client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Set port and connect to it
port = 11111
client.connect(('10.113.32.109' , port))
path = 'files'