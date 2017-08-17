"""
The level module
================

Here is defined the base class for every level.
"""

import pygame
from pygame.locals import *

from bubble_platform.settings import logger

BLOCK_SIZE = 32

class Level:
    """
    The base class for every level.
    """
    def __init__(self, rc_manager, filename, name):
        """
        The __init__ method.

        :param rc_manager: The resource manager.
        :param filename: The file name for the tilemap.
        :param name: The full name of the level.
        """

        self.filename = filename
        self.name = name

        self.map  = []
        self.drawn_rect = None

    def load_map(self):
        """
        Loads the tilemap.
        """
        logger.info("Loading map {}".format(self.filename))
        with open(self.filename) as f:
            s = f.read().split('\n')

        self.map = [list(l) for l in s]

    def find_image(self, tile):
        """
        Returns the right image for the given tile.

        :param tile: the tile.
        """
        if tile == ' ':
            return None
        elif self.rc_manager.exists("block_" + tile):
            return self.rc_manager.get("block_"+tile)
        raise ValueError("No tile {} registered.".format(repr(tile)))

    def on_render(self, dst, rect):
        """
        Render the map on the given destination. Will only render blocks that
        are in the given rect.
        """
        self.drawn_rect = rect
        size_x = len(self.map)
        size_y = len(self.map[0])

        begin_x = min(rect[0] // BLOCK_SIZE, size_x)
        end_x = min((rect[0] + rect[2]) // BLOCK_SIZE + 1, size_x)
        begin_y = min(rect[1] // BLOCK_SIZE, size_y)
        end_y = min((rect[1] + rect[3]) // BLOCK_SIZE + 1, size_y)

        for x,i in enumerate(range(begin_x, end_x+1)):
            for y,j in enumerate(range(begin_y, end_y+1)):
                img = self.get_image(self.map[i][j])
                if img:
                    dst.blit(img, (x*BLOCK_SIZE, y*BLOCK_SIZE))

    def coordinate_to_map(self, coord):
        """
        Maps drawing coordinates to Map coordinate.

        :param coord: The drawing coordinates.
        """
        x,y = coord
        x -= self.drawn_rect[0]
        y -= self.drawn_rect[1]
        return (x//BLOCK_SIZE, y//BLOCK_SIZE)

