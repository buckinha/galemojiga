import os
import pygame
from galemojiga.globals import IMAGE_DIR
from galemojiga.SpriteSheet import SpriteSheet

BULLET_SCALE = [20,20]
SMILE_SCALE = [25,25]

def load_ship_p1():
    path = os.path.join(IMAGE_DIR, 'emojione-sprite-40-travel.png')
    ss = SpriteSheet(path)
    ship_image = ss.image_at((0, 7))
    ship_image = pygame.transform.rotate(ship_image, 45)
    return ship_image

def load_orange_bullet():
    path = os.path.join(IMAGE_DIR, 'emojione-sprite-40-symbols.png')
    ss = SpriteSheet(path)
    bullet_image = ss.image_at((11,10))
    bullet_image = pygame.transform.scale(bullet_image, BULLET_SCALE)
    return bullet_image

def load_smile():
    path = os.path.join(IMAGE_DIR, 'emojione-sprite-40-people.png')
    ss = SpriteSheet(path)
    smile = ss.image_at((5, 15))
    smile = pygame.transform.scale(smile, SMILE_SCALE)
    return smile

def load_wink():
    path = os.path.join(IMAGE_DIR, 'emojione-sprite-40-people.png')
    ss = SpriteSheet(path)
    wink = ss.image_at((6, 13))
    wink = pygame.transform.scale(wink, SMILE_SCALE)
    return wink

def load_cryer_1():
    path = os.path.join(IMAGE_DIR, 'emojione-sprite-40-people.png')
    ss = SpriteSheet(path)
    img = ss.image_at((3, 14))
    img = pygame.transform.scale(img, SMILE_SCALE)
    return img

def load_cryer_2():
    path = os.path.join(IMAGE_DIR, 'emojione-sprite-40-people.png')
    ss = SpriteSheet(path)
    img = ss.image_at((14, 13))
    img = pygame.transform.scale(img, SMILE_SCALE)
    return img

def load_tear():
    path = os.path.join(IMAGE_DIR, 'emojione-sprite-40-nature.png')
    ss = SpriteSheet(path)
    img = ss.image_at((7, 10))
    img = pygame.transform.scale(img, BULLET_SCALE)
    return img

def load_devil():
    path = os.path.join(IMAGE_DIR, 'emojione-sprite-40-people.png')
    ss = SpriteSheet(path)
    img = ss.image_at((5, 13))
    img = pygame.transform.scale(img, SMILE_SCALE)
    return img