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
            if e.key == K_LEFT:
                self.objects[0].change_direction(Player.LEFT)
            if e.key == K_RIGHT:
                self.objects[0].change_direction(Player.RIGHT)
            if e.key == K_UP:
                self.objects[0].change_movement(Player.JUMPING)
            if e.key == K_z:
                self.objects[0].change_movement(Player.RUNNING)
            if e.key == K_d:
                self.objects[0].change_movement(Player.DEAD)


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
