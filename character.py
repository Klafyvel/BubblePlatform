import pygame
from pygame.locals import *

from sprites import SpriteSheet, Animation, TimedAnimation
from block import Block, get_equivalent_block_pos, test_in_rect

class CollideDirection:
    def __init__(self, **kwargs):
        """args :
            - top : bool
            - bottom : bool
            - left : bool
            - right : bool
            - center : bool
        """
        self.left = kwargs.get("left", None)
        self.right = kwargs.get("right", None)
        self.top = kwargs.get("top", None)
        self.bottom = kwargs.get("bottom", None)
        self.center = kwargs.get("center", None)

    def __str__(self):
        return "Collide : left {} \t right {} \t top {} \t bottom {}".format(self.left, self.right, self.top, self.center)

class Collider:

    def __init__(self, app):
        self.app = app

    def collides(self):
        for o in self.app.objects:
            self.collide(o)

    def collide(self, o):
        x_o,y_o = o.rect.x, o.rect.y
        w_o, h_o= o.rect.w, o.rect.h
        pos_to_be_tested = [(x,y) if not test_in_rect((x_o,y_o,w_o,h_o), (x,y)) else None for x in range(x_o - 2, x_o + w_o + 2) for y in range(y_o-2, y_o + h_o + 2)]

        c = {"left":None,"right":None,"top":None,"bottom":None, "center":None}
        for p in pos_to_be_tested:
            if not p:
                continue
            b = self.app.middleground.get(get_equivalent_block_pos(p), None)
            if not b:
                continue
            k = "left"
            if p[1] <= y_o:
                k = "top"
            elif p[0] > x_o:
                k = "right"
            elif p[1] > y_o:
                k = "bottom"
            c[k] = (pygame.sprite.collide_mask(b, o), b)
        o.collide = CollideDirection(**c)

class Character(pygame.sprite.Sprite):

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
    Y_DISPLACEMENT = 5

    Y_SPEED = -20

    Y_SPEED_MAX = -30

    def __init__(self, pos, collider):
        self.image = pygame.Surface((0, 0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

        self.v_y = 0

        self.direction = self.RIGHT
        self.movement = self.MOTIONLESS

        self.collider = collider
        self.collide = CollideDirection()

    def on_render(self, dst):
        dst.blit(self.image)

    def move_right(self):
        if self.collide.right:
            return
        self.rect.x += self.X_DISPLACEMENT

    def move_left(self):
        if self.collide.left:
            return
        self.rect.x -= self.X_DISPLACEMENT

    def jump(self):
        if self.collide.bottom:
            self.v_y = self.Y_SPEED
            self.rect.y += self.v_y

    def gravity(self):
        if not self.collide.bottom:
            self.rect.y += self.v_y
            self.v_y = self.v_y+self.Y_DISPLACEMENT
        else:
            self.v_y = 0
    def adjust_pos(self):
        while True:
            self.collider.collide(self)
            if self.collide.bottom and self.collide.bottom[0]:
                self.rect.y -= 1
            elif self.collide.top and self.collide.top[0]:
                self.rect.y += 1
            elif self.collide.right and self.collide.right[0]:
                self.rect.x -= 1
            elif self.collide.left and self.collide.left[0]:
                self.rect.x += 1
            else:
                break

    def on_update(self):
        self.gravity()
        self.adjust_pos()
        print(self.collide)

    def get_mask(self):
        return pygame.mask.from_surface(self.image)


class Player(Character):

    """The main character."""

    def __init__(self, *args):
        Character.__init__(self, *args)
        sprite_sheet = SpriteSheet('main_char.png')


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
        self.change_movement(self.JUMPING)
        #self.collide.bottom = False

    def gravity(self):
        super(Player, self).gravity()
        if self.movement == Character.JUMPING and self.v_y==0:
            self.change_movement(Character.MOTIONLESS)

    def on_render(self, dst):
        self.image = self.anims[self.direction + self.movement].current_image()
        x,y = self.rect.x, self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x,y
        dst.blit(self.image, (self.rect.x, self.rect.y))
        self.anims[self.direction + self.movement].next()

    def get_mask(self):
        s = self.anims[self.direction + self.movement].current_image()
        return pygame.mask.from_surface(s)
