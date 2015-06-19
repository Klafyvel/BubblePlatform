import pygame
from pygame.locals import *



class Block:

    """A block in the game."""

    def __init__(self, pos):
        self.x, self.y = pos
