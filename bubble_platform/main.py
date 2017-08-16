import pygame
from pygame.locals import *

from bubble_platform.resource_manager import ResourceManager
from bubble_platform.ui import Menu

class App():
    """
    A simple application.
    """
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.window = pygame.display.set_mode((600,600))
        pygame.display.set_caption("Bubble Platform !")

        self.rc_manager = ResourceManager()

        self.menu = Menu(
            ("Foo", self.on_foo),
            ("Bar", self.on_bar),
            ("Quit", self.on_quit),
            rc_manager=self.rc_manager,
            color=(0, 0, 0),
            background=(200, 25, 100),
            border=(255, 255, 255),
            border_width=3,
        )

        self.running = True

    def on_mainloop(self):
        while self.running:
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.on_quit()
                else:
                    self.menu.on_event(e)
            self.window.fill((0,0,0))
            self.menu.on_render(self.window, 0, 0)

            pygame.display.flip()
            pygame.time.Clock().tick(20)

    def on_quit(self):
        self.running = False
        print("Bye.")

    def on_foo(self):
        print("Foo")

    def on_bar(self):
        print("Bar")

def main():
    a = App()
    a.on_mainloop()