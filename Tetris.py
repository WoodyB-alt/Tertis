from tkinter import Grid
from turtle import position
from playsound import playsound 
import pygame
import random

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

# playsound ('') #grab tetris song!!!!

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2 # represents the top left postion of play area, for collision  
top_left_y = s_height - play_height


# SHAPE FORMATS -- shapes and there positions/ rotations 

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape

# represents diffrent peices 
class Piece(object):
    def __init__(self, x, y, shape): 
        self.x =x 
        self.y =y 
        self.shape = shape 
        self.color = shape_colors[shapes.index(shape)] #referances colour index list 
        self.rotation = 0  #will represent pressing up key to add one to scroll through postion of peices in shape index 
#slef.rotation from number 0-3 

#creating grid multidimensional list that contains 20 lists of 10 elements (rows and columns).
#Each element in the lists will be a tuple representing the color of the peice in that current postion
#locked position parameter to contain a dictionary of key value pairs where each key is a postion of a peice 
#that has already fallen and each value is its color, set to loop through locked postuins and modify blank grid to show places
def create_grid(locked_positions={}):  

    grid = [[(0,0,0)for x in range(10)] for x in range (20)] #create list for every row in the grid 20 rows 10 colours 10 squares each row 
    
    for i in range(len(grid)): 
        for j in range(len(grid[i])):  
          if (j, i) in locked_positions: #j is our x value and j is our y value |
             c = locked_positions[(j, i)]
             grid[i][j] = c
    return grid 

#translates multidimential list into shape format by converting list into postutuins we can return
#convert_shape_format() will do this
def convert_shape_format(shape):
    positions =[]
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, colum in enumerate(row):
            if colum == '0':
                position.append((shape.x + j, shape.y +i))
    
    for i, pos in enumerate(positions):
        position[i] = (pos[0] -2, pos[1] - 4)
    return positions

#two parameters: grid and shape. check the grid to ensure that the current position we're trying to move into is not occupied.
#by seeing if any of the positions in the grid that the shape is attempting to move into have a color
def valid_space(shape, grid):

    accepted_positions = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_positions = [j for sub in accepted_positions for j in sub]
    formatted = convert_shape_format(shape)
 
    for pos in formatted:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
 
    return True

#check if any position in the given list is above the screen.
# if reached the top and therefore lost the game.
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

#generating random shape
def get_shape():
    global shapes, shape_colors

    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(text, size, color, surface):  
    pass


def draw_grid(surface, row, col):
# This function draws the grey grid lines that we see
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + play_width, sy + i * 30))  # horizontal lines
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))  # vertical lines
    

def clear_rows(grid, locked):
   # need to see if row is clear the shift every other row above down one

    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            # add positions to remove from locked
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

# display the next falling shape on the right side of the screen.
def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*30, 30, 30), 0)

    surface.blit(label, (sx + 10, sy- 30))

#call function to draw all objects to the screen. 
#The font module allows for rendering TrueType fonts into a new Surface object. 
#pygame.font.SysFont = create a Font object from the system fonts
#surface.blit = draw one image onto another
#pygame.draw.rect= draw a rectangle
def draw_window(surface):
    surface.fill((0, 0, 0)) 
   
   #creating and drawing label 
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render("Tetris", 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width/2 - (label.get.width()/2), 30))
    
    #drawing grid objects onto page surface-grid and postion of grid 
    for i in range(len(grid)) :
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y+ i*block_size, block_size, block_size ), 0)
   
    # draw grid and border
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (255,0,0), (top_left_x, top_left_y, play_width, play_height), 5)
    #update screen
    pygame.display.update()

# game loop = This is what will be running constantly and checking to see if events occur.
# define variables then move into the while loop and check for press events 
#when user presses the up arrow key the piece will rotate.(done by inceasing shape rotation attribute to next shape)
#left and right keys will be movment of our peice by chaning the x value of the peice
#down arrow to increase speed for shape falling 
def main():
    global grid 

    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)
    change_piece = False 
    run = True 
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0 

    while run: 
        fall_speed = 0.27
        
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()
         
        if fall_time/1000 >= fall_speed:
         fall_time = 0
         current_piece.y += 1
         if not (valid_space(current_piece, grid)) and current_piece.y > 0:
             current_piece.y -= 1
             change_piece = True

        for event in pygame.event.get(): 
            run = False 
            pygame.display.quit()
            quit()

        if event.type == pygame.KEYDOWN:
           if event.key == pygame.Quit: 
              run = False 
              pygame.display.quit()
              quit()
            
        elif event.key == pygame.K_RIGHT:
            current_piece.x += 1

            if not valid_space(current_piece, grid):
                current_piece.x -=1 

            elif event.key == pygame.K_UP: 
                # rotate shape
                current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)

                if not valid_space(current_piece, grid):
                    current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)

                if event.key == pygame.K_DOWN:
                    #move shape down
                    current_piece.y += 1 
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1 
                    draw_next_shape(next_piece, win)
                    pygame.display.update()
        
        shape_pos = convert_shape_format(current_piece)

        # add color of piece to the grid for drawing
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1: # If we are not above the screen
                grid[y][x] = current_piece.color
       # IF PIECE HIT GROUND
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False


    draw_window(win)

    # Check if user lost
    if check_lost(locked_positions):
      run = False

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption(' Tetris ')

def main_menu():
    pass

main_menu()  # start game

main()
