import pygame
from pygame.locals import *

from sprites import SpriteSheet, Animation, TimedAnimation


class CollideDirection:
    def __init__(self, **kwargs):
        """args :
            - top : bool
            - bottom : bool
            - left : bool
            - right : bool
        """
        self.left = kwargs.get("left", False)
        self.right = kwargs.get("right", False)
        self.top = kwargs.get("top", False)
        self.bottom = kwargs.get("bottom", True)

class Character:

    """A character in the game."""


    MOTIONLESS = 0
    RUNNING = 2
    JUMPING = 4
    FALLING = 6
    SHOOTING = 8
    BYE = 10
    DEAD = 12

    LEFT = 0
    RIGHT = 1

    X_DISPLACEMENT = 15
    Y_DISPLACEMENT = 2

    Y_SPEED = -15

    def __init__(self, pos):
        self.x, self.y = pos
        self.image = pygame.Surface((0, 0))

        self.v_y = 0

        self.collide = CollideDirection()

    def on_render(self, dst):
        dst.blit(self.image)

    def move_right(self):
        self.x += self.X_DISPLACEMENT

    def move_left(self):
        self.x -= self.X_DISPLACEMENT

    def jump(self):
        if self.collide.bottom:
            self.v_y = self.Y_SPEED

    def gravity(self):
        if not self.collide.bottom:
            self.y += self.v_y
            self.v_y += self.Y_DISPLACEMENT

    def on_update(self):
        self.gravity()


class Player(Character):

    """The main character."""

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
        self.anims[self.direction + self.movement].stop()
        self.movement = mov
        self.direction = dir
    def change_direction(self, dir):
        if dir is not self.direction:
            self.change_anim(self.movement, dir)

    def on_update(self):
        super(Player, self).on_update()
        if self.movement == self.RUNNING:
            if self.direction == self.RIGHT:
                self.move_right()
            else:
                self.move_left()
        if self.v_y > 0:
            self.movement = self.FALLING

    def change_movement(self, mov):
        if mov is not self.movement:
            self.change_anim(mov, self.direction)

    def jump(self):
        super(Player, self).jump()
        self.change_movement(self.RUNNING)
        self.collide.bottom = False

    def on_render(self, dst):
        dst.blit(self.anims[self.direction + self.movement].next(), (self.x, self.y))

    def get_mask(self):
        s = self.anims[self.direction + self.movement].current()
        return pygame.mask.from_surface(s)
