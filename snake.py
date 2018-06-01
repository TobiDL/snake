import pygame
import numpy as np
import os
from random import randint

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)

MARGIN = 1
WIDTH = 23
HEIGHT = 23

class Apple:

    def __init__(self):
        self.position =(randint(0,19), randint(0,19))

    def randomize(self):
        self.position =(randint(0,19), randint(0,19))

class Snake:

    def __init__(self):

        self.head = (randint(4,14), randint(4,14))
        self.body = [self.head]

        self.direction = 0

    def eat(self, tuple):
        self.body.insert(0, tuple)
        self.head = self.body[0]

    def move(self, tuple):
        self.body.insert(0, tuple)
        self.body = self.body[:-1]
        self.head = self.body[0]

class SnakeGame:

    def __init__(self):

        self.score = 0

        self.window_width = 482
        self.window_height = 500

        self.board = np.zeros((20,20), dtype = np.int8)

        self.snake = Snake()

        self.apple = Apple()

    def print_board(self):
        for line in self.board:
            conv = [str(x) for x in line]
            print(' '.join(conv))

    def update_board(self):

        self.board = np.zeros((20,20), dtype = np.int8)

        if len(set(self.snake.body)) != len(self.snake.body):
            self._running = False
            return
        elif self.snake.head[0] < 0 or self.snake.head[0] > 19 or self.snake.head[1] < 0 or self.snake.head[1] > 19:
            self._running = False
            return

        for pos in self.snake.body:

            x = pos[0]
            y = pos[1]

            if self.board[x][y] != 0:
                return False
            else:
                self.board[x][y] = 1

        x = self.apple.position[0]
        y = self.apple.position[1]
        
        if self.board[x][y] != 0:
                return False
        else:
            self.board[x][y] = 2

    def run_game(self):

        pygame.init()
        screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('Snake')

        font = pygame.font.SysFont("monospace", 15)
        font2 = pygame.font.SysFont("monospace", 80)


        clock = pygame.time.Clock()

        self._running = True
        ctr = 0

        while self._running:

            
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:  
                    self._running = False  
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w and self.snake.direction != 3:  
                        self.snake.direction = 0
                    if event.key == pygame.K_d and self.snake.direction != 2:  
                        self.snake.direction = 1
                    if event.key == pygame.K_a and self.snake.direction != 1:  
                        self.snake.direction = 2
                    if event.key == pygame.K_s and self.snake.direction != 0:  
                        self.snake.direction = 3

            #updates the board
            screen.fill(BLACK)
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

                    label = font.render("Score: "+str(self.score), 1, RED)
                    screen.blit(label, (10, 483))

            if ctr % 6 == 0:
                self.move()
            
            self.update_board()
            clock.tick(60)
            pygame.display.flip()
            ctr += 1
        
        end = font2.render("GAME OVER", 1, RED)
        screen.blit(end, (20, 200))
        pygame.display.flip()

        pygame.time.wait(1000)



    def move(self):
        #0 - up
        #1 - right
        #2 - left
        #3 - down

        if self.snake.direction == 0:
            x = self.snake.head[0]-1
            y = self.snake.head[1]

            if self.snake.head == self.apple.position:
                self.snake.eat((x,y))
                self.apple.randomize()
                self.score += 1
            else:
                self.snake.move((x,y))

        elif self.snake.direction == 1:
            x = self.snake.head[0]
            y = self.snake.head[1]+1
            
            if self.snake.head == self.apple.position:
                self.snake.eat((x,y))
                self.apple.randomize()
                self.score += 1
            else:
                self.snake.move((x,y))
        elif self.snake.direction == 2:
            x = self.snake.head[0]
            y = self.snake.head[1]-1

            if self.snake.head == self.apple.position:
                self.snake.eat((x,y))
                self.apple.randomize()
                self.score += 1
            else:
                self.snake.move((x,y))

        elif self.snake.direction == 3:
            x = self.snake.head[0]+1
            y = self.snake.head[1]

            if self.snake.head == self.apple.position:
                self.snake.eat((x,y))
                self.apple.randomize()
                self.score += 1
            else:
                self.snake.move((x,y))


game = SnakeGame()
game.run_game()