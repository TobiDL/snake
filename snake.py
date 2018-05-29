import pygame
import numpy as np
import os
from random import randint

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)

MARGIN = 4
WIDTH = 26
HEIGHT = 26

class Snake:

    def __init__(self):

        self.window_width = 604
        self.window_height = 604

        self.board = np.zeros((20,20), dtype = np.int8)

        self.head_pos = (randint(4,14), randint(4,14))
        self.snake = [self.head_pos]

        self.apple = (randint(0,19), randint(0,19))

    def display_board(self):
        for line in self.board:
            conv = [str(x) for x in line]
            print(' '.join(conv))

    def draw_board(self):

        self.board = np.zeros((20,20), dtype = np.int8)

        for pos in self.snake:
            x = pos[0]
            y = pos[1]

            if self.board[x][y] != 0:
                return False
            else:
                self.board[x][y] = 1

        x = self.apple[0]
        y = self.apple[1]
        
        if self.board[x][y] != 0:
                return False
        else:
            self.board[x][y] = 2

    def init_game(self):

        pygame.init()
        screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Snake')
        clock = pygame.time.Clock()

        self._running = True

        while self._running:
            
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:  
                    self._running = False  

            for row in range(20):
                for column in range(20):

                    tile = self.board[row][column]
                    if tile == 0:
                        color = WHITE
                    if tile == 1:
                        color = BLUE
                    if tile == 2:
                        color = RED
                    pygame.draw.rect( screen, color, 
                                     ((MARGIN + WIDTH) * column + MARGIN,
                                      (MARGIN + HEIGHT) * row + MARGIN,
                                      WIDTH,
                                      HEIGHT))
            clock.tick(60)
            pygame.display.flip()


    def move(self, direction):
        #0 - up
        #1 - right
        #2 - left
        #3 - down
        pass



snake = Snake()
snake.draw_board()
snake.display_board()
snake.init_game()