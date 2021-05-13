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

cPlayer_ = 1

import pygame
import copy
import sys
import traceback
import random
import numpy as np
import pickle
import socket

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

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
        currentPlayer = 0
    
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
        # Complete line?
        for i in range(3):
            s = set(gs.grid[i, :])
            if len(s) == 1 and min(s) != 0:
                return s.pop()
            
        # Complete column?
        for i in range(3):
            s = set(gs.grid[:, i])
            if len(s) == 1 and min(s) != 0:
                return s.pop()
            
        # Complete diagonal (main)?
        s = set([gs.grid[i, i] for i in range(3)])
        if len(s) == 1 and min(s) != 0:
            return s.pop()
        
        # Complete diagonal (opposite)?
        s = set([gs.grid[-i-1, i] for i in range(3)])
        if len(s) == 1 and min(s) != 0:
            return s.pop()
            
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
        
        
        # Switch player turn
        if gs.currentPlayer == 0:
            gs.currentPlayer = 1
        elif gs.currentPlayer == 1:
            gs.currentPlayer = 2
        elif gs.currentPlayer == 2:
            gs.currentPlayer = 1
            
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
        s = set(grid[i, :])
        if len(s) == 1 and min(s) != 0:
            return s.pop()
        
    # Complete column?
    for i in range(3):
        s = set(grid[:, i])
        if len(s) == 1 and min(s) != 0:
            return s.pop()
        
    # Complete diagonal (main)?
    s = set([grid[i, i] for i in range(3)])
    if len(s) == 1 and min(s) != 0:
        return s.pop()
    
    # Complete diagonal (opposite)?
    s = set([grid[-i-1, i] for i in range(3)])
    if len(s) == 1 and min(s) != 0:
        return s.pop()
        
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
        #Atualizar
        #confere se mudou de quadrado (padrao do inicio do jogo é 0 0, canto superior esquerdo)
        if((cX != pos[0] // (GameConstants.screenWidth // GameConstants.gridWidth))or(cY != pos[1] // (GameConstants.screenHeight // GameConstants.gridHeight))):            
            cX = pos[0] // (GameConstants.screenWidth // GameConstants.gridWidth)
            cY = pos[1] // (GameConstants.screenHeight // GameConstants.gridHeight)
            gs = game.states[-1]
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
            #print('clicked cell: {}, {}'.format(cellX, cellY))
            if cPlayer_ == 1:
                cPlayer_ = 2
            elif cPlayer_ == 2:
                cPlayer_ = 1
            # send player action to game
            game.eventJournal.append((row, col))
        

            
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

            
def mainGamePlayer():
    try:
        # Initialize pygame and etc.
        screen, font, game, fpsClock = initialize()
              
        # Main game loop
        while game.alive:
            # Handle events
            handleEvents(game)
                    
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
    
    

# mainGamePlayer()

def menu():
    print("Bem vindo ao Jogo Da Velha da Quarentena")
    print("Voce quer ser")
    print("1- Cliente (primeiro a jogar)")
    print("2- Servidor (segundo a jogar)")

    choice = ''
    while(not(choice in ['1','2'])):
        choice = input("Insira sua escolha: ")

    if(choice=='1'):

        pass
    else:

        pass

menu()