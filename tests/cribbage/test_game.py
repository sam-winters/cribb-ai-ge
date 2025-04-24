from src.cribbage.game import Game
from src.cribbage.player import Player
from src.cribbage.cards import Card, Suit
import pytest

def test_discard_to_crib_2_player():
    """Test that in a 2-player game, each player must discard exactly 2 cards."""
    # Create a 2-player game
    players = [Player("Alice"), Player("Bob")]
    game = Game(players)
    game.start()
    
    # Get the first player
    player = players[0]
    
    # Get the cards that were dealt
    cards = player.get_playable_cards()
    assert len(cards) == 6  # Should have 6 cards in 2-player game
    
    # Try to discard 1 card (should fail)
    assert not game.discard_to_crib(player, [cards[0]])
    
    # Try to discard 3 cards (should fail)
    assert not game.discard_to_crib(player, cards[:3])
    
    # Try to discard 2 cards (should succeed)
    assert game.discard_to_crib(player, cards[:2])
    
    # Verify cards were removed from player's hand
    remaining_cards = player.get_playable_cards()
    assert len(remaining_cards) == 4
    assert cards[0] not in remaining_cards
    assert cards[1] not in remaining_cards

def test_discard_to_crib_3_player():
    """Test that in a 3-player game, each player must discard exactly 1 card."""
    # Create a 3-player game
    players = [Player("Alice"), Player("Bob"), Player("Charlie")]
    game = Game(players)
    game.start()
    
    # Get the first player
    player = players[0]
    
    # Get the cards that were dealt
    cards = player.get_playable_cards()
    assert len(cards) == 5  # Should have 5 cards in 3-player game
    
    # Try to discard 2 cards (should fail)
    assert not game.discard_to_crib(player, cards[:2])
    
    # Try to discard 0 cards (should fail)
    assert not game.discard_to_crib(player, [])
    
    # Try to discard 1 card (should succeed)
    assert game.discard_to_crib(player, [cards[0]])
    
    # Verify card was removed from player's hand
    remaining_cards = player.get_playable_cards()
    assert len(remaining_cards) == 4
    assert cards[0] not in remaining_cards

def test_discard_to_crib_invalid_cards():
    """Test that discarding cards not in player's hand fails."""
    # Create a 2-player game
    players = [Player("Alice"), Player("Bob")]
    game = Game(players)
    game.start()
    
    # Get the first player
    player = players[0]
    
    # Get the cards that were dealt
    player_cards = player.get_playable_cards()
    assert len(player_cards) == 6  # Should have 6 cards in 2-player game
    
    # Create some invalid cards (not in player's hand)
    invalid_cards = [
        Card(3, Suit.HEARTS),  # Three
        Card(4, Suit.HEARTS)   # Four
    ]
    
    # Try to discard cards not in player's hand (should fail)
    assert not game.discard_to_crib(player, invalid_cards)
    
    # Try to discard one valid and one invalid card (should fail)
    assert not game.discard_to_crib(player, [player_cards[0], invalid_cards[0]])
    
    # Try to discard valid cards (should succeed)
    assert game.discard_to_crib(player, player_cards[:2])
    
    # Verify cards were removed from player's hand
    remaining_cards = player.get_playable_cards()
    assert len(remaining_cards) == 4
    assert player_cards[0] not in remaining_cards
    assert player_cards[1] not in remaining_cards

def test_discard_to_crib_no_current_round():
    """Test that discarding fails when there is no current round."""
    # Create a 2-player game
    players = [Player("Alice"), Player("Bob")]
    game = Game(players)
    
    # Don't start the game, so there's no current round
    player = players[0]
    cards = [Card(1, Suit.HEARTS), Card(2, Suit.HEARTS)]
    
    # Try to discard cards (should fail)
    assert not game.discard_to_crib(player, cards) 