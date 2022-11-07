import pygame as pg
import parameters.enums as en
from typing import Dict


class Robot(pg.sprite.Sprite):
    def __init__(self, game, x: int = 0, y: int = 0):
        self.groups = game.allSprites, game.robots
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((en.TILE_SIZE, en.TILE_SIZE))
        self.image.fill(en.LIGHTGREY)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move(self, dx: int = 0, dy: int = 0) -> None:
        self.x += dx
        self.y += dy

    def update(self):
        self.rect.x = self.x * en.TILE_SIZE
        self.rect.y = self.y * en.TILE_SIZE
