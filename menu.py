import pygame
from pygame.locals import *

from block import test_in_rect

class MenuItem:
    def __init__(self, value, image, pos, size, txt=None, txt_size=32):
        self.font = pygame.font.Font(None, txt_size)


        self.size = size
        self.pos = pos

        self.value = value
        if image:
            self.image = image.copy()
        else:
            self.image = None
        if txt:
            self.txt = self.font.render(txt, True, (255,255,255))
            if self.image:
                self.image.blit(self.txt, (0,0))
            else:
                self.image = self.txt
                self.size = self.txt.get_size()
        self.selected = False

    def on_render(self, dst):
        if self.image:
            dst.blit(self.image, self.pos)
        if self.selected:
            x,y = self.pos
            w,h = self.size
            pygame.draw.rect(dst, (0,255,0), (x,y,w,h), 2)

class Menu:
    def __init__(self, pos, size):
        self.current = None
        self.pos = pos
        self.size = size

        self.items = []

    def on_render(self, dst):
        for b in self.items:
            b.on_render(dst)

    def test_click(self, pos):
        click_on_me = test_in_rect((self.pos[0], self.pos[1], self.size[0], self.size[1]), pos)
        for n,b in enumerate(self.items):
            x,y = b.pos
            w,h = b.size
            if test_in_rect((x,y,w,h), pos):
                if self.current:
                    self.items[self.current].selected = False
                self.current = n
                self.items[self.current].selected = True

        return click_on_me
    def test_key(self, k):
        return False

    def get_current(self):
        if self.current is not None:
            return self.items[self.current].value
        else:
            return None

    def reset_current(self):
        if self.current is not None:
            self.items[self.current].selected = False
            self.current = None

class MainMenu(Menu):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        x,y = pos
        w,h = size
        w,h = (75*w)//100, (25*h)//100
        self.items = [
            MenuItem("Jouer", None, (x+w//2, y), (w,h), "Jouer", txt_size=200),
            MenuItem("Éditeur", None, (x+w//2, y+(size[1]-h)), (w,h), "Éditeur", txt_size=200)
        ]
        w,h = size
        h += 20
        for i in self.items:
            i_w,i_h = i.size
            i.pos = x + (w-i_w)//2, y
            y += i_h*1.25
