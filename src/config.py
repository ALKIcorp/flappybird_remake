import pygame

# Screen Dimensions
SCREEN_WIDTH = 288
SCREEN_HEIGHT = 512

# Game Constants
GRAVITY = 0.25
PIPE_GAP = 150 # Not explicitly variable before but logic used 150 offset
FLOOR_HEIGHT = 400 # 512 - 112

# Events
BIRDFLAP = pygame.USEREVENT + 1
SPAWNPIPE = pygame.USEREVENT

# State
STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAMEOVER = 2
STATE_SETTINGS = 3

# Colors
COLOR_WHITE = (255, 255, 255)
COLOR_SKY_BLUE = (78, 192, 202)
