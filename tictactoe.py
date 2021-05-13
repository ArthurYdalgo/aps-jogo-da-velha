# -*- coding: utf-8 -*-
"""
Recriação do Jogo da Velha

@author: Prof. Daniel Cavalcanti Jeronymo
"""
count = 0
cX = -1
cY = -1

player1=0
player2=0

cPlayer_ = 0

whoAmI = 0

import pygame
import copy
import sys
import traceback
import random
import numpy as np
from uuid import getnode as get_mac
import socket,pickle
from time import time 

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


def refreshGame():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    ip_serv = '127.0.0.1'

    porta_serv = 65432

    dest = (ip_serv,porta_serv)


    tcp.connect(dest)

    tcp.send(pickle.dumps({'command':'refresh'}))
    
    resp = pickle.loads(tcp.recv(1024))

    print(resp)

    tcp.close()

    return resp


def action(player_num,mac,coordenadas):
    jogada = {
        'command' : 'action',
        'data' : {
            'player' : player_num,
            'mac' : mac,
            'coordinates' :coordenadas
        }
    }

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    ip_serv = '127.0.0.1'

    porta_serv = 65432

    dest = (ip_serv,porta_serv)


    tcp.connect(dest)

    tcp.send(pickle.dumps(jogada))

    # tamp_resp = int.from_bytes(tcp.recv(4),'big')
    resp = pickle.loads(tcp.recv(1024))

    print(resp)
    tcp.close()

    return resp


class GameConstants:
    #                  R    G    B
    ColorWhite     = (255, 255, 255)
    ColorBlack     = (  0,   0,   0)
    ColorRed       = (255,   0,   0)
    ColorGreen     = (  0, 255,   0)
    ColorBlue     = (  0, 0,   255)
    ColorDarkGreen = (  0, 155,   0)
    ColorDarkGray  = ( 40,  40,  40)
    BackgroundColor = ColorBlack
    
    screenScale = 1
    screenWidth = screenScale*600
    screenHeight = screenScale*600
    
    # grid size in units
    gridWidth = 3
    gridHeight = 3
    
    # grid size in pixels
    gridMarginSize = 5
    gridCellWidth = screenWidth//gridWidth - 2*gridMarginSize
    gridCellHeight = screenHeight//gridHeight - 2*gridMarginSize
    
    randomSeed = 0
    
    FPS = 30
    
    fontSize = 20

class Game:
    class GameState:
        # 0 empty, 1 X, 2 O
        grid = np.zeros((GameConstants.gridHeight, GameConstants.gridWidth))
        currentPlayer = 1
        turn = None
    
    def __init__(self, expectUserInputs=True):
        self.expectUserInputs = expectUserInputs
        
        # Game state list - stores a state for each time step (initial state)
        gs = Game.GameState()
        self.states = [gs]
        
        # Determines if simulation is active or not
        self.alive = True
        
        self.currentPlayer = 1
        
        # Journal of inputs by users (stack)
        self.eventJournal = []
        
    

    def checkObjectiveState(self, gs):

        grid = gs.grid
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
    
    
    # Implements a game tick
    # Each call simulates a world step
    def update(self):  
        # If the game is done or there is no event, do nothing
        if not self.alive or not self.eventJournal:
            return
        
        # Get the current (last) game state
        gs = self.states[-1]
        
        
        # # Switch player turn
        # if gs.currentPlayer == 0:
        #     gs.currentPlayer = 1
        # elif gs.currentPlayer == 1:
        #     gs.currentPlayer = 2
        # elif gs.currentPlayer == 2:
        #     gs.currentPlayer = 1
            
        # Mark the cell clicked by this player
        cell = self.eventJournal.pop()
        gs.grid[cell[0]][cell[1]] = gs.currentPlayer
        global grid_
        grid_ = gs.grid

        
        
        # Check if end of game
        if self.checkObjectiveState(gs):
            self.alive = False
                
        # Add the new modified state
        self.states += [gs]

def ganhadorDoJogo(grid): #por algum motivo não conseguia chamar essa função do msm jeito q o jogo, entao dupliquei ela
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

def permutate(grid_,cPlayer):
            
    ganhador = ganhadorDoJogo(grid_)#confere se o jogador ganhou, incrementando ao seu acumulo de possibilidades de vitoria
    if(ganhador!=0):            
        if(ganhador==1):
            global player1
            player1+=1
        else:
            global player2
            player2+=1
        return

    #muda jogador
    if cPlayer == 1:
        cPlayer = 2
    elif cPlayer == 2:
        cPlayer = 1 
    

    #testa para cada campo restante recursivamente   
    for row in range(len(grid_)):        
        for collumn in range(len(grid_[row])):
            if(grid_[row][collumn]==0):
                newGrid = copy.deepcopy(grid_)
                newGrid[row][collumn] = cPlayer
                permutate(newGrid,cPlayer)


