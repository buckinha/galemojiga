from galemojiga.game_objects.GameObject import GameObject
import galemojiga.globals as globals

class Bullet(GameObject):
    def __init__(self, game_context, position, speed, launched_by,
                 strength, image='orange_bullet'):
        super().__init__()
        self.position = position
        self.size = [12,12]

        # if speed is a tuple or list, use both items, otherwise, assume it's numeric
        if hasattr(speed, '__iter__'):
            self.speed_vertical = speed[0]
            self.speed_horizontal = speed[1]
        else:
            self.speed_vertical = speed
            self.speed_horizontal = 0

        self.launched_by = launched_by
        self.strength = strength

        self.dead = False

        self.frame_list = [image]

    def update(self, game_context):
        self.x += self.speed_vertical
        self.y += self.speed_horizontal
        self.check_dismissal()

    def check_dismissal(self):
        buffer = 50
        if self.position[1] < -buffer or self.position[1] > globals.MAIN_WINDOW_SIZE[1] + buffer:
            self.dead = True

    def hit_by(self, anything):
        self.dead = True
        self.strength = 0


class BulletTear(Bullet):
    def __init__(self, game_context, position, speed=(0,5),
                 launched_by='enemy',
                 strength=1, image='tear'):
        super().__init__(game_context=game_context,
                         position=position, speed=speed,
                         launched_by=launched_by,
                         strength=strength, image=image)

        self.size = [14, 17]
        self.hit_offset = [4, 2]
