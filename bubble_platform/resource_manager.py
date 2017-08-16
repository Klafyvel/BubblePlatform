"""
The resource manager module
===========================

This module provides a class which load resources and let the other classes
access to them.
"""

import os

import pygame

from bubble_platform import settings
from bubble_platform.settings import logger

class ResourceManager():
    """
    This class loads resources and let the other classes access to them.
    """
    def __init__(self):
        """
        The __init__ method.
        """
        self.rc = {}
        self.load_font(None, 20, "default_font")

    def load_font(self, font_name, text_size, rc_name):
        """
        Loads a font.

        :param font_name: The name of the font.
        :param text_size: The size of the text (px).
        :param rc_name: The name of the resource.
        """
        logger.info("Loading font {} with size {} as {}".format(
            font_name, text_size, rc_name)
        )
        self.rc[rc_name] = pygame.font.Font(font_name, text_size)

    def load_image(self, path, rc_name):
        """
        Loads an image.

        :param path: The path of the image.
        :param rc_name: The name of the resource.
        """
        full_path = os.path.join(settings.RC_DIR, path)
        logger.info("Loading image {} as {}".format(path, rc_name))
        self.rc[rc_name] = pygame.image.load(full_path, rc_name)

    def add_surface(self, s, name):
        """
        Adds a surface to the resources.

        :param s: The surface.
        :param name: The name of the resource.
        """
        logger.info("Registering surface {}".format(name))
        self.rc[name] = s

    def exists(self, name):
        """
        Checks if a resources is registered.

        :param name: The name of_the resource.
        """
        return name in self.rc.keys()

    def get(self, name):
        """
        Return the queried resource.

        :param name: The name of the resource.
        """
        return self.rc[name]