def drawGrid(screen, game):
    rects = []

    rects = [screen.fill(GameConstants.BackgroundColor)]
    
    # Get the current game state
    gs = game.states[-1]
    grid = gs.grid
 
    # Draw the grid
    for row in range(GameConstants.gridHeight):
        for column in range(GameConstants.gridWidth):
            color = GameConstants.ColorWhite
            
            if grid[row][column] == 1:
                color = GameConstants.ColorRed
            elif grid[row][column] == 2:
                color = GameConstants.ColorBlue
            
            m = GameConstants.gridMarginSize
            w = GameConstants.gridCellWidth
            h = GameConstants.gridCellHeight
            rects += [pygame.draw.rect(screen, color, [(2*m+w) * column + m, (2*m+h) * row + m, w, h])]    
    
    return rects


def draw(screen, font, game):
    rects = []
            
    rects += drawGrid(screen, game)

    return rects


def initialize():
    random.seed(GameConstants.randomSeed)
    pygame.init()
    game = Game()
    font = pygame.font.SysFont('Courier', GameConstants.fontSize)
    fpsClock = pygame.time.Clock()

    # Create display surface
    screen = pygame.display.set_mode((GameConstants.screenWidth, GameConstants.screenHeight), pygame.DOUBLEBUF)
    screen.fill(GameConstants.BackgroundColor)
        
    return screen, font, game, fpsClock


def handleEvents(game):
    #gs = game.states[-1]    
    for event in pygame.event.get():
        global cX
        global cY
        pos = pygame.mouse.get_pos()  

        global player1
        global player2
        global cPlayer_
        gs = game.states[-1]

        global whoAmI

        #Atualizar
        #confere se mudou de quadrado (padrao do inicio do jogo é 0 0, canto superior esquerdo)
        if((cX != pos[0] // (GameConstants.screenWidth // GameConstants.gridWidth))or(cY != pos[1] // (GameConstants.screenHeight // GameConstants.gridHeight))):            
            cX = pos[0] // (GameConstants.screenWidth // GameConstants.gridWidth)
            cY = pos[1] // (GameConstants.screenHeight // GameConstants.gridHeight)
            grid = copy.deepcopy(gs.grid)#copia a grid do jogo atual
            player1=0
            player2=0
            if(grid[cY][cX]==0 and cY!=-1 and cX!=-1):#confere se a posição sendo verificada é válida
                jogador = copy.copy(cPlayer_)                
                grid[cY][cX] = jogador#atribui o jogador atual ao teste, considerando o quadrado que está em cima
                # permutate(grid,jogador)#chama a função recursiva
                
                # #calcula a chance e mostra de acordo com o atual jogador
                # if(cPlayer_==1):                    
                #     print("Chance do jogador 1 ganhar: {:.2f}%".format(100*player1/(player2+player1)))
                # else:
                #     print("Chance do jogador 2 ganhar: {:.2f}%".format(100*player2/(player2+player1)))
                        
        

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            
            col = pos[0] // (GameConstants.screenWidth // GameConstants.gridWidth)
            row = pos[1] // (GameConstants.screenHeight // GameConstants.gridHeight)            
            
            # send player action to game
            response = action(whoAmI,get_mac(),(row,col))
            if(response != 'invalid'):
                gs.grid = response
            # game.eventJournal.append((row, col))


        

            
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

            
def mainGamePlayer(iAm):
    ts = 0
    try:
        # Initialize pygame and etc.
        screen, font, game, fpsClock = initialize()
        game.currentPlayer = iAm
        # Main game loop
        while game.alive:
            # Handle events
            handleEvents(game)

            test = int(time())
            
            if(test>ts+3):
                gs = game.states[-1]
                gs.currentPlayer = iAm
                state = refreshGame()
                # grid = [
                #     [0,0,0],
                #     [0,0,0],
                #     [0,0,0],
                # ]
                grid = state['grid']
                current_player = state['current_player']
                gs.currentPlayer = current_player
                ts = test
                # gs.grid = state 
                # print(gs.grid)
                    
            # Update world
            game.update()
            
            # Draw this world frame
            rects = draw(screen, font, game)     
            pygame.display.update(rects)
            
            # Delay for required FPS
            fpsClock.tick(GameConstants.FPS)
            
        # close up shop
        pygame.quit()
    except SystemExit:
        pass
    except Exception as e:
        #print("Unexpected error:", sys.exc_info()[0])
        traceback.print_exc(file=sys.stdout)
        pygame.quit()
        #raise Exception from e
    
    

# mainGamePlayer(1)

def menu():
    print("Bem vindo ao Jogo Da Velha da Quarentena")
    print("Insira o IP do servidor")    
    
    # ip = input("IP: ")
    ip = '127.0.0.1'
        
    dest = (ip,PORT)

    try:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        tcp.connect(dest)
        
        command = {
            'command' : 'insert',
            'data':get_mac()
        }

        tcp.send(pickle.dumps(command))

        # tamp_resp = int.from_bytes(tcp.recv(4),'big')
        resp = pickle.loads(tcp.recv(1024))
        
        tcp.close()

        if(resp == 'unavailable'):
            print("Jogo indisponível")
            sys.exit()
        else:
            global whoAmI
            whoAmI = resp
            mainGamePlayer(whoAmI)

    except:
        print("Erro ao conectar ao servidor")



    
    

menu()