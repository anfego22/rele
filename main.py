import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT
from os import path
import parameters.enums as en
from Objects.player import Player, Wall
from Objects.map import Map
from Objects.robot import Robot
import numpy as np
from Objects.machinery import Machinery, Destiny
import sys
import torch
from Objects.utils import GameBuffer
import pickle


class Game(pygame.sprite.Sprite):
    SCORE = 0

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((en.WIDTH, en.HEIGHT))
        self.clock = pygame.time.Clock()
        self.load_data()
        self.checkpoint = "robotCheckpoint" if path.exists("robotCheckpoint") else None

    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map = Map(game_folder + "/Static/map.txt")

    def new(self):
        """Initialize all variables."""
        self.buffer = GameBuffer.remote()
        self.allSprites = pygame.sprite.Group()
        self.machineryParts = pygame.sprite.Group()
        self.destination = pygame.sprite.Group()
        self.robots = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.part = Machinery(self)
        for j, row in enumerate(self.map.data):
            for i, col in enumerate(row):
                if col == "1":
                    Wall(self, i, j)
                elif col == "D":
                    self.destiny = Destiny(self, i, j)
                elif col == "P":
                    self.player = Player(self, self.buffer, i, j)
                elif col == "R":
                    self.robot = Robot(self, self.buffer, i, j, self.checkpoint)

    def quit(self):
        pygame.quit()
        sys.exit()

    def events(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.robot.save()
                    self.quit()
            if event.type == QUIT:
                self.robot.save()
                self.quit()

    def get_screen(self):
        screen = pygame.transform.scale(self.screen, (60, 60))
        screen = np.array(pygame.surfarray.array3d(screen))
        screen = screen.transpose((2, 1, 0))
        return torch.from_numpy(screen)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(en.FPS) / 1000
            screenMatrix = self.get_screen()
            self.events()
            self.updates(windowPixel=screenMatrix)
            self.draw()

    def updates(self, **args):
        for sprite in self.allSprites:
            if isinstance(sprite, Robot) or isinstance(sprite, Player):
                sprite.update(args["windowPixel"])
            else:
                sprite.update()

    def draw_grid(self):
        for x in range(0, en.WIDTH, en.TILE_SIZE):
            pygame.draw.line(self.screen, en.LIGHTGREY, (x, 0), (x, en.HEIGHT))
        for y in range(0, en.HEIGHT, en.TILE_SIZE):
            pygame.draw.line(self.screen, en.LIGHTGREY, (0, y), (en.WIDTH, y))

    def draw(self):
        self.screen.fill(en.BGCOLOR)
        self.draw_grid()
        self.allSprites.draw(self.screen)
        pygame.display.flip()


g = Game()
while True:
    g.new()
    g.run()
