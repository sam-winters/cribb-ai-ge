import pytest
from src.cribbage.cards import Card, Suit
from src.cribbage.scorer import Scorer

def test_hand_size_validation():
    """Test that scoring requires exactly 4 cards in hand."""
    # Too few cards
    print("testing too few cards")
    hand = [Card(10, Suit.HEARTS), Card(5, Suit.HEARTS)]
    starter = Card(2, Suit.HEARTS)
    with pytest.raises(ValueError):
        Scorer.score_hand(hand, starter)
        
    # Too many cards
    print("testing too many cards")
    hand = [Card(10, Suit.HEARTS), Card(5, Suit.HEARTS), 
            Card(2, Suit.HEARTS), Card(3, Suit.HEARTS), Card(4, Suit.HEARTS)]
    starter = Card(2, Suit.HEARTS)
    with pytest.raises(ValueError):
        Scorer.score_hand(hand, starter)

def test_score_15s():
    """Test scoring combinations that add up to 15."""
    # Two cards that add to 15
    hand = [Card(10, Suit.HEARTS), Card(5, Suit.DIAMONDS), 
            Card(1, Suit.CLUBS), Card(3, Suit.SPADES)]
    starter = Card(8, Suit.HEARTS)
    assert Scorer.score_hand(hand, starter) == 2  # 10+5 = 15
    
    # Three cards that add to 15
    hand = [Card(7, Suit.HEARTS), Card(6, Suit.DIAMONDS), 
            Card(1, Suit.CLUBS), Card(2, Suit.SPADES)]
    starter = Card(12, Suit.HEARTS)
    assert Scorer.score_hand(hand, starter) == 2  # 7+6+2 = 15
    
    # Multiple combinations
    hand = [Card(5, Suit.HEARTS), Card(5, Suit.DIAMONDS), 
            Card(5, Suit.CLUBS), Card(2, Suit.SPADES)]
    starter = Card(10, Suit.HEARTS)
    assert Scorer.score_hand(hand, starter) == 14  # Three 5+10 combinations + 5+5+5 + 3 of a kind

def test_score_pairs():
    """Test scoring pairs."""
    # One pair
    hand = [Card(5, Suit.HEARTS), Card(5, Suit.DIAMONDS), 
            Card(1, Suit.HEARTS), Card(6, Suit.HEARTS)]
    starter = Card(2, Suit.CLUBS)
    assert Scorer.score_hand(hand, starter) == 2
    
    # Two pairs
    hand = [Card(5, Suit.HEARTS), Card(5, Suit.DIAMONDS), 
            Card(6, Suit.HEARTS), Card(6, Suit.DIAMONDS)]
    starter = Card(2, Suit.HEARTS)
    assert Scorer.score_hand(hand, starter) == 4
    
    # Three of a kind
    hand = [Card(4, Suit.HEARTS), Card(4, Suit.DIAMONDS), 
            Card(4, Suit.CLUBS), Card(2, Suit.HEARTS)]
    starter = Card(10, Suit.HEARTS)
    assert Scorer.score_hand(hand, starter) == 6  # Three pairs

    # Test where the pair comes from the starter card
    hand = [Card(9, Suit.HEARTS), Card(5, Suit.DIAMONDS), 
            Card(2, Suit.HEARTS), Card(3, Suit.HEARTS)]
    starter = Card(9, Suit.CLUBS)
    assert Scorer.score_hand(hand, starter) == 2

def test_score_runs():
    """Test scoring runs."""
    # Run of 3
    hand = [Card(5, Suit.HEARTS), Card(6, Suit.HEARTS), 
            Card(7, Suit.HEARTS), Card(1, Suit.DIAMONDS)]
    starter = Card(2, Suit.CLUBS)
    assert Scorer.score_hand(hand, starter) == 7 # run of 3 + 1+2+7+5(15) + 1+6+7(15)
    
    # Run of 4
    hand = [Card(5, Suit.HEARTS), Card(6, Suit.HEARTS), 
            Card(7, Suit.HEARTS), Card(8, Suit.DIAMONDS)]
    starter = Card(2, Suit.HEARTS)
    assert Scorer.score_hand(hand, starter) == 10  # 4 points for run + 6 points for three 15s (7+8, 5+6+4, 5+7+3)

    # Run of 5
    hand = [Card(13, Suit.HEARTS), Card(12, Suit.HEARTS), 
            Card(11, Suit.CLUBS), Card(10, Suit.DIAMONDS)]
    starter = Card(9, Suit.HEARTS)
    assert Scorer.score_hand(hand, starter) == 5
    
    # Double run of 3
    hand = [Card(5, Suit.HEARTS), Card(5, Suit.DIAMONDS), 
            Card(6, Suit.HEARTS), Card(7, Suit.HEARTS)]
    starter = Card(2, Suit.HEARTS)
    assert Scorer.score_hand(hand, starter) == 10  # Two runs of 3 plus pair

    # bug case from validation 3♦ 6♠ 3♣ 7♦ with starter 5♥
    hand = [Card(3, Suit.DIAMONDS), Card(6, Suit.SPADES), 
            Card(3, Suit.CLUBS), Card(7, Suit.DIAMONDS)]
    starter = Card(5, Suit.HEARTS)
    assert Scorer.score_hand(hand, starter) == 9  # Two runs of 3 plus pair

