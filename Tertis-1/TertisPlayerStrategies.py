"""
TERTIS Player strategies library
"""
import pygame

class TertisPlayerStrategy:
    """Base interface for a Tertis player startegy."""
    pass


class StraightDown(TertisPlayerStrategy):
    """Implement a 'straight down' Tertis player strategy."""
    counter = 0
    def straightdown(feild, figures, W, H):
        global counter
        counter += 1
        if counter < 3:
            return[]
        counter = 0
        e = pygame.KEYDOWN, pygame.K_SPACE
        return [e]