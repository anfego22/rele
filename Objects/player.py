import pygame as pg
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT
import parameters.enums as en
from typing import Dict


class Player(pg.sprite.Sprite):
    def __init__(self, game, x: int = 0, y: int = 0):
        self.groups = game.allSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((en.TILE_SIZE, en.TILE_SIZE))
        self.image.fill(en.YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move(self, dx: int = 0, dy: int = 0) -> None:
        if not (self.game.robot.x == self.x + dx and self.game.robot.y == self.y + dy):
            self.x += dx
            self.y += dy
        blockList = pg.sprite.spritecollide(self, self.game.machineryParts, False)
        for b in blockList:
            b.x = self.x + dx
            b.y = self.y + dy

    def move_key(self, pressKey: Dict):
        if pressKey[K_UP]:
            self.move(dy=-1)
        if pressKey[K_DOWN]:
            self.move(dy=1)
        if pressKey[K_RIGHT]:
            self.move(dx=1)
        if pressKey[K_LEFT]:
            self.move(dx=-1)

    def update(self):
        self.rect.x = self.x * en.TILE_SIZE
        self.rect.y = self.y * en.TILE_SIZE
