import os
from pygame.locals import *

MAIN_WINDOW_SIZE = (640, 480)
IMAGE_DIR = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'images')

SPECIAL_TYPES = {'NONE': None}

MAX_PLAYERS = 3

FIRE_DELAY = 0.25

P1_MOVEMENT_KEYS = [K_w, K_s, K_a, K_d]
P2_MOVEMENT_KEYS = [K_i, K_k, K_j, K_l]
P3_MOVEMENT_KEYS = [K_UP, K_DOWN, K_LEFT, K_RIGHT]


BULLET_SCALE = [20,20]
ENEMY_SCALE = [25,25]

PLAYER_GUN_1_SPEED = [0,-12]