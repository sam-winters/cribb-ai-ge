import unittest
from src.game.scoring import count_pairs, count_runs, count_fifteens

class TestScoring(unittest.TestCase):

    def test_count_pairs(self):
        hand = ['5', '5', '7', '8']
        self.assertEqual(count_pairs(hand), 2)

    def test_count_runs(self):
        hand = ['3', '4', '5', '6']
        self.assertEqual(count_runs(hand), 4)

    def test_count_fifteens(self):
        hand = ['5', '5', '5', '5']
        self.assertEqual(count_fifteens(hand), 8)

if __name__ == '__main__':
    unittest.main()