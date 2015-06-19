import pygame
from pygame.locals import *


class App:

    """Handles the application"""

    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((0, 0), FULLSCREEN)
        pygame.mouse.set_visible(False)
        pygame.key.set_repeat(5, 5)

        self.running = False

    def on_event(self, e):
        if e.type == QUIT:
            self.running = False

    def on_render(self):
        pass

    def on_mainloop(self):
        self.running = True

        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_render()
            pygame.display.flip()

    def on_exit(self):
        pygame.quit()
