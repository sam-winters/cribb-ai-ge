import unittest
from src.game.player import Player

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player(name="Test Player")

    def test_initial_hand_empty(self):
        self.assertEqual(len(self.player.hand), 0)

    def test_play_card(self):
        self.player.hand = ['5H', '7D', '9C']
        card_to_play = '7D'
        self.player.play_card(card_to_play)
        self.assertNotIn(card_to_play, self.player.hand)

    def test_calculate_score(self):
        self.player.hand = ['5H', '5D', '7C', '9C']
        score = self.player.calculate_score()
        self.assertEqual(score, 2)  # Assuming pairs score 2 points

if __name__ == '__main__':
    unittest.main()