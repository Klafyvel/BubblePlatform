import pygame
from pygame.locals import *

from bubble_platform.resource_manager import ResourceManager
from bubble_platform.ui import VLayout, ImageButton, Button, Input

class App():
    """
    A simple application.
    """
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.window = pygame.display.set_mode((800,600))
        pygame.display.set_caption("Bubble Platform !")

        self.rc_manager = ResourceManager()
        self.rc_manager.load_image("Blocks.png", "blocks")
        self.rc_manager.load_font(None, 40, "main_menu")

        kwargs = {
            'rc_manager' : self.rc_manager,
            'color' : (0, 0, 0),
            'background' : (200, 25, 100),
            'border' : (255, 255, 255),
            'border_width' : 3,
            'image' : 'blocks',
            'min_width' : 200,
            'min_height' : 50,
            'font' : "main_menu",        
        }

        self.menu = VLayout()

        self.menu.add_widget(Button(
            **kwargs,
            text="Foo",
            callback=self.on_foo
        ))

        self.menu.add_widget(Button(
            **kwargs,
            text="Bar",
            callback=self.on_bar
        ))

        self.menu.add_widget(Input(
            text="Input widget :",
            rc_manager=self.rc_manager,
            color=(0, 0, 0),
            background=(200, 25, 100),
            border=(255, 255, 255),
            border_width=3,
            image='blocks',
            min_width=200,
            min_height=50,
            font="main_menu",
            max_length=20,
        ))

        self.menu.add_widget(Button(
            **kwargs,
            text="Quit",
            callback=self.on_quit
        ))

        self.running = True

    def on_mainloop(self):
        while self.running:
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.on_quit()
                else:
                    self.menu.on_event(e)
            w,h = self.menu.size()
            self.window.fill((0,0,0))
            self.menu.on_render(self.window, (800-w)/2, (600-h)/2)

            pygame.display.flip()
            pygame.time.Clock().tick(20)

    def on_quit(self):
        self.running = False
        print(self.menu.widgets[-2].input)
        print("Bye.")

    def on_foo(self):
        print("Foo")

    def on_bar(self):
        print("Bar")

def main():
    a = App()
    a.on_mainloop()