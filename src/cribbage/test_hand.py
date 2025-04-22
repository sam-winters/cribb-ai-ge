from typing import List
import pytest
from .cards import Card, Suit
from .hand import Hand

def test_hand_initialization():
    """Test that a new hand is empty."""
    hand = Hand()
    assert len(hand) == 0
    assert hand.get_cards() == []
    assert hand.get_played_cards() == []
    assert hand.get_discarded_cards() == []
    assert hand.get_unplayed_cards() == []

def test_add_card():
    """Test adding cards to the hand."""
    hand = Hand()
    card = Card(1, Suit.HEARTS)
    hand.add_card(card)
    assert len(hand) == 1
    assert card in hand.get_cards()
    assert card in hand.get_unplayed_cards()
    assert card not in hand.get_played_cards()
    assert card not in hand.get_discarded_cards()

def test_play_card():
    """Test playing cards from the hand."""
    hand = Hand()
    card = Card(1, Suit.HEARTS)
    hand.add_card(card)
    
    # Test playing a card
    played_card = hand.play_card(card)
    assert played_card == card
    assert card in hand.get_played_cards()
    assert card not in hand.get_unplayed_cards()
    assert card in hand.get_cards()
    
    # Test playing the same card again
    played_card = hand.play_card(card)
    assert played_card is None
    
    # Test playing a card not in hand
    other_card = Card(2, Suit.HEARTS)
    played_card = hand.play_card(other_card)
    assert played_card is None

def test_discard_card():
    """Test discarding cards to the crib."""
    hand = Hand()
    card = Card(1, Suit.HEARTS)
    hand.add_card(card)
    
    # Test discarding a card
    discarded_card = hand.discard_card(card)
    assert discarded_card == card
    assert card in hand.get_discarded_cards()
    assert card not in hand.get_unplayed_cards()
    assert card in hand.get_cards()
    
    # Test discarding the same card again
    discarded_card = hand.discard_card(card)
    assert discarded_card is None
    
    # Test discarding a card not in hand
    other_card = Card(2, Suit.HEARTS)
    discarded_card = hand.discard_card(other_card)
    assert discarded_card is None

def test_play_and_discard_interaction():
    """Test that a card can't be both played and discarded."""
    hand = Hand()
    card = Card(1, Suit.HEARTS)
    hand.add_card(card)
    
    # Play the card
    hand.play_card(card)
    assert card in hand.get_played_cards()
    
    # Try to discard the played card
    discarded_card = hand.discard_card(card)
    assert discarded_card is None
    
    # Clear and try the opposite
    hand.clear()
    hand.add_card(card)
    
    # Discard the card
    hand.discard_card(card)
    assert card in hand.get_discarded_cards()
    
    # Try to play the discarded card
    played_card = hand.play_card(card)
    assert played_card is None

def test_unplay_card():
    """Test unplaying a card."""
    hand = Hand()
    card = Card(1, Suit.HEARTS)
    hand.add_card(card)
    
    # Play and then unplay the card
    hand.play_card(card)
    hand.unplay_card(card)
    
    assert card not in hand.get_played_cards()
    assert card in hand.get_unplayed_cards()
    assert card in hand.get_cards()

def test_undiscard_card():
    """Test undiscarding a card."""
    hand = Hand()
    card = Card(1, Suit.HEARTS)
    hand.add_card(card)
    
    # Discard and then undiscard the card
    hand.discard_card(card)
    hand.undiscard_card(card)
    
    assert card not in hand.get_discarded_cards()
    assert card in hand.get_unplayed_cards()
    assert card in hand.get_cards()

def test_clear():
    """Test clearing the hand."""
    hand = Hand()
    card1 = Card(1, Suit.HEARTS)
    card2 = Card(2, Suit.HEARTS)
    hand.add_card(card1)
    hand.add_card(card2)
    
    # Play and discard some cards
    hand.play_card(card1)
    hand.discard_card(card2)
    
    # Clear the hand
    hand.clear()
    
    assert len(hand) == 0
    assert hand.get_cards() == []
    assert hand.get_played_cards() == []
    assert hand.get_discarded_cards() == []
    assert hand.get_unplayed_cards() == []

def test_string_representation():
    """Test the string representation of the hand."""
    hand = Hand()
    card1 = Card(1, Suit.HEARTS)  # A♥
    card2 = Card(2, Suit.HEARTS)  # 2♥
    card3 = Card(3, Suit.HEARTS)  # 3♥
    
    hand.add_card(card1)
    hand.add_card(card2)
    hand.add_card(card3)
    
    # Initially all cards are unplayed
    assert str(hand) == "A♥ 2♥ 3♥"
    
    # Play a card
    hand.play_card(card1)
    assert str(hand) == "A♥* 2♥ 3♥"
    
    # Discard a card
    hand.discard_card(card2)
    assert str(hand) == "A♥* 2♥^ 3♥"
    
    # Play another card
    hand.play_card(card3)
    assert str(hand) == "A♥* 2♥^ 3♥*" 