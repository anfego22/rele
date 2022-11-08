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


class Levels:
    def __init__(self, game, dirname: str, sep: str = ","):
        self.data = self.read_data(dirname, sep)
        self.game = game
        self.level = 0

    def read_data(self, dirname: str, sep: str = ",") -> None:
        with open(dirname, "rt") as f:
            data = f.readlines()
            self.levelDict = {}
            for row in data[1:]:
                x, y, lv = row.split(sep)
                if int(lv) in self.levelDict:
                    self.levelDict[int(lv)].append((int(x), int(y)))
                else:
                    self.levelDict[int(lv)] = [(int(x), int(y))]

    def create_level(self) -> None:
        if self.level not in self.levelDict:
            return None
        for x, y in self.levelDict[self.level]:
            Destiny(self.game, x, y)

    def update(self):
        if len(self.game.destination) != 0:
            return None
        self.level += 1
        self.create_level()
