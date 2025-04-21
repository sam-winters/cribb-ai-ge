import unittest
from src.game.deck import Deck

class TestDeck(unittest.TestCase):

    def setUp(self):
        self.deck = Deck()

    def test_deck_initialization(self):
        self.assertEqual(len(self.deck.cards), 52)

    def test_shuffle(self):
        original_order = self.deck.cards[:]
        self.deck.shuffle()
        self.assertNotEqual(original_order, self.deck.cards)

    def test_deal(self):
        hand = self.deck.deal(5)
        self.assertEqual(len(hand), 5)
        self.assertEqual(len(self.deck.cards), 47)

    def test_reset(self):
        self.deck.shuffle()
        self.deck.deal(5)
        self.deck.reset()
        self.assertEqual(len(self.deck.cards), 52)

if __name__ == '__main__':
    unittest.main()