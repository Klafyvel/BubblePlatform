import os
from bubble_platform import level
from slugify import slugify
LEVEL_DIR = os.path.dirname(os.path.abspath(__file__))

LEVEL_NAME = "Some level"

class Level(level.Level):
    def __init__(self, rc_manager):

        super(Level, self).__init__(
            rc_manager=rc_manager,
            filename=os.path.join(LEVEL_DIR, slugify(LEVEL_NAME)+".map"),
            name=LEVEL_NAME,
        )
        