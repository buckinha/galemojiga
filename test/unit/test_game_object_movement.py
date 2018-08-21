import unittest
from galemojiga.game_objects.GameObject import GameObject
import galemojiga.globals as globals


class TestMovement(unittest.TestCase):

    def setUp(self):
        self.gameobj = GameObject()
        self.gameobj.speed_h = 5
        self.gameobj.speed_v = 15
        self.gameobj.size = [30,40] # ensuring that i don't mix up these indices

    def tearDown(self):
        pass

    def test_move_up(self):

        x = 300
        y = 300
        self.gameobj.position = [x,y]
        self.gameobj._move_up_to_unit(0)
        self.assertEqual(self.gameobj.y, y-self.gameobj.speed_v)

        # move to ceiling
        self.gameobj.position = [x,y]
        for i in range(200):
            self.gameobj._move_up_to_ceiling()
        self.assertEqual(self.gameobj.y, globals.CEILING)

    def test_move_down(self):
        x = 300
        y = 300
        self.gameobj.position = [x,y]
        self.gameobj._move_down_to_unit(globals.V_UNITS)
        self.assertEqual(self.gameobj.y, y+self.gameobj.speed_v)

        # move to floor
        self.gameobj.position = [x,y]
        for i in range(300):
            self.gameobj._move_down_to_floor()
        self.assertEqual(self.gameobj.y, globals.FLOOR-self.gameobj.size[1])

    def test_move_right(self):
        x = 300
        y = 300
        self.gameobj.position = [x,y]
        self.gameobj._move_right_to_unit(globals.H_UNITS)
        self.assertEqual(self.gameobj.x, x+self.gameobj.speed_h)

        # move to wall
        self.gameobj.position = [x,y]
        for i in range(300):
            self.gameobj._move_right_to_wall()
        self.assertEqual(self.gameobj.x, globals.RIGHT_WALL-self.gameobj.size[0])

    def test_move_left(self):
        x = 300
        y = 300
        self.gameobj.position = [x,y]
        self.gameobj._move_left_to_unit(0)
        self.assertEqual(self.gameobj.x, x-self.gameobj.speed_h)

        # move to wall
        self.gameobj.position = [x,y]
        for i in range(300):
            self.gameobj._move_left_to_wall()
        self.assertEqual(self.gameobj.x, globals.LEFT_WALL)


class TestRandomMovement(unittest.TestCase):

    def setUp(self):
        self.gameobj = GameObject()
        self.gameobj.speed_h = 5
        self.gameobj.speed_v = 15
        self.gameobj.size = [30,40] # ensuring that i don't mix up these indices

    def tearDown(self):
        pass

    def test_left_random(self):
        x = 300
        y = 300
        self.gameobj.position = [x,y]
        # can never happen, since the lowest draw is 0
        self.gameobj._move_left_random(-1, 1)
        self.assertEqual(x - self.gameobj.x, self.gameobj.speed_h)

        x = 300
        y = 300
        self.gameobj.position = [x,y]
        # will always happen, because it always draws 1
        self.gameobj._move_left_random(1, 1)
        self.assertEqual(x, self.gameobj.x)

    def test_right_random(self):
        x = 300
        y = 300
        self.gameobj.position = [x,y]
        # can never happen, since the lowest draw is 0
        self.gameobj._move_right_random(-1, 1)
        self.assertEqual(self.gameobj.x - x, self.gameobj.speed_h)

        x = 300
        y = 300
        self.gameobj.position = [x,y]
        # will always happen, because it always draws 1
        self.gameobj._move_right_random(1, 1)
        self.assertEqual(x, self.gameobj.x)

    def test_up_random(self):
        x = 300
        y = 300
        self.gameobj.position = [x,y]
        # can never happen, since the lowest draw is 0
        self.gameobj._move_up_random(-1, 1)
        self.assertEqual(y - self.gameobj.y, self.gameobj.speed_v)

        x = 300
        y = 300
        self.gameobj.position = [x,y]
        # will always happen, because it always draws 1
        self.gameobj._move_up_random(1, 1)
        self.assertEqual(y, self.gameobj.y)

    def test_down_random(self):
        x = 300
        y = 300
        self.gameobj.position = [x,y]
        # can never happen, since the lowest draw is 0
        self.gameobj._move_down_random(-1, 1)
        self.assertEqual(self.gameobj.y - y, self.gameobj.speed_v)

        x = 300
        y = 300
        self.gameobj.position = [x,y]
        # will always happen, because it always draws 1
        self.gameobj._move_down_random(1, 1)
        self.assertEqual(y, self.gameobj.y)


class TestMovementByUnit(unittest.TestCase):

    def setUp(self):
        self.gameobj = GameObject()
        self.gameobj.speed_h = 5
        self.gameobj.speed_v = 15
        self.gameobj.size = [30,40] # ensuring that i don't mix up these indices

    def tearDown(self):
        pass

    def test_down_one_unit(self):
        x = 300
        y = 300
        self.gameobj.position = [x,y]
        self.gameobj.move_list = [self.gameobj._move_down_one_unit,
                                  self.gameobj._hold]
        for i in range(300):
            self.gameobj.do_move()
        self.assertEqual(self.gameobj.y - y, globals.UNIT)

    def test_up_one_unit(self):
        x = 300
        y = 300
        self.gameobj.position = [x,y]
        self.gameobj.move_list = [self.gameobj._move_up_one_unit,
                                  self.gameobj._hold]
        for i in range(300):
            self.gameobj.do_move()
        self.assertEqual(y - self.gameobj.y, globals.UNIT)

    def test_right_one_unit(self):
        x = 300
        y = 300
        self.gameobj.position = [x, y]
        self.gameobj.move_list = [self.gameobj._move_right_one_unit,
                                  self.gameobj._hold]
        for i in range(300):
            self.gameobj.do_move()
        self.assertEqual(self.gameobj.x - x, globals.UNIT)

    def test_left_one_unit(self):
        x = 300
        y = 300
        self.gameobj.position = [x, y]
        self.gameobj.move_list = [self.gameobj._move_left_one_unit,
                                  self.gameobj._hold]
        for i in range(300):
            self.gameobj.do_move()
        self.assertEqual(x - self.gameobj.x, globals.UNIT)