import unittest
from src.cribbage.cards import Card, Suit, Deck
import pytest


class TestCard(unittest.TestCase):
    def test_card_creation(self):
        """Test that cards are created correctly."""
        card = Card(1, Suit.HEARTS)
        self.assertEqual(card.rank, 1)
        self.assertEqual(card.suit, Suit.HEARTS)

    def test_card_value(self):
        """Test that card values are calculated correctly."""
        # Test number cards
        assert Card(5, Suit.HEARTS).value == 5
        assert Card(10, Suit.HEARTS).value == 10
        
        # Test face cards
        assert Card(11, Suit.HEARTS).value == 10  # Jack
        assert Card(12, Suit.HEARTS).value == 10  # Queen
        assert Card(13, Suit.HEARTS).value == 10  # King
        
        # Test Ace
        assert Card(1, Suit.HEARTS).value == 1

    def test_card_display(self):
        """Test that cards display correctly."""
        card = Card(1, Suit.HEARTS)
        self.assertEqual(str(card), "A♥")

    def test_card_comparison(self):
        """Test card equality comparison."""
        card1 = Card(1, Suit.HEARTS)
        card2 = Card(1, Suit.HEARTS)
        card3 = Card(2, Suit.HEARTS)
        card4 = Card(1, Suit.DIAMONDS)
        
        assert card1 == card2
        assert card1 != card3
        assert card1 != card4
        assert card1 != "not a card"

    def test_card_hashing(self):
        """Test that cards can be used in sets and as dictionary keys."""
        card1 = Card(1, Suit.HEARTS)
        card2 = Card(1, Suit.HEARTS)
        card3 = Card(2, Suit.HEARTS)
        
        # Test in sets
        card_set = {card1, card2, card3}
        assert len(card_set) == 2  # card1 and card2 are equal
        
        # Test as dictionary keys
        card_dict = {card1: "value1", card3: "value3"}
        assert card_dict[card2] == "value1"  # card1 and card2 are equal
        assert card_dict[card3] == "value3"

    def test_invalid_card_creation(self):
        """Test that invalid cards cannot be created."""
        with pytest.raises(ValueError):
            Card(0, Suit.HEARTS)  # Rank too low
        with pytest.raises(ValueError):
            Card(14, Suit.HEARTS)  # Rank too high

    def test_special_rank_display(self):
        """Test display of special ranks (A, J, Q, K)."""
        assert str(Card(1, Suit.HEARTS)) == "A♥"   # Ace
        assert str(Card(11, Suit.HEARTS)) == "J♥"  # Jack
        assert str(Card(12, Suit.HEARTS)) == "Q♥"  # Queen
        assert str(Card(13, Suit.HEARTS)) == "K♥"  # King


class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()

    def test_deck_creation(self):
        """Test that a deck is created with all 52 cards."""
        self.assertEqual(len(self.deck), 52)
        self.assertEqual(len(set(self.deck)), 52)  # All cards are unique

    def test_draw_card(self):
        """Test drawing a card from the deck."""
        initial_size = len(self.deck)
        card = self.deck.draw()
        self.assertIsInstance(card, Card)
        self.assertEqual(len(self.deck), initial_size - 1)

    def test_draw_multiple(self):
        """Test drawing multiple cards from the deck."""
        cards = self.deck.draw_multiple(6)  # Standard cribbage hand size
        self.assertEqual(len(cards), 6)
        self.assertEqual(len(self.deck), 46)

    def test_shuffle(self):
        """Test that shuffling the deck randomizes the order."""
        original_order = self.deck.cards.copy()
        self.deck.shuffle()
        self.assertNotEqual(self.deck.cards, original_order)
        self.assertEqual(set(self.deck.cards), set(original_order))


if __name__ == '__main__':
    unittest.main() 