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
        self.vx, self.vy = 0, 0
        self.x = x
        self.y = y

    def move_key(self):
        self.vx, self.vy = 0, 0
        pressKey = pg.key.get_pressed()
        if pressKey[K_UP]:
            self.vy = -en.PLAYER_SPEED
        if pressKey[K_DOWN]:
            self.vy = en.PLAYER_SPEED
        if pressKey[K_RIGHT]:
            self.vx = en.PLAYER_SPEED
        if pressKey[K_LEFT]:
            self.vx = -en.PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.71707
            self.vy *= 0.71707

    def update(self):
        self.move_key()
        dx = self.vx * self.game.dt
        dy = self.vy * self.game.dt
        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)
        if pg.sprite.spritecollideany(self, self.game.robots):
            self.x -= dx
            self.y -= dy
            self.rect.topleft = (self.x, self.y)
        blockList = pg.sprite.spritecollide(self, self.game.machineryParts, False)
        for b in blockList:
            b.x += dx
            b.y += dy


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        """Create a Wall."""
        self.groups = game.allSprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((en.TILE_SIZE, en.TILE_SIZE))
        self.image.fill(en.WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x * en.TILE_SIZE
        self.rect.y = y * en.TILE_SIZE
