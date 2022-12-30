import random
import torch
import pygame as pg
import parameters.enums as en
from typing import Dict
import numpy as np
from Objects.utils import GameBuffer
from Objects.basic import Brain


class Robot(pg.sprite.Sprite):
    def __init__(self, game, buffer: GameBuffer, x: int = 0, y: int = 0):
        self.groups = game.allSprites, game.robots
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((en.TILE_SIZE, en.TILE_SIZE))
        self.image.fill(en.LIGHTGREY)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * en.TILE_SIZE
        self.y = y * en.TILE_SIZE
        self.actions = [pg.K_UP, pg.K_RIGHT, pg.K_DOWN, pg.K_LEFT]
        self.lastScore = 0
        self.buffer = buffer
        self.brain = Brain([3, 60, 60], 4)

    def move(self, pressKey) -> None:
        self.vx, self.vy = 0, 0
        if pressKey == pg.K_UP:
            self.vy = -en.PLAYER_SPEED
        if pressKey == pg.K_DOWN:
            self.vy = en.PLAYER_SPEED
        if pressKey == pg.K_RIGHT:
            self.vx = en.PLAYER_SPEED
        if pressKey == pg.K_LEFT:
            self.vx = -en.PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.71707
            self.vy *= 0.71707

    def wall_collision(self, dx: float = 0, dy: float = 0):
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.x -= dx
            self.y -= dy
            self.rect.topleft = (self.x, self.y)

    def machine_parts_collision(self, dx: float = 0, dy: float = 0) -> None:
        blockList = pg.sprite.spritecollide(self, self.game.machineryParts, False)
        for b in blockList:
            b.x += dx
            b.y += dy
            if pg.sprite.spritecollideany(b, self.game.walls):
                b.set_ttl()
                b.x -= dx
                b.y -= dy

    def update(self, X: np.array):
        action = self.predict(X)
        if action:
            self.move(action)
        dx = self.vx * self.game.dt
        dy = self.vy * self.game.dt
        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)
        self.wall_collision(dx, dy)
        self.machine_parts_collision(dx, dy)

    def predict(self, X: np.array) -> int:
        with torch.no_grad():
            if len(self.buffer.history) > en.PREV_OBS:
                policy = self.brain.act(self.buffer.history[-1]["obs"][None, :])
                return np.random.choice(self.actions, p=policy[0])
        return None
