"""
The sprite module allows to deal with sprites.
"""

import pygame
from pygame.locals import *


class SpriteSheet:
    """
    A simple sprite sheet.
    """

    def __init__(self, image_path, default_rect=None):
        """
        The __init__ method.

        :param image_path: The path to the image.
        :param default_rect: The default rect to be used if no one is provided.
        """
        self.image = pygame.image.load(image_path).convert_alpha()
        self.default_rect = default_rect

    def image_at(self, rect):
        """
        Return the image at the asked rect.

        :param rect: The rect.
        """
        if rect:
            image = self.image.subsurface(rect)
        else:
            image = self.image.subsurface(self.default_rect)
        return image.copy()

    def images_at(self, nb, rect=None):
        """
        Same as image_at, but with several images.

        :param rect: The rect.
        :param nb: The number of images.
        """
        if not rect:
            rect = self.default_rect
        return [self.image_at((i * rect[2], rect[1], rect[2], rect[3])) for i in range(nb)]


class Animation:

    def __init__(self, images):
        self.images = images
        self.current = 0

    def next(self):
        i = self.images[self.current]
        self.current = (self.current + 1) % len(self.images)
        return i

    def current_image(self):
        return self.images[self.current]

    def stop(self):
        self.current = 0


class TimedAnimation(Animation):

    def __init__(self, images, delta):
        Animation.__init__(self, images)
        self.timer = pygame.time.get_ticks()
        self.delta = delta

    def next(self):
        if (pygame.time.get_ticks() - self.timer) > self.delta:
            self.timer = pygame.time.get_ticks()
            return Animation.next(self)
        else:
            return self.images[self.current]

    def stop(self):
        pass
