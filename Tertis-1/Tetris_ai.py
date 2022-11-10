import pygame


class event():
    type = None
    key = None

    def __init__(self, type, key):
        self.type = type
        self.key = key



counter = 0
def run_ai(feild, figures, W, H):
    global counter
    counter += 1
    if counter < 3:
        return[]
    counter = 0
    rotation, position = best_rotation_position(feild, figures, W, H)
    if figures != rotation:
        e = event(pygame.KEYDOWN, pygame.K_UP)
    elif figures.x < position:
        e = event(pygame.KEYDOWN, pygame.K_RIGHT)
    elif figures.x > position:
        e = event(pygame.KEYDOWN, pygame.K_LEFT)
    else:
        e = event(pygame.KEYDOWN, pygame.K_SPACE)
    return[e]


def intersects (figures, H, W, GAME_res, x, y):
    intersection = False
    for i in range(4):
        for j in range(4):
            if i * 4 + j in figures:
                if i + y > H -1 or \
                    j + x > W - 1 or \
                    j + x < 0 or \
                    GAME_res[i + y][j + x] < 0:
                 intersection = True
    return intersection

def simulate(feild, x, y, W, H, figures):
    while not intersects(feild, x, y, H, W, figures):
        y += 1
    y -= 1

    height = H
    holes = 0
    filled = []
    for i in range(H - 1, -1, -1):
        for j in range(H):
            u = '_'
            if feild[i][j] !=0:
                u = "x"
            for ii in range(4):
                for jj in range(4):
                    if ii * 4 + jj in figures:
                        if jj + x == j and ii + y == i:
                            u = "x"

            if u == "x" and i < height:
                height = i
            if u == "x":
                filled.append((i,j))
                for k in range(i, H):
                    if (k, j) not in filled:
                        holes += 1
                        filled.append((k, j))

    return holes

def best_rotation_position(feild, figures, W, H):
    best_height = H
    best_holes = H * W
    best_rotation = None
    best_position = None

    for rotation in range(len([figures])):
        fig = figures[rotation]
        for j in range(-3, W):
            if not intersects(
                    feild,
                    j,
                    0,
                    W,
                    H,
                    fig):
                holes, Height = simulate(
                    feild,
                    j,
                    0,
                    W,
                    H,
                    fig
                )
                if best_position is None or best_holes > holes or \
                    best_holes == holes and best_height > Height:
                    best_height = Height
                    best_holes = holes
                    best_position = j
                    best_rotation = rotation
    return best_rotation, best_rotation