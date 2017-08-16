import pygame
from pygame.locals import *

from bubbleLoader import BubbleLoader
from character import Player, Character, Collider

UPDATE_SPRITES_EVENT = pygame.USEREVENT

class App:

    """Handles the application"""

    def __init__(self, window):
        self.window = window
        pygame.mouse.set_visible(False)
        pygame.key.set_repeat(5, 5)

        self.loader = BubbleLoader("test.zip", self)

        self.running = False

        self.collider = Collider(self)

        self.player = Player((0,60), self.collider)
        self.objects = {self.player}
        self.foreground = {}
        self.background = {}
        self.middleground = {}


        pygame.time.set_timer(UPDATE_SPRITES_EVENT, 60)

        self.loader.load()


    def on_event(self, e):
        k = pygame.key.get_pressed()
        if k[K_LEFT]:
            self.player.change_direction(Player.LEFT)
            self.player.change_movement(Player.RUNNING)
        if k[K_RIGHT]:
            self.player.change_direction(Player.RIGHT)
            self.player.change_movement(Player.RUNNING)

        if e.type == QUIT:
            self.running = False
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                self.running = False
            elif e.key == K_UP:
                self.player.jump()
            if e.key == K_d:
                self.player.change_movement(Player.DEAD)
        elif e.type == UPDATE_SPRITES_EVENT:
            for o in self.objects:
                o.on_update()

    def on_render(self):
        for o in self.background.values():
            o.on_render(self.window)
        for o in self.middleground.values():
            o.on_render(self.window)
        for o in self.objects:
            o.on_render(self.window)
        for o in self.foreground.values():
            o.on_render(self.window)

    def on_mainloop(self):
        self.running = True

        while self.running:
            #if pygame.event.peek(KEYDOWN):
            #    for event in pygame.event.get():
            #        self.on_event(event)
            #else:
            #    self.player.change_movement(Player.MOTIONLESS)
            self.window.fill((200,200,200))
            self.collider.collides()
            if not pygame.event.peek(KEYDOWN):
                self.player.change_movement(Player.MOTIONLESS)

            for e in pygame.event.get():
                self.on_event(e)
            self.on_render()
            pygame.display.flip()
            pygame.time.Clock().tick(20)

