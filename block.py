import pygame
from pygame.locals import *

test_in_rect = lambda rect, pos: pos[0] >= rect[0] and pos[0] < (rect[2]+rect[0]) and pos[1] >= rect[1] and pos[1] < (rect[3]+rect[1])
get_equivalent_block_pos = lambda pos : (pos[0] - (pos[0]%Block.BLOCK_SIZE), pos[1] - (pos[1]%Block.BLOCK_SIZE))

class Block(pygame.sprite.Sprite):

    """A block in the game."""

    BLOCK_SIZE = 32
    SPRITES = {}
    SPRITES_DESC = {}

    def __init__(self, pos, image=None):
        super().__init__()
        self.image = Block.SPRITES.get(image, None)
        self.image_name = image
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def on_render(self, dst):
        dst.blit(self.image, (self.rect.x, self.rect.y))

    def on_update(self):
        pass
    def as_dict(self):
        return {"x":self.x, "y":self.y, "Type":self.image_name}
