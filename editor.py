#! /usr/bin/python3

import pygame
from pygame.locals import *


from app import App, UPDATE_SPRITES_EVENT
from character import Player
from block import Block
from bubbleLoader import BubbleLoader

test_in_rect = lambda rect, pos: pos[0] >= rect[0] and pos[0] < (rect[2]+rect[0]) and pos[1] >= rect[1] and pos[1] < (rect[3]+rect[1])

class Editor(App):
    def __init__(self):
        super().__init__()
        pygame.mouse.set_visible(True)

        self.current_layer = "Background"
        x,y = self.window.get_width() - Block.BLOCK_SIZE - 20, 0
        w,h = Block.BLOCK_SIZE + 20, self.window.get_height()
        self.menu = SideMenu((x,y), (w,h))

        self.font = pygame.font.Font(None, 32)

    def on_render(self):
        super().on_render()
        self.menu.on_render(self.window)
        txt = self.font.render(self.current_layer, True, (0,0,0))
        self.window.blit(txt, (0,0))

    def on_event(self, e):
        if e.type == QUIT:
            self.running = False
        elif e.type == KEYDOWN:
            if self.menu.test_key(e.key):
                return
            if e.key == K_ESCAPE:
                self.running = False
            elif e.key == K_b:
                self.current_layer = "Background"
            elif e.key == K_m:
                self.current_layer = "Middleground"
            elif e.key == K_f:
                self.current_layer = "Foreground"
            elif e.key == K_s:
                self.loader.save()
        elif e.type == UPDATE_SPRITES_EVENT:
            for o in self.objects:
                o.on_update()
        elif e.type == MOUSEBUTTONDOWN:
            if self.menu.test_click(e.pos):
                return
            eq = e.pos[0] - (e.pos[0]%Block.BLOCK_SIZE), e.pos[1] - (e.pos[1]%Block.BLOCK_SIZE)
            if e.button == 3:
                if self.current_layer == "Background":
                    self.background.pop(eq, None)
                elif self.current_layer == "Middleground":
                    self.middleground.pop(eq, None)
                elif self.current_layer == "Foreground":
                    self.foreground.pop(eq, None)
                return
            if self.current_layer == "Background":
                self.background[eq] = Block(eq,self.menu.get_current())
            if self.current_layer == "Middleground":
                self.middleground[eq] = Block(eq,self.menu.get_current())
            if self.current_layer == "Foreground":
                self.foreground[eq] = Block(eq,self.menu.get_current())

    def on_mainloop(self):
        self.running = True

        while self.running:
            self.window.fill((200,200,200))
            if not pygame.event.peek(KEYDOWN):
                self.player.change_movement(Player.MOTIONLESS)

            for e in pygame.event.get():
                self.on_event(e)
            self.on_render()
            pygame.display.flip()
            pygame.time.Clock().tick(20)

    def on_exit(self):
        pygame.quit()

class MenuItem:
    def __init__(self, value, image, pos, size, txt=None):
        self.font = pygame.font.Font(None, 32)

        self.value = value
        self.image = image.copy()
        if txt:
            self.txt = self.font.render(txt, True, (200,200,200))
            self.image.blit(self.txt, (0,0))
        self.pos = pos
        self.size = size
        self.selected = False

    def on_render(self, dst):
        dst.blit(self.image, self.pos)
        if self.selected:
            x,y = self.pos
            w,h = self.size
            pygame.draw.rect(dst, (0,255,0), (x,y,w,h), 2)

class Menu:
    def __init__(self, pos, size):
        self.current = 0
        self.pos = pos
        self.size = size

        self.items = []

    def on_render(self, dst):
        x,y = self.pos
        w,h = self.size
        pygame.draw.rect(dst, (0,0,0), (x,y,w,h))
        for b in self.items:
            b.on_render(dst)

    def test_click(self, pos):
        click_on_me = test_in_rect((self.pos[0], self.pos[1], self.size[0], self.size[1]), pos)
        for n,b in enumerate(self.items):
            x,y = b.pos
            w,h = b.size
            if test_in_rect((x,y,w,h), pos):
                self.items[self.current].selected = False
                self.current = n
                self.items[self.current].selected = True
        return click_on_me
    def test_key(self, k):
        return False

    def get_current(self):
        return self.items[self.current].value

class SideMenu(Menu):
    def __init__(self, pos, size):
        super().__init__(pos, size)
        x,y = pos
        x,y = x + 10, y + 10
        k = list(Block.SPRITES.keys())
        k.sort()
        for b in k:
            i = MenuItem(b, Block.SPRITES[b], (x,y), (Block.BLOCK_SIZE, Block.BLOCK_SIZE), b)
            self.items.append(i)
            y += Block.BLOCK_SIZE + 5
        self.items[0].selected = True
    def test_key(self, k):
        if k==K_UP:
            c = (self.current - 1) % len(self.items)
        elif k == K_DOWN:
            c = (self.current + 1) % len(self.items)
        else :
            return False
        self.items[self.current].selected = False
        self.current = c
        self.items[self.current].selected = True
        return True

class BottomMenu(Menu):
    def __init__(self, pos, size):
        super().__init__(pos,size)


if __name__ == "__main__":
    e = Editor()
    e.on_mainloop()
    e.on_exit()