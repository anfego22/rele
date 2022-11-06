import pygame
import parameters.enums as en
from typing import Dict


class Robot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.surf = pygame.image.load(fp.PLAYER_IMAGE).convert()
        self.surf = pygame.surface.Surface(en.ROBOT_DIM)
        self.surf.fill(en.ROBOT_FILL)
        self.rect = self.surf.get_rect()
        self.actions = {
            "UP": self.rect.move_ip(0, -en.MOV_STEP),
            "DOWN": self.rect.move_ip(0, en.MOV_STEP),
            "RIGHT": self.rect.move_ip(en.MOV_STEP, 0),
            "LEFT": self.rect.move_ip(-en.MOV_STEP, 0),
        }

    def perform_action(self, a: str):
        if a in self.action:
            self.action[a]
