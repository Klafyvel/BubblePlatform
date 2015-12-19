import json
import zipfile
import tempfile

import pygame
from pygame.locals import *

from sprites import SpriteSheet, Animation, TimedAnimation
from block import Block

class BubbleLoaderError(Exception):
    pass

class BubbleLoader(dict):
    def __init__(self, filepath, app):
        super().__init__(self)
        self.file = filepath
        self.objects = {}
        self.app = app

        self.tmp_dir = None

    def load(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        manifest = {}
        print("BubbleLoader : Extraction de l'archive.")
        with zipfile.ZipFile(self.file) as archive:
            archive.extractall(self.tmp_dir.name)

        with open(self.tmp_dir.name + "/manifest.json") as manifest_file:
            manifest = json.loads(manifest_file.read())

        if 'Blocks' in manifest.keys():
            self.load_blocks(manifest['Blocks'])
        else:
            print("BubbleLoader : Le niveau ne semble pas contenir de blocks.")

        self.tmp_dir.cleanup()

    def create_characters_types(self):
        pass

    def load_blocks(self,blocks_info):
        if not self.tmp_dir:
            raise BubbleLoaderError("BubbleLoader : Il n'y a pas de dossier temporaire pour l'extraction des sprites.")

        print("BubbleLoader : Chargement des images de blocks.")
        sprite_sheet = SpriteSheet(self.tmp_dir.name + '/' + blocks_info['Sprite sheet']['Path'])
        Block.SPRITES_DESC = blocks_info['Sprite sheet']['Sprites description']
        for o_type in blocks_info['Sprite sheet']['Sprites description']:
            rect = (o_type['x'], o_type['y'], o_type['width'], o_type['height'])
            Block.SPRITES[o_type['Name']] = sprite_sheet.image_at(rect).convert_alpha()

        print("BubbleLoader : Placement des blocks.")
        for b in blocks_info['Background blocks']:
            pos = (b['x'], b['y'])
            self.app.background[pos] = Block(pos, image=b['Type'])

        for b in blocks_info['Foreground blocks']:
            pos = (b['x'], b['y'])
            self.app.foreground[pos] = Block(pos, image=b['Type'])

    def save(self):
        self.tmp_dir = tempfile.TemporaryDirectory()





