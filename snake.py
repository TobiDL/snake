import pygame
import numpy as np
import os
from random import randint

from neural_net import Snake_nn

#Preset colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
BLUE = (0,0,255)

BOARD_SIZE = 10

MARGIN = 1
WIDTH = 25
HEIGHT = 25


WINDOW_WIDTH = BOARD_SIZE * 25 + BOARD_SIZE
WINDOW_HEIGHT = BOARD_SIZE * 25 + BOARD_SIZE + 20

class Snake:

    def __init__(self):

        self.head = (randint(4,BOARD_SIZE- 5), (randint(4,BOARD_SIZE- 5)))
        self.body = [self.head]

        #direction the snake is facing
        self.direction = 0

    #use when head is on top of apple
    def eat(self, tuple):
        self.body.insert(0, tuple)
        self.head = self.body[0]

    #use for regular movement
    def move(self, tuple):
        self.body.insert(0, tuple)
        self.body = self.body[:-1]
        self.head = self.body[0]

class SnakeGame:

    def __init__(self, training = True, load = True):

        self.score = 0

        self.board = np.zeros((BOARD_SIZE,BOARD_SIZE), dtype = np.int8)
        self.prev_board = None

        self.snake = Snake()
        self.apple = (randint(0,BOARD_SIZE-1), randint(0,BOARD_SIZE-1))

        #If true, nn will be disabled and the user can train the snake manually
        self.training = training
        self.features = None


        if self.training:
            self.data = []
        else:
            self.nn = Snake_nn(load = load)

    #Places the apple in an empty board space
    def place_apple(self):

        self.apple = (randint(0,BOARD_SIZE-1), randint(0,BOARD_SIZE-1))

        while self.apple in self.snake.body:
            self.apple = (randint(0,BOARD_SIZE-1), randint(0,BOARD_SIZE-1))

        if self.training:
            self.save_data()
    
    #prints the board state on the console   
    def print_board(self):
        for line in self.board:
            conv = [str(x) for x in line]
            print(' '.join(conv))
    
    #Collects features to train or predict
    def get_features(self):
            
            input_nodes = [0 for _ in range(13)]

            x,y = self.snake.head
            a,b = self.apple

            if x == 0 or self.board[x-1][y] == 1:
                input_nodes[0] = 1

            if y == BOARD_SIZE-1 or self.board[x][y+1] == 1:
                input_nodes[1] = 1

            if y == 0 or self.board[x][y-1] == 1:
                input_nodes[2] = 1

            if x == BOARD_SIZE-1 or self.board[x+1][y] == 1:
                input_nodes[3] = 1

            if a < x:
                input_nodes[4] = 1

            if b > y:
                input_nodes[5] = 1

            if b < y:
                input_nodes[6] = 1

            if a > x:
                input_nodes[7] = 1

            input_nodes[8] = abs(x-a) + abs(y-b)
            
            input_nodes[9 + self.snake.direction] = 1

            self.features = input_nodes

    #Appends features to temporary cache
    def record_data(self):

            output = ['0','0','0','0']
            output[self.snake.direction] = '1'

            data = ','.join([str(x) for x in self.features]) + ',' + ','.join(output)+'\n'

            self.data.append(data)
          
    #Appends features stored in cache into data folder  
    def save_data(self):

        with open('data/snake_data.txt', 'a') as file:
            for x in self.data:
                file.write(x)
        self.data = []

    #Update board matrix and checks for colision
    def update_board(self):

        self.board = np.zeros((BOARD_SIZE,BOARD_SIZE), dtype = np.int8)

        if len(set(self.snake.body)) != len(self.snake.body):
            self._running = False
            return
        elif self.snake.head[0] < 0 or self.snake.head[0] > BOARD_SIZE-1 or self.snake.head[1] < 0 or self.snake.head[1] > BOARD_SIZE-1:
            self._running = False
            return

        for pos in self.snake.body:
            x = pos[0]
            y = pos[1]
            

            if pos == self.snake.head:
                self.board[x][y] = 3
            elif self.board[x][y] != 0:
                return False
            else:
                self.board[x][y] = 1

        x = self.apple[0]
        y = self.apple[1]
        
        if self.board[x][y] != 0:
                return False
        else:
            self.board[x][y] = 2

    #Main loop
    def run_game(self):

        pygame.init()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Snake')

        #score font
        font = pygame.font.SysFont("monospace", 20)
        #game over font
        font2 = pygame.font.SysFont("monospace", 4*BOARD_SIZE + 5)

        clock = pygame.time.Clock()

        self._running = True
        ctr = 0
        n = True

        next_dir = 0

        while self._running:


            event = pygame.event.poll()
            if event.type == pygame.QUIT:  
                self._running = False  
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and self.snake.direction != 3:  
                    next_dir = 0
                if event.key == pygame.K_d and self.snake.direction != 2:  
                    next_dir = 1
                if event.key == pygame.K_a and self.snake.direction != 1:  
                    next_dir = 2
                if event.key == pygame.K_s and self.snake.direction != 0:  
                    next_dir = 3

            if n and not self.training:
                
                self.get_features()

                next_dir = self.nn.predict_direction(np.array([self.features]))
                n = False

            #updates the board
            screen.fill(BLACK)
            for row in range(BOARD_SIZE):
                for column in range(BOARD_SIZE):

                    tile = self.board[row][column]
                    if tile == 0:
                        color = WHITE
                    if tile == 1 or tile == 3:
                        color = BLUE
                    if tile == 2:
                        color = RED

                    pygame.draw.rect( screen, color, 
                                     ((MARGIN + WIDTH) * column + MARGIN,
                                      (MARGIN + HEIGHT) * row + MARGIN,
                                      WIDTH,
                                      HEIGHT))

                    label = font.render("Score: "+str(self.score), 1, RED)
                    screen.blit(label, (10, WINDOW_WIDTH))

            #dictates game speed
            if ctr % 10 == 0:
                self.snake.direction = next_dir
                self.move()
                self.update_board()
                

                if self.training:
                    self.get_features()
                    self.record_data()
                
                n = True

            clock.tick(60)
            pygame.display.flip()
            ctr += 1
        
        end = font2.render("GAME OVER", 1, RED)
        screen.blit(end, (BOARD_SIZE, 10*BOARD_SIZE))
        pygame.display.flip()

        pygame.time.wait(1000)

    #Moves the snake to the direction its facing
    def move(self):
        #0 - up
        #1 - right
        #2 - left
        #3 - down

        if self.snake.direction == 0:
            x = self.snake.head[0]-1
            y = self.snake.head[1]

            if (x,y) == self.apple:
                self.snake.eat((x,y))
                self.place_apple()
                self.score += 1
            else:
                self.snake.move((x,y))

        elif self.snake.direction == 1:
            x = self.snake.head[0]
            y = self.snake.head[1]+1
            
            if (x,y) == self.apple:
                self.snake.eat((x,y))
                self.place_apple()
                self.score += 1
            else:
                self.snake.move((x,y))
        elif self.snake.direction == 2:
            x = self.snake.head[0]
            y = self.snake.head[1]-1

            if (x,y) == self.apple:
                self.snake.eat((x,y))
                self.place_apple()
                self.score += 1
            else:
                self.snake.move((x,y))

        elif self.snake.direction == 3:
            x = self.snake.head[0]+1
            y = self.snake.head[1]

            if (x,y) == self.apple:
                self.snake.eat((x,y))
                self.place_apple()
                self.score += 1
            else:
                self.snake.move((x,y))
