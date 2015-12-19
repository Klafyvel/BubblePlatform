import pygame
from pygame.locals import *



class Block:

    """A block in the game."""

    BLOCK_SIZE = 32
    SPRITES = {}
    SPRITES_DESC = {}

    def __init__(self, pos, image=None):
        self.x, self.y = pos
        self.image = Block.SPRITES.get(image, None)
        self.image_name = image

    def on_render(self, dst):
        dst.blit(self.image, (self.x, self.y))

    def on_update(self):
        pass
    def as_dict(self):
        return {"x":self.x, "y":self.y, "Type":self.image_name}
