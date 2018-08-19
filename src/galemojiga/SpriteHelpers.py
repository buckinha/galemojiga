import os
import pygame
from galemojiga.globals import IMAGE_DIR
from galemojiga.SpriteSheet import SpriteSheet
import galemojiga.colors as colors
import galemojiga.globals as globals


def crop(img, rect):
    small_img = pygame.Surface(rect.size)
    small_img.set_colorkey(colors.TRANSPARENT)
    small_img.blit(source=img, dest=(0,0), area=rect)
    return small_img

def load_ship_p1():
    path = os.path.join(IMAGE_DIR, 'emojione-sprite-40-travel.png')
    ss = SpriteSheet(path)
    ship_image = ss.image_at((0, 7))
    ship_image = pygame.transform.rotate(ship_image, 45)
    return ship_image

def load_orange_bullet():
    path = os.path.join(IMAGE_DIR, 'emojione-sprite-40-symbols.png')
    ss = SpriteSheet(path)
    img = ss.image_at((11,10))
    img = pygame.transform.smoothscale(img, globals.BULLET_SCALE)
    # crop it
    inner_rect = pygame.Rect(4, 4, 10, 10)
    small_img = crop(img, inner_rect)
    return small_img

def load_smile():
    path = os.path.join(IMAGE_DIR, 'emojione-sprite-40-people.png')
    ss = SpriteSheet(path)
    img = ss.image_at((5, 15))
    img = pygame.transform.scale(img, globals.ENEMY_SCALE)
    return img

def load_wink():
    path = os.path.join(IMAGE_DIR, 'emojione-sprite-40-people.png')
    ss = SpriteSheet(path)
    img = ss.image_at((6, 13))
    img = pygame.transform.scale(img, globals.ENEMY_SCALE)
    return img

def load_cryer_1():
    path = os.path.join(IMAGE_DIR, 'emojione-sprite-40-people.png')
    ss = SpriteSheet(path)
    img = ss.image_at((3, 14))
    img = pygame.transform.scale(img, globals.ENEMY_SCALE)
    return img

def load_cryer_2():
    path = os.path.join(IMAGE_DIR, 'emojione-sprite-40-people.png')
    ss = SpriteSheet(path)
    img = ss.image_at((14, 13))
    img = pygame.transform.scale(img, globals.ENEMY_SCALE)
    return img

def load_tear():
    path = os.path.join(IMAGE_DIR, 'emojione-sprite-40-nature.png')
    ss = SpriteSheet(path)
    img = ss.image_at((7, 10))
    img = pygame.transform.scale(img, globals.BULLET_SCALE)
    return img

def load_devil():
    path = os.path.join(IMAGE_DIR, 'emojione-sprite-40-people.png')
    ss = SpriteSheet(path)
    img = ss.image_at((5, 13))
    img = pygame.transform.scale(img, globals.ENEMY_SCALE)
    return img