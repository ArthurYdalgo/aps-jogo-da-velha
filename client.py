import socket,pickle
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_serv = '127.0.0.1'

porta_serv = 65432

dest = (ip_serv,porta_serv)



tcp.connect(dest)
msg = int(input("Digite um numero: "))

tcp.send(pickle.dumps(msg))

tamp_resp = int.from_bytes(tcp.recv(4),'big')
resp = tcp.recv(tamp_resp)

print(resp.decode())
tcp.close()

