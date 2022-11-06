import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT
import parameters.filePath as fp
import parameters.enums as en
from typing import Dict


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.surf = pygame.image.load(fp.PLAYER_IMAGE).convert()
        self.surf = pygame.surface.Surface(en.PLAYER_DIM)
        self.surf.fill(en.PLAYER_FILL)
        self.rect = self.surf.get_rect()

    def update(self, press_key: Dict):
        if press_key[K_UP]:
            self.rect.move_ip(0, -en.MOV_STEP)
        if press_key[K_DOWN]:
            self.rect.move_ip(0, en.MOV_STEP)
        if press_key[K_RIGHT]:
            self.rect.move_ip(en.MOV_STEP, 0)
        if press_key[K_LEFT]:
            self.rect.move_ip(-en.MOV_STEP, 0)

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(en.SCREEN_DIM[0], self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(en.SCREEN_DIM[1], self.rect.bottom)
