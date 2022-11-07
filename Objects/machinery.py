import pygame as pg
from random import randint
import parameters.enums as en
from typing import Dict, List, Tuple
from datetime import datetime


class Machinery(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.allSprites, game.machineryParts
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((en.TILE_SIZE, en.TILE_SIZE))
        self.image.fill(en.GREEN)
        self.rect = self.image.get_rect()
        self.x = randint(10, en.GRID_WIDTH - 4) * en.TILE_SIZE
        self.y = randint(4, en.GRID_HEIGHT - 4) * en.TILE_SIZE
        self.ttl = False

    def update(self):
        nowTime = datetime.now()
        if self.ttl and (nowTime - self.startTime).seconds > en.MACHINE_TTL:
            self.ttl = False
            self.x = randint(10, en.GRID_WIDTH - 2) * en.TILE_SIZE
            self.y = randint(2, en.GRID_HEIGHT - 2) * en.TILE_SIZE
        self.rect.x = self.x
        self.rect.y = self.y

    def set_ttl(self):
        self.ttl = True
        self.startTime = datetime.now()


class Destiny(pg.sprite.Sprite):
    def __init__(self, game, x: int = 0, y: int = 0) -> None:
        self.groups = game.allSprites, game.destination
        pg.sprite.Sprite.__init__(self, self.groups)
        # super().__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((en.TILE_SIZE, en.TILE_SIZE))
        self.image.fill(en.BLUE)
        self.rect = self.image.get_rect()
        self.x, self.y = x, y
        self.rect.x = self.x * en.TILE_SIZE
        self.rect.y = self.y * en.TILE_SIZE
