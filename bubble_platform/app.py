"""
This module provides the main class of the application.
"""

import os

import pygame
from pygame.locals import *

from bubble_platform import settings
from bubble_platform.settings import logger
from bubble_platform.resource_manager import ResourceManager
from bubble_platform import ui
from bubble_platform.editor import LevelEditor, CampaignEditor

class MainMenu(ui.VLayout):
    def on_render(self, dst):
        w,h = self.size()
        w_dst,h_dst = dst.get_size()
        self.on_render_as_layout(dst, (w_dst-w)/2, (h_dst-h)/2)


class App():
    """
    The application.
    """
    def __init__(self):
        pygame.init()
        pygame.font.init()
        if settings.DEBUG:
            self.window = pygame.display.set_mode((800,600))
        else:
            self.window = pygame.display.set_mode(FULLSCREEN)

        pygame.display.set_caption("Bubble Platform !")

        self.rc_manager = ResourceManager()
        self.rc_manager.load_image("Blocks.png", "blocks")
        self.rc_manager.load_font(None, 40, "main_menu")

        self.main_menu = MainMenu(
            rc_manager=self.rc_manager,
            text="Bubble Platform !",
            font="main_menu"
        )

        main_menu_args = {
            'background' : (200,200,200),
            'border' : (50,50,50),
            'border_width' : 4,
            'font' : "main_menu",
            'rc_manager' : self.rc_manager
        }

        self.main_menu.add_widget(ui.Button(
            text="CAMPAIGN !",
            **main_menu_args,
            callback=self.on_foo,
        ))

        self.main_menu.add_widget(ui.Button(
            text="Editor",
            **main_menu_args,
            callback=self.on_editor,
        ))

        self.main_menu.add_widget(ui.Button(
            text="Quit",
            **main_menu_args,
            callback=self.on_quit,
        ))

        self.main_widget = self.main_menu

        self.running = True

    def on_mainloop(self):
        while self.running:
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.on_quit()
                else:
                    self.main_widget.on_event(e)
            self.window.fill((255,255,255))
            self.main_widget.on_render(self.window)

            pygame.display.flip()
            pygame.time.Clock().tick(20)

    def on_quit(self):
        self.running = False
        logger.info("Bye")

    def on_foo(self):
        logger.debug("Foo")

    def on_editor(self):
        editor = CampaignEditor(
            rc_manager=self.rc_manager,
            path=os.path.join(settings.APP_DIR, 'campaigns', 'First campaign', ''),
            app=self,
        )
        self.main_widget = editor