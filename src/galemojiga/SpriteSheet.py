# From https://www.pygame.org/wiki/Spritesheet
# Edited for py3, and for style/formatting


import os
import pygame
from pygame.locals import *
import galemojiga.colors as colors
import galemojiga.globals as globals


class SpriteSheet(object):
    def __init__(self, filename, tile_size=(41, 41)):
        fname = os.path.join(globals.IMAGE_DIR, filename)
        try:
            if not os.path.exists(fname):
               print(os.listdir(os.path.split(fname)[0]))
            self.sheet = pygame.image.load(fname)
            self.sheet.set_colorkey(colors.TRANSPARENT)

        except pygame.error as e:
            print('Unable to load spritesheet image: {}'.format(fname))
            print(e)
            raise SystemExit

        self.tile_size = tile_size

    @property
    def tile_width(self):
        return self.tile_size[0]

    @property
    def tile_height(self):
        return self.tile_size[1]

    # Load a specific image from a specific rectangle
    def _image_at_coords(self, rectangle):
        image = pygame.Surface(rectangle.size)
        image.set_colorkey(colors.TRANSPARENT)
        image.blit(source=self.sheet, dest=(0,0), area=rectangle)
        return image

    def image_at(self, tile_coords):
        x = tile_coords[0] * self.tile_width
        y = tile_coords[1] * self.tile_height
        r = pygame.Rect(x, y, self.tile_width, self.tile_height)
        return self._image_at_coords(r)
