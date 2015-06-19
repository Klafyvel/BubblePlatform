import pygame
from pygame.locals import *

class Character:

    """A character in the game."""

    def __init__(self, pos):
        self.x, self.y = pos
        self.image = pygame.Surface((0,0))

    def on_render(self, dst):
        dst.blit(self.image)

class Player(Character):

    """The main character."""

    MOTIONLESS = 0
    RUNNING = 2
    JUMPING = 4
    SHOOTING = 6
    BYE = 8
    DEAD = 9

    LEFT = 0
    RIGHT = 1

    def __init__(self, pos):
        Character.__init__(self, pos)
        self.sprite_sheet = pygame.image.load('main_char.png').convert_alpha()

        self.direction = self.RIGHT
        self.movement = self.MOTIONLESS
        self.anim_state = 0

    def on_render(self, dst):
        rect = pygame.Rect((self.anim_state*32, (self.direction+self.movement)*32, 32, 32))
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sprite_sheet, (0, 0), rect)
        image.convert_alpha()
        dst.blit(image, (self.x, self.y))
        self.anim_state += 1
        self.anim_state %= 7