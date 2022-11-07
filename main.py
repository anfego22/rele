import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT
import parameters.enums as en
from Objects.player import Player
from Objects.robot import Robot
import sys


class Game(pygame.sprite.Sprite):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((en.WIDTH, en.HEIGHT))
        self.clock = pygame.time.Clock()
        self.load_data()

    def load_data(self):
        pass

    def new(self):
        """Initialize all variables."""
        self.allSprites = pygame.sprite.Group()
        self.robots = pygame.sprite.Group()
        self.player = Player(self, 10, 10)
        self.robot = Robot(self, 8, 10)

    def quit(self):
        pygame.quit()
        sys.exit()

    def events(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.quit()
            if event.type == QUIT:
                self.quit()
        pressedKeys = pygame.key.get_pressed()
        self.player.move_key(pressedKeys)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(en.FPS) / 1000
            self.events()
            self.updates()
            self.draw()

    def updates(self):
        self.allSprites.update()

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
