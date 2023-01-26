# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# Game setting
WIDTH = 1024
HEIGHT = 768
FPS = 30
BGCOLOR = DARKGREY

# Tile Size
TILE_SIZE = 32
GRID_WIDTH = WIDTH / TILE_SIZE
GRID_HEIGHT = HEIGHT / TILE_SIZE

# Player settings
PLAYER_SPEED = 320

# Machine parts setting
MACHINE_TTL = 1  # in seconds
MACHINE_COLOR_VALUES = [(WHITE, 5), (RED, -8), (GREEN, 3), (WHITE, 3)]

# ROBOT SETUP
PREV_OBS = 3
BATCH_SIZE = 32
