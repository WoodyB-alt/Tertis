import random
import pygame 

#colours of the blocks stored in list 
shapeColors = [ (0, 255, 0), 
 (255, 0, 0), 
 (0, 255, 255),
 (255, 255, 0),
 (255, 165, 0), 
 (0, 0, 255), 
 (128, 0, 128) 
 ]

'''
==Shapes of the blocks ==
the shapes variable holds the matrix that contains information about the shape of the block. 
Assume a 4×4 block and give each cell indices as shown below

0	1	2	3
4	5	6	7
8	9	10	11
12	13	14	15
Using init to construct the objects
randomly pick a type and a color.
get current rotation and rotate 
'''

class shape: 
 x = 0
 y = 0

 shapes = [#I shape
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        #Z
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        #L 
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        #other L
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        #T shape
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        #Square
        [[1, 2, 5, 6]],
 ]
 def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.shapes) -1)
        self.color = random.randint(1, len(shapeColors) -1)
        self.rotation = 0 
    
 def image(self):
     return self.shapes[self.type][self.rotation]

 def rotate(self): 
     self.rotation = (self.rotation + 1) % len(self.shapes[self.type])

'''
tetris class:
1)game variables
state for if we are playing or not 
feild is feild of game 
contains zeros where it is empty 
and contains colors where there are shapes (except ones that is still comming down)

2)initalise the game that creates a feild with a size height x width

3)create a new figure and postion it at coordinates in middle (3,0)

4)check if figure is intersecting with somthing fixed on the feild
could happen when shape is moving in any direction or roatating
done by checking each cell in the 4x4 matrix of the current Figure
whether it is out of game bounds and whether it is touching some busy feild
check self.feild as there may be color 
if theres 0 it means feild is empty so its fine to move 
checked with self.shape[..] [..] > 0 , 

5) freeze class will define if a block moves down and intersets with another piece
this will stop object in place 

6) breaklines will check feild from bottom to top to look for full lines and remove them
!!!!come back to write more about breaklines as youre lost with this function!!!!!

7) move function (self explanitory)
'''

class Tertis:
 level = 2
 score = 0 
 state = "start"
 field = []
 height = 0 
 width = 0 
 zoom = 20 
 x = 100 
 y = 60 
 shape = None
 
 def __init__(self, height, width):
     self.height = height
     self.width = width
     self.field = []
     self.score = 0
     self.state = "start"
     for i in range(height):
         new_line = []
         for j in range(width):
             new_line.append(0)
         self.field.append(new_line)

 def new_shape(self):
     self.shape = shape(3, 0)
 
 def intersects(self):
     intersection = False
     for i in range(4):
         for j in range(4):
             if i * 4 + j in self.shape.image():
                 if i + self.shape.y > self.height - 1 or \
                     j + self.shape.x > self.width - 1 or \
                     j + self.shape.x < 0 or \
                     self.field[i + self.shape.y][j + self.shape.x] > 0:
                    intersection = True
     return intersection
     
 def break_lines(self):
     lines = 0 
     for i in range(1, self.height):
         zeros = 0
         for j in range(self.width):
             if self.field[i][j] == 0:
                 zeros += 1
         if zeros == 0:
             lines += 1
             for i1 in range (i, 1, -1):
                 for j in range(self.width):
                     self.field[i1][j] = self.field[i1 -1][j]
     self.score += lines ** 2

 def go_space(self):
     while not self.intersects():
         self.shape.y += 1
     self.shape.y -= 1 
     self.freeze()
 
 def go_down(self):
     self.shape.y += 1
     if self.intersects():
         self.shape.y -= 1 
         self.freeze()

 def freeze(self):
     for i in range(4): 
         for j in range(4):
             if i * 4 + j in self.shape.image():
                 self.field[i + self.shape.y][j + self.shape.x] = self.shape.color
     self.break_lines()
     self.new_shape()
     if self.intersects():
         self.state= "GAMEOVER"

 def go_side(self, dx):
     old_x = self.shape.x
     self.shape.x += dx
     if self.intersects():
         self.shape.x = old_x
 
 def rotate(self):
     old_rotation = self.shape.rotation
     self.shape.rotate()
     if self.intersects():
         self.shape.rotation = old_rotation

#initalize pygame engine 
pygame.init()

#define colours 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size =(800, 800)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("TERTIS")

#Loop until the user clicks the close button 
done = False
clock = pygame.time.Clock()
fps = 25 
game = Tertis(20, 10)
counter = 0 

pressing_down = False 

while not done: 
    if game.shape is None:
        game.new_shape()
    counter += 1 
    if counter > 100000: 
        counter = 0
    
    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
             game.go_down()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.rotate()
            if event.key == pygame.K_DOWN:
                pressing_down = True 
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)

    if event.type == pygame.KEYUP: 
        if event.key == pygame.K_DOWN:
            pressing_down = False
    
    screen.fill(BLACK)

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, shapeColors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.shape is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.shape.image():
                    pygame.draw.rect(screen, shapeColors[game.shape.color],
                                     [game.x + game.zoom * (j + game.shape.x) + 1,
                                      game.y + game.zoom * (i + game.shape.y) + 1,
                                      game.zoom - 2, game.zoom - 2])
   
   #render text 
    font = pygame.font.SysFont('comicsans', 25, True, False)
    font1 = pygame.font.SysFont('comicsans', 65, True, False)
    text = font.render("Score: " + str(game.score), True, WHITE)
    text_game_over = font1.render("GAME OVER", True, (255, 125,0))
    text_game_over1 = font1.render("Press ESC", True, (255, 125,0))
   
    screen.blit(text, [0, 0])
    if game.state == "gameover":
         screen.blit(text_game_over, [20, 200])
         screen.blit(text_game_over1, [25, 265])
    
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()