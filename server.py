import socket,pickle


tcp = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


ip = ''
porta = 65432
orig = (ip,porta)
tcp.bind(orig)

class Game():
    def __init__(self):
        self.player_1 = None
        self.player_2 = None
        self.current_player = None
        self.over = None

        self.tic_tac_toe = [
            [0,0,0],
            [0,0,0],
            [0,0,0],
        ]

    def checkWinner(self,grid): #por algum motivo não conseguia chamar essa função do msm jeito q o jogo, entao dupliquei ela
    # Complete line?
        for i in range(3):
            jogador1 = 0
            jogador2 = 0
            for j in range(3):
                if (grid[i][j]==1):
                    jogador1+=1
                elif(grid[i][j]==2):
                    jogador2+=1
            if(jogador1 == 3):
                return 1
            elif(jogador2 == 3):
                return 2
        
        for i in range(3):
            jogador1 = 0
            jogador2 = 0
            for j in range(3):
                if (grid[j][i]==1):
                    jogador1+=1
                elif(grid[j][i]==2):
                    jogador2+=1
            if(jogador1 == 3):
                return 1
            elif(jogador2 == 3):
                return 2
        
        jogador1 = 0
        jogador2 = 0
        for i in range(3):
            
            if (grid[i][i]==1):
                jogador1+=1
            elif(grid[i][i]==2):
                jogador2+=1
        if(jogador1 == 3):
            return 1
        elif(jogador2 == 3):
            return 2

        jogador1 = 0
        jogador2 = 0
        for i in range(3):
            
            if (grid[2-i][i]==1):
                jogador1+=1
            elif(grid[2-i][i]==2):
                jogador2+=1
                
        if(jogador1 == 3):
            return 1
        elif(jogador2 == 3):
            return 2
        
            
        # nope, not an objective state
        return 0

    def insertPlayer(self,mac):
        if(self.player_1 is None):
            self.player_1 = mac
            return 1
        elif((not (self.player_1 is None)) and (self.player_2 is None) and mac != self.player_1):
            self.player_2 = mac
            self.current_player = 1
            print("jogo iniciado")
            return 2
        else:
            print("mac ja em uso")
            return 'unavailable'

    def registerAction(self,player_number,mac,coordinates):
        print("jogador {} ({}) jogou em {} , {}".format(player_number,mac,coordinates[0],coordinates[1]))
        # Validate action
        if((self.player_1 is None) or (self.player_2 is None)):
            print("jogada invalida1")
            return "invalid"


        if(self.current_player != player_number):
            print("jogada invalida2")
            return "invalid"

        if(player_number == 1):
            if(self.player_1 != mac):
                print("jogada invalida3")
                return "invalid"   
        else:
            if(self.player_2 != mac):
                print("jogada invalida4")
                return "invalid"
        
        x , y = coordinates 
        if(not(0<=x<=2) or not(0<=y<=2)):
            pass
        if(self.tic_tac_toe[x][y]!=0):
            print("jogada invalida5")
            return "invalid"
        
        self.tic_tac_toe[x][y]=player_number
        board = self.tic_tac_toe
        if(self.current_player == 1):
            self.current_player = 2
        else:
            self.current_player = 1
        print("checando vencedor")
        ganhador = self.checkWinner(board)
        
        if(ganhador!=0):
            print("vencedor {}".format(ganhador))
            game.over = True
                    
            self.current_player = None

            # self.tic_tac_toe = [
            #     [0,0,0],
            #     [0,0,0],
            #     [0,0,0],
            # ]

        return board
        

        pass
    
game = Game()

while(True):
    #print("escutando")
    tcp.listen(1)
    tcp_dados,cliente = tcp.accept()
    #print("escutei")

    received_data = pickle.loads(tcp_dados.recv(1024))

    command = received_data['command']

    if(command == 'insert'):
        mac = received_data['data']
        print("inserindo jogador ({})".format(mac))
        response = game.insertPlayer(mac)
        pass
    elif(command == 'action'):    
        player_number = received_data['data']['player']
        mac = received_data['data']['mac']
        coordinates = received_data['data']['coordinates']

        response = game.registerAction(player_number,mac,coordinates)        
        pass
    elif(command == 'refresh'):
        response = {'grid':game.tic_tac_toe,'current_player':game.current_player}
        if(game.over):            
            game.player_1 , game.player_2 = None , None
            game.tic_tac_toe = [
                [0,0,0],
                [0,0,0],
                [0,0,0],
            ]
            game.over = None
        
    tcp_dados.send(pickle.dumps(response))
    

tcp_dados.close()



