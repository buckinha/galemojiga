from galemojiga.game_objects.GameObject import GameObject
import galemojiga.globals as globals
import random

class PowerUp(GameObject):
    def __init__(self):
        super().__init__()

class PartyParrotLeft(GameObject):

    def __init__(self):
        super().__init__()
        self.frame_list = ['parrot_{}'.format(i) for i in range(10)]
        self.frame_rate = 0.1
        self.dead = False
        self.speed_h = 5
        self.move_list = [self._move_left_forever]
        self.x = globals.RIGHT_WALL
        self.powerup = None
        self.powerup_launched = False
        drop_width = int((globals.PLAY_WIDTH / 2) * 0.75)
        self.launch_point = globals.H_MIDDLE + random.randint(-drop_width, drop_width)

    def update(self, game_context):
        super().update()

        buffer = 50
        if self.position[0] < (0 - buffer):
            self.dead = True
        if self.position[0] > globals.MAIN_WINDOW_SIZE[0] + buffer:
            self.dead = True

        buffer = self.speed_h
        if self.powerup_launched is False:
            if self.position[0] < self.launch_point + buffer:
                if self.position[0] > self.launch_point - buffer:
                    self.powerup_launched = True
                    pup = PowerUp()
                    game_context.powerups.append(pup)

class PartyParrotRight(PartyParrotLeft):

    def __init__(self):
        super().__init__()
        self.move_list = [self._move_right_forever]
        self.x = globals.LEFT_WALL
