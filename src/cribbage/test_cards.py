import unittest
from .cards import Card, Suit, Deck


class TestCard(unittest.TestCase):
    def test_card_creation(self):
        card = Card(1, Suit.HEARTS)
        self.assertEqual(card.rank, 1)
        self.assertEqual(card.suit, Suit.HEARTS)

    def test_card_value(self):
        # Test face cards
        king = Card(13, Suit.SPADES)
        self.assertEqual(king.value, 10)
        queen = Card(12, Suit.HEARTS)
        self.assertEqual(queen.value, 10)
        jack = Card(11, Suit.DIAMONDS)
        self.assertEqual(jack.value, 10)

        # Test number cards
        five = Card(5, Suit.CLUBS)
        self.assertEqual(five.value, 5)

    def test_card_display(self):
        ace = Card(1, Suit.HEARTS)
        self.assertEqual(str(ace), "A♥")
        king = Card(13, Suit.SPADES)
        self.assertEqual(str(king), "K♠")
        ten = Card(10, Suit.DIAMONDS)
        self.assertEqual(str(ten), "10♦")


class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()

    def test_deck_creation(self):
        self.assertEqual(len(self.deck), 52)

    def test_draw_card(self):
        initial_size = len(self.deck)
        card = self.deck.draw()
        self.assertIsInstance(card, Card)
        self.assertEqual(len(self.deck), initial_size - 1)

    def test_draw_multiple(self):
        cards = self.deck.draw_multiple(6)  # Standard cribbage hand size
        self.assertEqual(len(cards), 6)
        self.assertEqual(len(self.deck), 46)

    def test_shuffle(self):
        # Note: This test could theoretically fail even with correct implementation
        # due to the random nature of shuffling
        original_order = self.deck.cards.copy()
        self.deck.shuffle()
        self.assertNotEqual(self.deck.cards, original_order)


if __name__ == '__main__':
    unittest.main() 