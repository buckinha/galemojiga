import unittest
from galemojiga.game_objects.Effects import Scoreboard


class TestScoreboard(unittest.TestCase):

    def test_get_digits(self):
        sb = Scoreboard()
        self.assertEqual(sb.get_digits(123), [1,2,3])
        self.assertEqual(sb.get_digits(123.4), [1,2,3])
        self.assertEqual(sb.get_digits(1), [1])
        self.assertEqual(sb.get_digits(0), [0])
        self.assertEqual(sb.get_digits(-1), [0])
        self.assertEqual(sb.get_digits(9090), [9,0,9,0])
        self.assertEqual(sb.get_digits(10), [1,0])