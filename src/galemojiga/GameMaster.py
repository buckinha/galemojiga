import sys
import time
import os
import pygame
from galemojiga.GameInputs import get_input_dict
import galemojiga.globals
from galemojiga.game_contexts.main_game import MainGameContext
from galemojiga.game_contexts.main_menu import MainMenuContext
from galemojiga.SpriteSheet import SpriteSheet
import galemojiga.globals as globals
import galemojiga.colors as colors
import galemojiga.SpriteHelpers as sprites

class GameMaster:

    def __init__(self, window_size=galemojiga.globals.MAIN_WINDOW_SIZE):
        self.width = window_size[0]
        self.height = window_size[1]
        self.game_objects = []
        self.player_count = 1
        self.difficulty = 1

        # center the game window
        os.environ['SDL_VIDEO_CENTERED'] = '1'

        pygame.init()
        self.screen = pygame.display.set_mode(self.window_size)

        pygame.font.init()
        self.debug_font = pygame.font.SysFont('Comic Sans MS', 12)
        self.menu_font = pygame.font.SysFont('Comic Sans MS', 30)

        self.sprite_master = SpriteMaster()

        self.contexts = {
            'main_menu': MainMenuContext(self, window_size),
            'main_game': None,
            'high_score': None
        }
        self.current_context = self.contexts['main_menu']

    @property
    def window_size(self):
        return (self.width, self.height)

    def set_context(self, context_name):
        if context_name in self.contexts:
            print('Setting Context to: {}'.format(context_name))
            self.current_context = self.contexts[context_name]

    def reset_context(self, context_name):
        if context_name == 'main_menu':
            self.contexts['main_menu'] = MainMenuContext(game_master=self,
                                                         size=self.window_size)
        if context_name == 'main_game':
            self.contexts['main_game'] = MainGameContext(game_master=self,
                                                         size=self.window_size,
                                                         player_count=self.player_count,
                                                         difficulty=self.difficulty,
                                                         debug_font=self.debug_font)

    def run(self):

        while True:
            events = [e for e in pygame.event.get()]

            # check quit
            for event in events:
                if event.type == pygame.QUIT: sys.exit()

            event_dict = get_input_dict(events)

            self.current_context.update(self.screen, event_dict)

            if self.current_context.game_over:
                break

            pygame.display.flip()
            time.sleep(0.02)


class SpriteMaster:
    def __init__(self):
        self.sprite_sheets = {
            'people': SpriteSheet('emojione-sprite-40-people.png'),
            'objects': SpriteSheet('emojione-sprite-40-objects.png'),
            'food': SpriteSheet('emojione-sprite-40-food.png'),
            'nature': SpriteSheet('emojione-sprite-40-nature.png'),
            'symbols': SpriteSheet('emojione-sprite-40-symbols.png'),
            'travel': SpriteSheet('emojione-sprite-40-travel.png'),
            'activity': SpriteSheet('emojione-sprite-40-activity.png')
        }

        self.image_name_dict = {
            'heart': ['symbols', [16, 10]],
            'heart_box': ['symbols', [6, 8]],
            'coffee': ['food', [8,9]],
            'clinking_glasses': ['food', [8, 2]],
            'helicopter': ['travel', [1, 7]],
            'bomb': ['objects', [3, 4]],
            'train_0': ['travel', [2, 7]],
            'train_1': ['travel', [3, 7]],
            'p1_bullet': ['symbols', [11, 7], globals.BULLET_SCALE],
            'p2_bullet': ['symbols', [7, 15], globals.BULLET_SCALE],
            'p3_bullet': ['symbols', [8, 15], globals.BULLET_SCALE],
            'orange_bullet': ['symbols', [11, 10], globals.BULLET_SCALE],
            'smile': ['people', [5, 15]],
            'wink': ['people', [6, 13]],
            'cryer_1': ['people', [3, 14]],
            'cryer_2': ['people', [14, 13]],
            'tear': ['nature', [7, 10], globals.BULLET_SCALE],
            'devil': ['people', [5, 13]]
        }

        # add cars:
        for i in range(8):
            self.image_name_dict['car_{}'.format(i)] = ['travel', (i, 8)]

    def get_image(self, sheet, position, scale=globals.ENEMY_SCALE):
        if sheet in self.sprite_sheets:
            img = self.sprite_sheets[sheet].image_at(position)
            return pygame.transform.smoothscale(img, scale)
        else:
            return None

    def get_image_name(self, name, scale=globals.ENEMY_SCALE):

        if 'parrot' in name:
            return self.load_party_parrot_image(name)

        if '_ship' in name:
            return self.load_player_image(name)

        if name in self.image_name_dict:
            sheet = self.image_name_dict[name][0]
            pos = self.image_name_dict[name][1]
            if len(self.image_name_dict[name]) > 2:
                scl = self.image_name_dict[name][2]
            else:
                scl = scale
            return self.get_image(sheet, pos, scl)
        else:
            raise KeyError('Key "{}" not found in SpriteMaster name dictionary'.format(name))

    def load_player_image(self, player_frame):
        # load_base_ship
        ship_image = self.get_image('travel', (0, 7), globals.NORMAL_SCALE)
        ship_image = pygame.transform.rotate(ship_image, 45)

        # add bullet for color
        if player_frame == 'p1_ship':
            bullet = self.get_image_name('p1_bullet')
        elif player_frame == 'p2_ship':
            bullet = self.get_image_name('p2_bullet')
        else:
            bullet = self.get_image_name('p3_bullet')
        ship_image.blit(source=bullet, dest=(21, 15))
        return ship_image

    def load_party_parrot_image(self, parrot_frame):
        path = os.path.join(globals.IMAGE_DIR, '{}.png'.format(parrot_frame))
        img = load_image(path).convert()
        img.set_colorkey(colors.TRANSPARENT)
        return pygame.transform.smoothscale(img, (25,25))


def load_image(filename):
    try:
        if not os.path.exists(filename):
            print(os.listdir(os.path.split(filename)[0]))
        img = pygame.image.load(filename)
        img.set_colorkey(colors.TRANSPARENT)
        return img

    except pygame.error as e:
        print('Unable to load spritesheet image: {}'.format(filename))
        print(e)
        raise SystemExit

if __name__ == "__main__":
    game = GameMaster()
    game.run()