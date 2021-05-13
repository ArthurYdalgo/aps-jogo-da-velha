#!/usr/bin/env python3

import socket, pickle
from time import sleep

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
arr = [[-1,-1,1],[-1,1,-1],[1,-1,-1]]
data_string = pickle.dumps(arr)
a = 0
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        s.connect((HOST, PORT))
        print("enviando {}".format(a))
        s.sendall(pickle.dumps(a))  
        print("aguardando resposta")      
        data = s.recv(1024)
        print("recebido")
        a+=1
        # sleep(1)

    
    

print('Received', repr(data))