def test_score_flush():
    """Test scoring flushes."""
    # 4-card flush in regular hand
    hand = [Card(2, Suit.HEARTS), Card(4, Suit.HEARTS), 
            Card(6, Suit.HEARTS), Card(8, Suit.HEARTS)]
    starter = Card(10, Suit.DIAMONDS)
    assert Scorer.score_hand(hand, starter) == 4

    # no flush in hand but starter matches
    hand = [Card(2, Suit.HEARTS), Card(4, Suit.HEARTS), 
            Card(6, Suit.DIAMONDS), Card(8, Suit.HEARTS)]
    starter = Card(10, Suit.HEARTS)
    assert Scorer.score_hand(hand, starter) == 0
    
    # 5-card flush in regular hand
    hand = [Card(2, Suit.HEARTS), Card(4, Suit.HEARTS), 
            Card(6, Suit.HEARTS), Card(8, Suit.HEARTS)]
    starter = Card(10, Suit.HEARTS)
    assert Scorer.score_hand(hand, starter) == 5
    
    # 4-card flush in crib (should score 0)
    hand = [Card(2, Suit.HEARTS), Card(4, Suit.HEARTS), 
            Card(6, Suit.HEARTS), Card(8, Suit.HEARTS)]
    starter = Card(10, Suit.DIAMONDS)
    assert Scorer.score_hand(hand, starter, is_crib=True) == 0
    
    # 5-card flush in crib
    hand = [Card(2, Suit.HEARTS), Card(4, Suit.HEARTS), 
            Card(6, Suit.HEARTS), Card(8, Suit.HEARTS)]
    starter = Card(10, Suit.HEARTS)
    assert Scorer.score_hand(hand, starter, is_crib=True) == 5

def test_score_nobs():
    """Test scoring nobs (Jack of same suit as starter)."""
    # Nobs
    hand = [Card(11, Suit.DIAMONDS), Card(9, Suit.CLUBS), 
            Card(13, Suit.HEARTS), Card(7, Suit.HEARTS)]
    starter = Card(1, Suit.DIAMONDS)
    assert Scorer.score_hand(hand, starter) == 1
    
    # No nobs
    hand = [Card(11, Suit.DIAMONDS), Card(9, Suit.CLUBS), 
            Card(13, Suit.HEARTS), Card(7, Suit.HEARTS)]
    starter = Card(1, Suit.HEARTS)
    assert Scorer.score_hand(hand, starter) == 0

def test_combination_scoring():
    """Test hands with multiple scoring combinations."""
    # Example hand: 5♥ 5♣ 5♦ J♠ (starter: 5♠)
    # Should score:
    # - Three 15s (5+J)
    # - Three pairs
    # - Four of a kind (6 pairs)
    hand = [Card(5, Suit.HEARTS), Card(5, Suit.CLUBS), 
            Card(5, Suit.DIAMONDS), Card(11, Suit.SPADES)]
    starter = Card(5, Suit.SPADES)
    assert Scorer.score_hand(hand, starter) == 29  # 6 + 12 + 0 + 0 + 0 + 11 (pairs)

def test_four_of_a_kind():
    """Test scoring four of a kind."""
    hand = [Card(1, Suit.HEARTS), Card(1, Suit.CLUBS), 
            Card(1, Suit.DIAMONDS), Card(1, Suit.SPADES)]
    starter = Card(10, Suit.HEARTS)
    assert Scorer.score_hand(hand, starter) == 12  # 6 pairs

def test_multiple_runs():
    """Test scoring with multiple runs."""
    # Two separate runs
    hand = [Card(3, Suit.HEARTS), Card(4, Suit.HEARTS), 
            Card(5, Suit.HEARTS), Card(4, Suit.DIAMONDS)]
    starter = Card(5, Suit.DIAMONDS)
    assert Scorer.score_hand(hand, starter) == 16  # Two runs of 3 plus pair

    # Overlapping runs
    hand = [Card(3, Suit.HEARTS), Card(4, Suit.CLUBS), 
            Card(5, Suit.HEARTS), Card(6, Suit.HEARTS)]
    starter = Card(7, Suit.DIAMONDS)
    assert Scorer.score_hand(hand, starter) == 9  # One run of 5

def test_all_face_cards():
    """Test scoring with all face cards."""
    hand = [Card(11, Suit.HEARTS), Card(12, Suit.HEARTS), 
            Card(13, Suit.HEARTS), Card(11, Suit.DIAMONDS)]
    starter = Card(12, Suit.CLUBS)
    assert Scorer.score_hand(hand, starter) == 16  # Two pairs

def test_nobs_and_flush_and_run():
    """Test scoring with both nobs and flush and run."""
    hand = [Card(11, Suit.HEARTS), Card(2, Suit.HEARTS), 
            Card(3, Suit.HEARTS), Card(4, Suit.HEARTS)]
    starter = Card(5, Suit.HEARTS)
    assert Scorer.score_hand(hand, starter) == 14  # 5-card flush + nobs + run of 4

def test_complex_combinations():
    """Test scoring with multiple complex combinations."""
    # Hand: 5♥ 5♣ 6♦ 7♠ (starter: 8♥)
    # Should score:
    # - One 15 (7+8)
    # - One pair (5s)
    # - Two runs of 4 (5-6-7-8)
    hand = [Card(5, Suit.HEARTS), Card(5, Suit.CLUBS), 
            Card(6, Suit.DIAMONDS), Card(7, Suit.SPADES)]
    starter = Card(8, Suit.HEARTS)
    assert Scorer.score_hand(hand, starter) == 12  # 2 + 2 + 3 