import pygame as pg
from random import randint
import parameters.enums as en
from typing import Dict


class Machinery(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.allSprites, game.machineryParts
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((en.TILE_SIZE, en.TILE_SIZE))
        self.image.fill(en.GREEN)
        self.rect = self.image.get_rect()
        self.x = randint(10, en.GRID_WIDTH - 2) * en.TILE_SIZE
        self.y = randint(2, en.GRID_HEIGHT - 2) * en.TILE_SIZE

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y
