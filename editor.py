#! /usr/bin/python3

import pygame
from pygame.locals import *


from app import App, UPDATE_SPRITES_EVENT
from character import Player
from block import Block, get_equivalent_block_pos, test_in_rect
from bubbleLoader import BubbleLoader
from menu import Menu, MenuItem


class Editor(App):
    def __init__(self, window):
        super().__init__(window)
        pygame.display.set_caption("Bubble Platform ! - Editor")

        pygame.mouse.set_visible(True)

        self.objects = {}

        self.current_layer = "Middleground"
        x,y = self.window.get_width() - Block.BLOCK_SIZE - 20, 0
        w,h = Block.BLOCK_SIZE + 20, self.window.get_height()
        self.menu = SideMenu((x,y), (w,h))

        self.font = pygame.font.Font(None, 32)

    def on_render(self):
        for o in self.background.values():
            o.on_render(self.window)
        if self.current_layer in ("Middleground", "Foreground"):
            for o in self.middleground.values():
                o.on_render(self.window)
        for o in self.objects:
            o.on_render(self.window)
        if self.current_layer == "Foreground":
            for o in self.foreground.values():
                o.on_render(self.window)

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
            eq = get_equivalent_block_pos(e.pos)
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
        self.current = 0
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
    def on_render(self, dst):
        x,y = self.pos
        w,h = self.size
        pygame.draw.rect(dst, (0,0,0), (x,y,w,h))
        super().on_render(dst)

class BottomMenu(Menu):
    def __init__(self, pos, size):
        super().__init__(pos,size)


if __name__ == "__main__":
    e = Editor()
    e.on_mainloop()
    e.on_exit()