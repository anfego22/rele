import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT
import parameters.enums as en
from typing import Dict


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x: int = 0, y: int = 0):
        self.groups = game.allSprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((en.TILE_SIZE, en.TILE_SIZE))
        self.image.fill(en.YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move(self, dx: int = 0, dy: int = 0) -> None:
        self.x += dx
        self.y += dy

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
