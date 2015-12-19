import pygame
from pygame.locals import *


class SpriteSheet:

    def __init__(self, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()


    def image_at(self, rect):
        image = self.image.subsurface(rect)
        #image.convert_alpha()
        return image.copy()

    def images_at(self, rect, nb):
        return [self.image_at((i * rect[2], rect[1], rect[2], rect[3])) for i in range(nb)]


class Animation:

    def __init__(self, images):
        self.images = images
        self.current = 0

    def next(self):
        i = self.images[self.current]
        self.current = (self.current + 1) % len(self.images)
        return i

    def current(self):
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
