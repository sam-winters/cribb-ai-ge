from typing import List, Tuple
import random
from ..cards import Card, Suit
from ..scorer import Scorer

"""
This script generates random cribbage hands and scores them.
It can be used to validate the scoring system by generating many examples
and manually checking the scores.
"""


def generate_random_hand_and_starter() -> Tuple[List[Card], Card]:
    """Generate a random hand of 4 cards and a starter card from the same deck."""
    deck = []
    for suit in Suit:
        for rank in range(1, 14):  # Ranks 1-13 (Ace through King)
            deck.append(Card(rank, suit))
    random.shuffle(deck)
    return deck[:4], deck[4]

def format_hand(hand: List[Card], starter: Card) -> str:
    """Format a hand and starter card for display."""
    hand_str = " ".join(str(card) for card in hand)
    return f"Hand: {hand_str} | Starter: {starter}"

def main():
    print("Generating 50 random hands and scoring them...\n")
    print("Format: Hand: [cards] | Starter: [card] | Regular Score: [score] | Crib Score: [score]")
    print("-" * 100)
    
    for i in range(50):
        hand, starter = generate_random_hand_and_starter()
        
        regular_score = Scorer.score_hand(hand, starter, is_crib=False)
        crib_score = Scorer.score_hand(hand, starter, is_crib=True)
        
        print(f"{i+1:2d}. {format_hand(hand, starter)} | Regular: {regular_score:2d} | Crib: {crib_score:2d}")

if __name__ == "__main__":
    main() 