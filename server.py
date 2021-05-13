import socket, pickle
from time import sleep
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
# arr = [[-1,-1,1],[-1,1,-1],[1,-1,-1]]

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if data:
                    obj = pickle.loads(data)
                    print("servidor recebeu...")
                    print(obj)
                    print("delay de 5s")
                    sleep(5)
                    conn.sendall(b'ok')
                    break
            