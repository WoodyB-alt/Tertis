"""
TERTIS Player strategies library
"""
import game
import pygame

class TertisPlayerStrategy:
    """Base interface for a Tertis player startegy."""
    pass


class StraightDown(TertisPlayerStrategy):

    counter = 0
    def Simulate_down_Keypress():
        global counter
        counter += 1
        if counter < 3:
            return[]
        counter = 0
        if game.figures != game.rotation:
            e = pygame.KEYDOWN, pygame.K_SPACE
        return[e]
