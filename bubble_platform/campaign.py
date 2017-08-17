"""
The campaign module
===================

Here is defined the base class for campaigns.
"""
import os
import json
import importlib

from collections import OrderedDict

import pygame
from pygame.locals import *

from bubble_platform import settings
from bubble_platform.settings import logger
from bubble_platform.level import BLOCK_SIZE

class Campaign():
    """
    The base class for campaigns.
    """
    def __init__(self, rc_manager, path):
        """
        The __init__ method.

        :param rc_manager: The resource manager.
        :param campaign_name: The name of the campaign
        :param path: The path to the campaign directory.
        """
        self.rc_manager = rc_manager
        self.name = "No name"
        self.path = path

        self.levels = OrderedDict()
        self.blocks = []
        self.images = []
        self.ennemies = []
        self.has_own_blocks = False

        self.load_file()

    def load_file(self):
        """
        Loads the file.
        """
        json_file = os.path.join(self.path, "campaign.json")
        with open(json_file) as f:
            j = json.load(f)

        self.name = j['name']

        level_directory = os.path.join(self.path, 'level', '')
        for l in j['level']:
            spec = importlib.util.spec_from_file_location(
                l, 
                os.path.join(level_directory, l+'.py')
            )
            self.levels[l] = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.levels[l])

        self.has_own_blocks = j['blocks']['has_own_blocks']
        if self.has_own_blocks:
            blocks_filename = os.path.join(self.path, 'rc', 'Blocks.png')
        else:
            blocks_filename = os.path.join(settings.RC_DIR, 'Blocks.png')
        self.rc_manager.load_sprite_sheet(
            blocks_filename, 
            (0,0,BLOCK_SIZE, BLOCK_SIZE), 
            len(j['blocks']['names']),
            'Block',
            j['blocks']['names']
        )
        self.blocks = j['blocks']['names']

    def to_dict(self):
        return {
            'name' : self.name,
            'level' : list(self.levels.keys()),
            'blocks' : {
                'has_own_blocks' : self.has_own_blocks,
                'names' : self.blocks,
            },
        }

    def save(self):
        json_file = os.path.join(self.path, "campaign.json")
        with open(json_file, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)


