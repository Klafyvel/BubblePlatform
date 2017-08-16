#! /usr/bin/python3

import pygame
from pygame.locals import *

from editor import Editor
from app import App

from menu import MainMenu

if __name__ == '__main__':

    pygame.init()
    pygame.font.init()
    #self.window = pygame.display.set_mode((0, 0), FULLSCREEN)
    window = pygame.display.set_mode((600,600))
    pygame.display.set_caption("Bubble Platform !")


    menu = MainMenu((0,0), window.get_size())

    c = None
    running = True
    while running:

        for e in pygame.event.get():
            if e.type == MOUSEBUTTONUP:
                menu.test_click(e.pos)
                c = menu.get_current()
                print(c)

            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    running = False
            elif e.type == QUIT:
                running = False

        window.fill((0,0,0))
        menu.on_render(window)

        pygame.display.flip()

        if c == "Jouer":
            App(window).on_mainloop()
        elif c == "Éditeur":
            Editor(window).on_mainloop()
        if c:
            menu.reset_current()
            pygame.mouse.set_visible(True)
            c = None

        pygame.time.Clock().tick(20)

    pygame.quit()