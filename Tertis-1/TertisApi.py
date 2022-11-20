"""
Tertis API

Expose a API for controlling the Tertis program.
"""
import pygame
import game

class TertisApi:
    """Expose api functions for controlling Tertis."""

    def __init__(self):
        """Initialize a Tertis Api object."""
        pygame.init()
        win = pygame.display.set_mode(game.res)
        game_sc = pygame.Surface(game.Game_res)
        clock = pygame.time.Clock()

    def startGame(self):
        """Start a new Tertis game."""
        open.game.py