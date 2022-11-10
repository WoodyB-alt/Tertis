from turtle import width
import pygame
import Tetris_ai
from copy import deepcopy
from random import choice, randrange


W, H = 10, 20
Tile = 35
Game_res = [W * Tile, H * Tile]
res = 750, 750
FPS = 60

pygame.init()
win = pygame.display.set_mode(res)
game_sc = pygame.Surface(Game_res)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * Tile, y * Tile, Tile, Tile) for x in range(W) for y in range(H)]

# Figures are render via coordinates in a grid
figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]


figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, Tile - 2, Tile - 2)
field = [[0 for i in range(W)] for j in range(H)]
anim_count, anim_speed, anim_limit = 0, 20, 2000
figure = deepcopy(choice(figures))


bg = pygame.image.load('bg.png').convert()
game_bg = pygame.image.load('bg.png').convert()


def get_colour():
    '''Generate random colour values for figures'''
    return (randrange(30, 256), randrange(30, 256), randrange(30, 256))


# Figures and fonts
figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
colour, next_colour = get_colour(), get_colour()

main_font = pygame.font.SysFont('ttf', 105, bold=True,)
font = pygame.font.SysFont('tahoma', 35, bold=True)

title_tetris = main_font.render('TERTIS', True, pygame.Color('yellow'))
title_nextShape = font.render('Next Shape:', True, pygame.Color('green'))
title_score = font.render('Score:', True, pygame.Color('green'))
title_HighScore = font.render('Highscore:', True, pygame.Color('green'))


# Score
''' variable for scroe and lines
and dictionary for accrual points by the number of collected lines'''
score, line = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}


def game_borders():
    '''Return a false value when the figure has reached the bottom
    and if another figure is already in the feild'''
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H-1 or field[figure[i].y][figure[i].x]:
        return False
    return True


def get_Highscore():
    try:
        with open('Highscore') as f:
            return f.readline()
    except FileNotFoundError:
        with open('Highscore', 'w') as f:
            f.write('0')


def set_Highscore(Highscore, score):
    HS = max(int(Highscore), score)
    with open('Highscore', 'w') as f:
        f.write(str(HS))


while True:
    Highscore = get_Highscore()
    dx, rotate = 0, False

    # Place backgrounds and grid
    win.blit(bg, (0, 0))
    win.blit(game_sc, (10, 50))
    game_sc.blit(game_bg, (0, 0))

    # Animate full line removal
    for i in range(line):
        pygame.time.wait(200)

    # Controls
    for event in list(pygame.event.get()):
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_UP:
                rotate = True
            elif event.key == pygame.K_SPACE:
                anim_limit = 10

    # Move x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not game_borders():
            figure = deepcopy(figure_old)
            break

    # Move y
    '''move y by using a counter that increases by the value
    of the animation speed and when the limit is reached we increase the y coordinate by 1'''
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1

            if not game_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = colour
                figure, colour = next_figure, next_colour
                next_figure, next_colour = deepcopy(choice(figures)), get_colour()
                anim_limit = 2000
                break

    # Rotate
    '''Center of rotation, rotate figure by 90 degrees this is done by
    calculating the difference between the coordinates of the  figure and
    the center of rotation and adding the differeance to the x coordinate'''
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not game_borders():
                figure = deepcopy(figure_old)
                break

    # Check and tally lines
    '''for each line collected, add to score depending on accruled lines
    for each line collected increase speed by 3'''
    line, lines = H-1, 0
    for row in range(H-1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
        else:
            anim_speed += 3
            lines += 1

    # Tally and blit score
    score += scores[lines]
    win.blit(title_score, (490, 480))
    win.blit(font.render(str(score), True, pygame.Color('yellow')), (525, 525))

    # Draw grid
    [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]

    # Draw figure by iterating through the coordinates and multiplying the x and y by the tile
    for i in range(4):
        figure_rect.x = figure[i].x * Tile
        figure_rect.y = figure[i].y * Tile
        pygame.draw.rect(game_sc, colour, figure_rect)

    # Draw next figure
    for i in range(4):
        figure_rect.x = next_figure[i].x * Tile + 380
        figure_rect.y = next_figure[i].y * Tile + 185
        pygame.draw.rect(win, next_colour, figure_rect)

    # Draw feild
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * Tile, y * Tile
                pygame.draw.rect(game_sc, col, figure_rect)
    win.blit(title_nextShape, (445, 130))

    # Titles
    win.blit(title_tetris, (405, 15))
    win.blit(title_HighScore, (455, 585))
    win.blit(font.render(Highscore, True, pygame.Color('yellow')), (525, 625))

    # GAME OVER
    for i in range(W):
        if field[0][i]:
            set_Highscore(Highscore, score)
            field = [[0 for i in range(W)] for i in range(H)]
            anim_count, anim_speed, anim_limit = 0, 20, 2000
            score = 0
            for i_rect in grid:
                pygame.draw.rect(game_sc, get_colour(), i_rect)
                win.blit(game_sc, (10, 50))
                pygame.display.flip()
                clock.tick(2000)

    pygame.display.flip()
    clock.tick()
