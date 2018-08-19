import pygame

class GameObject:

    def __init__(self):
        self.position = [0, 0]
        self.hit_scale = [0,0]

    @property
    def rect(self):
        # TODO shouldn't instantiate this every time.
        return pygame.Rect((self.position), (41, 41))

    @property
    def hit_rect(self):
        return self.rect.inflate(*self.hit_scale)


class Bullet(GameObject):
    def __init__(self, game_context, position, speed, launched_by,
                 strength, image='orange_bullet'):
        super().__init__()
        self.position = position

        # if speed is a tuple or list, use both items, otherwise, assume it's numeric
        if hasattr(speed, '__iter__'):
            self.speed_vertical = speed[0]
            self.speed_horizontal = speed[1]
        else:
            self.speed_vertical = speed
            self.speed_horizontal = 0

        self.launched_by = launched_by
        self.strength = strength

        self.image = image
        self.dead = False

    def update(self):
        self.position[0] += self.speed_vertical
        self.position[1] += self.speed_horizontal

    def hit_by(self, anything):
        self.dead = True
        self.strength = 0