import pygame as pg
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT
from Objects.machinery import Machinery
import parameters.enums as en
from typing import Dict
import numpy as np


class Player(pg.sprite.Sprite):
    def __init__(self, game, x: int = 0, y: int = 0):
        self.groups = game.allSprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((en.TILE_SIZE, en.TILE_SIZE))
        self.image.fill(en.YELLOW)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * en.TILE_SIZE
        self.y = y * en.TILE_SIZE

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

    def machine_parts_collision(self, dx: float = 0, dy: float = 0) -> None:
        blockList = pg.sprite.spritecollide(self, self.game.machineryParts, False)
        for b in blockList:
            b.x += dx
            b.y += dy
            if pg.sprite.spritecollideany(b, self.game.walls):
                b.set_ttl()
                b.x -= dx
                b.y -= dy

    def wall_collision(self, dx: float = 0, dy: float = 0):
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.x -= dx
            self.y -= dy
            self.rect.topleft = (self.x, self.y)

    def robot_collision(self, dx, dy):
        if pg.sprite.spritecollideany(self, self.game.robots):
            self.x -= dx
            self.y -= dy
            self.rect.topleft = (self.x, self.y)

    def update(self, X: np.array):
        self.move_key()
        dx = self.vx * self.game.dt
        dy = self.vy * self.game.dt
        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)
        self.robot_collision(dx, dy)
        self.wall_collision(dx, dy)
        self.machine_parts_collision(dx, dy)


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


class PlayerActionBuffer(object):
    """Class to store player history of moves."""

    def __init__(self, maxSize: int = 64) -> None:
        self.history = []
        self.maxSize = maxSize

    def update(self, X: np.array, action: int) -> None:
        if len(self.history) < self.maxSize:
            self.history.append((X, action))
            return None
        self.history.pop(0)
        self.history.append((X, action))
