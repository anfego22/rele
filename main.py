import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT
import parameters.enums as en
from Objects.player import Player
from Objects.robot import Robot

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(en.SCREEN_DIM)


# Groups
allSprites = pygame.sprite.Group()

# Run until the user asks to quit
running = True
player = Player()
robot = Robot()

allSprites.add([player, robot])

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        if event.type == QUIT:
            running = False
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    screen.fill(en.SCREEN_FILL)
    for entity in allSprites:
        screen.blit(entity.surf, entity.rect)

    pygame.display.flip()
    clock.tick(en.CLOCK_TICK)

pygame.quit()
