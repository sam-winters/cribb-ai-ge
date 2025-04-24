from typing import List, Set, Tuple
from .cards import Card
from itertools import combinations

class Scorer:
    @staticmethod
    def find_fifteens(cards: List[Card]) -> List[Tuple[Card, ...]]:
        """Find all combinations of cards that sum to 15."""
        fifteens = []
        for r in range(2, len(cards) + 1):
            for combo in combinations(cards, r):
                if sum(card.value for card in combo) == 15:
                    fifteens.append(combo)
        return fifteens

    @staticmethod
    def find_pairs(cards: List[Card]) -> List[Tuple[Card, Card]]:
        """Find all pairs of cards with the same rank."""
        pairs = []
        for i in range(len(cards)):
            for j in range(i + 1, len(cards)):
                if cards[i].rank == cards[j].rank:
                    pairs.append((cards[i], cards[j]))
        return pairs

    @staticmethod
    def find_runs(cards: List[Card]) -> List[List[Card]]:
        """Find all runs of 3 or more consecutive cards.
        
        Returns a list of all possible runs, including double runs.
        For example, with cards [3♥,4♥,5♥,4♦,5♦], there are four runs of 3:
        [3♥,4♥,5♥], [3♥,4♥,5♦], [3♥,4♦,5♥], [3♥,4♦,5♦]
        """
        # Sort cards by rank
        sorted_cards = sorted(cards, key=lambda c: c.rank)
        
        # Group cards by rank to handle duplicates
        rank_groups = {}
        for card in sorted_cards:
            if card.rank not in rank_groups:
                rank_groups[card.rank] = []
            rank_groups[card.rank].append(card)
        
        # Find all sequences of consecutive ranks
        ranks = sorted(rank_groups.keys())
        if not ranks:
            return []
            
        sequences = []
        current_seq = [ranks[0]]
        
        for i in range(1, len(ranks)):
            if ranks[i] == ranks[i-1] + 1:
                current_seq.append(ranks[i])
            else:
                if len(current_seq) >= 3:
                    sequences.append(current_seq[:])
                current_seq = [ranks[i]]
        
        if len(current_seq) >= 3:
            sequences.append(current_seq[:])
            
        # Generate all possible runs from the sequences
        runs = []
        for sequence in sequences:
            # For each rank in the sequence, get all cards of that rank
            rank_cards = [rank_groups[rank] for rank in sequence]
            # Generate all possible combinations using product
            from itertools import product
            for run_cards in product(*rank_cards):
                runs.append(list(run_cards))
                
        return runs

    @staticmethod
    def find_flush(cards: List[Card], starter: Card, is_crib: bool = False) -> int:
        """Find if there is a flush and return the points.
        
        For a regular hand:
        - 4 cards of the same suit in the hand = 4 points
        - 5 cards of the same suit (including starter) = 5 points
        
        For the crib:
        - Only 5 cards of the same suit (including starter) = 5 points
        - Otherwise = 0 points
        """
        # Count suits in the hand (excluding starter)
        suits = [card.suit for card in cards]
        suit_counts = {suit: suits.count(suit) for suit in set(suits)}
        max_count = max(suit_counts.values())
        
        if is_crib:
            # For crib, all 5 cards must match (including starter)
            if max_count == 4 and starter.suit in suit_counts and suit_counts[starter.suit] == 4:
                return 5
            return 0
        else:
            # For regular hand, either 4 cards match or all 5 match
            if max_count >= 4:
                # Check if starter matches the flush suit
                if starter.suit in suit_counts and suit_counts[starter.suit] == max_count:
                    return 5
                return 4
            return 0

    @staticmethod
    def find_nobs(cards: List[Card], starter: Card) -> bool:
        """Find if there is a nobs (Jack of the same suit as the starter)."""
        for card in cards:
            if card.rank == 11 and card.suit == starter.suit:
                return True
        return False

    @staticmethod
    def score_hand(cards: List[Card], starter: Card, is_crib: bool = False) -> int:
        """Score a hand of cards with the given starter card."""
        
        # validate the hand
        if not Scorer.is_valid_hand(cards):
            raise ValueError("Invalid hand")
        
        all_cards = cards + [starter]
        points = 0

        # Score fifteens
        fifteens = Scorer.find_fifteens(all_cards)
        points += len(fifteens) * 2

        # Score pairs
        pairs = Scorer.find_pairs(all_cards)
        points += len(pairs) * 2

        # Score runs
        runs = Scorer.find_runs(all_cards)
        if runs:
            # Count all valid runs
            points += len(runs) * len(runs[0])

        # Score flush
        points += Scorer.find_flush(cards, starter, is_crib)

        # Score nobs
        if Scorer.find_nobs(cards, starter):
            points += 1

        return points

    @staticmethod
    def is_valid_hand(cards: List[Card]) -> bool:
        """Check if the hand is valid."""

        # must have 4 cards and no duplicates
        return len(cards) == 4 and len(set(cards)) == 4
    

