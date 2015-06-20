import pygame
from pygame.locals import *

from sprites import SpriteSheet, Animation, TimedAnimation


class Character:

    """A character in the game."""

    def __init__(self, pos):
        self.x, self.y = pos
        self.image = pygame.Surface((0, 0))

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
        sprite_sheet = SpriteSheet('main_char.png')

        self.direction = self.RIGHT
        self.movement = self.MOTIONLESS

        self.anims = (
            Animation(sprite_sheet.images_at((0, 0, 32, 32), 1)),
            Animation(sprite_sheet.images_at((0, 32, 32, 32), 1)),
            TimedAnimation(sprite_sheet.images_at((0, 64, 32, 32), 7), 50),
            TimedAnimation(sprite_sheet.images_at((0, 96, 32, 32), 7), 50),
            Animation(sprite_sheet.images_at((0, 128, 32, 32), 4)),
            Animation(sprite_sheet.images_at((0, 160, 32, 32), 4)),
            Animation(sprite_sheet.images_at((0, 192, 32, 32), 1)),
            Animation(sprite_sheet.images_at((0, 224, 32, 32), 1)),
            Animation(sprite_sheet.images_at((0, 256, 32, 32), 1)),
            Animation(sprite_sheet.images_at((0, 288, 32, 32), 1)),
            TimedAnimation(sprite_sheet.images_at((0, 320, 32, 32), 2), 1000),
            TimedAnimation(sprite_sheet.images_at((0, 352, 32, 32), 2), 1000),
        )
    def change_anim(self, mov, dir):
        self.anims[self.direction + self.movement].current = 0
        self.movement = mov
        self.direction = dir
    def change_direction(self, dir):
        self.change_anim(self.movement, dir)

    def change_movement(self, mov):
        self.change_anim(mov, self.direction)

    def on_render(self, dst):
        dst.blit(self.anims[self.direction + self.movement].next(), (self.x, self.y))
