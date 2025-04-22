from typing import List, Set, Tuple
from .cards import Card
from itertools import combinations

class Scorer:
    @staticmethod
    def score_hand(hand: List[Card], starter: Card, is_crib: bool = False) -> int:
        """
        Score a cribbage hand including the starter card.
        Returns the total points for the hand.
        
        Args:
            hand: List of cards in the hand (must be exactly 4 cards)
            starter: The starter card
            is_crib: Whether this is the crib (affects flush scoring)
            
        Raises:
            ValueError: If hand does not contain exactly 4 cards
        """
        if len(hand) != 4:
            raise ValueError("Hand must contain exactly 4 cards")
            
        all_cards = hand + [starter]
        points = 0
        
        # Score 15s
        points += Scorer._score_15s(all_cards)
        
        # Score pairs
        points += Scorer._score_pairs(all_cards)
        
        # Score runs
        points += Scorer._score_runs(all_cards)
        
        # Score flush
        points += Scorer._score_flush(hand, starter, is_crib)
        
        # Score nobs
        points += Scorer._score_nobs(hand, starter)
        
        return points
        
    @staticmethod
    def _score_15s(cards: List[Card]) -> int:
        """Score combinations of cards that add up to 15."""
        points = 0
        # Generate all possible combinations of 2-5 cards
        for r in range(2, len(cards) + 1):
            for combo in combinations(cards, r):
                if sum(card.value for card in combo) == 15:
                    points += 2
        return points
        
    @staticmethod
    def _score_pairs(cards: List[Card]) -> int:
        """Score pairs of cards with the same rank."""
        points = 0
        # Check all possible pairs using combinations to avoid double-counting
        for card1, card2 in combinations(cards, 2):
            if card1.rank == card2.rank:
                points += 2
        return points
        
    @staticmethod
    def _score_runs(cards: List[Card]) -> int:
        """Score runs of 3 or more consecutive ranks."""
        # Sort cards by rank
        sorted_ranks = sorted([card.rank for card in cards])
        
        # Find the longest possible run
        max_run_length = 0
        current_run = 1
        
        for i in range(1, len(sorted_ranks)):
            if sorted_ranks[i] == sorted_ranks[i-1] + 1:
                current_run += 1
            elif sorted_ranks[i] != sorted_ranks[i-1]:  # Skip duplicates
                max_run_length = max(max_run_length, current_run)
                current_run = 1
                
        max_run_length = max(max_run_length, current_run)
        
        # Only score if run is 3 or more
        if max_run_length >= 3:
            # Count duplicates of each rank in the run
            rank_counts = {}
            for card in cards:
                if card.rank in sorted_ranks[0:max_run_length]:
                    rank_counts[card.rank] = rank_counts.get(card.rank, 0) + 1
            
            # Multiply run length by number of possible combinations
            total_runs = 1
            for count in rank_counts.values():
                total_runs *= count
                
            return max_run_length * total_runs
        return 0
        
    @staticmethod
    def _score_flush(hand: List[Card], starter: Card, is_crib: bool = False) -> int:
        """
        Score a flush of 4 or 5 cards of the same suit.
        
        For a regular hand:
        - 4 points for 4 cards of same suit in hand
        - 5 points if starter matches suit
        
        For the crib:
        - 5 points only if all 5 cards (including starter) are same suit
        - No points for 4-card flush
        """
        if is_crib:
            # For crib, all 5 cards must be same suit
            all_cards = hand + [starter]
            if all(card.suit == all_cards[0].suit for card in all_cards):
                return 5
            return 0
        else:
            # For regular hand, check 4-card flush first
            if all(card.suit == hand[0].suit for card in hand):
                # If starter matches, score 5
                if starter.suit == hand[0].suit:
                    return 5
                # Otherwise score 4
                return 4
            return 0
        
    @staticmethod
    def _score_nobs(hand: List[Card], starter: Card) -> int:
        """Score nobs (Jack of same suit as starter)."""
        for card in hand:
            if card.rank == 11 and card.suit == starter.suit:  # Jack is rank 11
                return 1
        return 0 