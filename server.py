import socket,pickle

tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


ip = ''
porta = 65432
orig = (ip,porta)
tcp.bind(orig)

while(True):
    print("escutando")
    tcp.listen(1)
    tcp_dados,cliente = tcp.accept()
    print("escutei")

    numero = int(input("escolha um numero: "))
    numeroCliente = int.from_bytes(tcp_dados.recv(4),'big')
    # resposta = pickle.loads(tcp_dados)

    if(numero + numeroCliente %2 ==0):
        print("ganhou")
        resposta = 'perdeu'
        resposta_b = pickle.dumps(resposta)
        tcp_dados.send(tam_resp+resposta.encode())
    else:
        print("perdeu")
        resposta = 'ganhou'
        tam_resp = (len(resposta)).to_bytes(4,'big')
        tcp_dados.send(tam_resp+resposta.encode())

tcp_dados.close()



