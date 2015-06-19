import pygame
from pygame.locals import *

from character import Player


class App:

    """Handles the application"""

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((0, 0), FULLSCREEN)
        pygame.mouse.set_visible(False)
        pygame.key.set_repeat(5, 5)

        self.running = False

        self.objects = [Player((0,0))]

    def on_event(self, e):
        if e.type == QUIT:
            self.running = False
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                self.running = False
            if e.key == K_a:
                self.objects[0].movement = Player.RUNNING


    def on_render(self):
        for o in self.objects:
            o.on_render(self.window)

    def on_mainloop(self):
        self.running = True

        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_render()
            pygame.display.flip()
            pygame.time.Clock().tick(20)

    def on_exit(self):
        pygame.quit()
