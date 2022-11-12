import pygame as pg
from random import randint, choice
import parameters.enums as en
from typing import Dict, List, Tuple
from datetime import datetime


class Machinery(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.allSprites, game.machineryParts
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((en.TILE_SIZE, en.TILE_SIZE))
        self.rect = self.image.get_rect()
        self.random_init()

    def random_init(self):
        self.ttl = False
        self.color, self.value = choice(en.MACHINE_COLOR_VALUES)
        self.image.fill(self.color)
        self.x = randint(10, en.GRID_WIDTH - 4) * en.TILE_SIZE
        self.y = randint(4, en.GRID_HEIGHT - 4) * en.TILE_SIZE

    def update(self):
        nowTime = datetime.now()
        if self.ttl and (nowTime - self.startTime).seconds > en.MACHINE_TTL:
            self.ttl = False
            self.random_init()
        self.rect.x = self.x
        self.rect.y = self.y

    def set_ttl(self):
        self.ttl = True
        self.startTime = datetime.now()

    def reset(self):
        self.random_init()
        self.rect.x = self.x
        self.rect.y = self.y


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

    def update(self):
        dest = pg.sprite.spritecollide(self, self.game.machineryParts, False)
        for b in dest:
            self.game.SCORE += b.value
            b.reset()
