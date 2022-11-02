import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, QUIT
import parameters.enums as en
from Objects.player import Player

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(en.SCREEN_DIM)


# Run until the user asks to quit
running = True
player = Player()

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        if event.type == QUIT:
            running = False
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    screen.fill((0, 0, 0))
    screen.blit(player.surf, player.rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
