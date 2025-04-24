from enum import Enum
from typing import List, Optional
import random


class Suit(Enum):
    HEARTS = "♥"
    DIAMONDS = "♦"
    CLUBS = "♣"
    SPADES = "♠"


class Card:
    def __init__(self, rank: int, suit: Suit):
        if not 1 <= rank <= 13:
            raise ValueError("Rank must be between 1 and 13")
        self.rank = rank
        self.suit = suit

    @property
    def value(self) -> int:
        """Returns the card's value for counting in cribbage."""
        if self.rank > 10:
            return 10
        return self.rank

    @property
    def display_rank(self) -> str:
        """Returns the display representation of the rank."""
        special_ranks = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}
        return special_ranks.get(self.rank, str(self.rank))

    def __str__(self) -> str:
        return f"{self.display_rank}{self.suit.value}"

    def __repr__(self) -> str:
        return f"Card(rank={self.rank}, suit={self.suit})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return False
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self) -> int:
        return hash((self.rank, self.suit))


class Deck:
    def __init__(self):
        self.cards = []
        for suit in Suit:
            for rank in range(1, 14):
                self.cards.append(Card(rank, suit))

    def __iter__(self):
        return iter(self.cards)

    def __len__(self):
        return len(self.cards)

    def draw(self):
        """Draw a card from the deck."""
        if not self.cards:
            raise ValueError("Deck is empty")
        return self.cards.pop()

    def draw_multiple(self, count):
        """Draw multiple cards from the deck."""
        if count > len(self.cards):
            raise ValueError("Not enough cards in deck")
        return [self.cards.pop() for _ in range(count)]

    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.cards)
        
    def reset(self) -> None:
        """Reset the deck to a full, unshuffled state."""
        self.cards = []
        for suit in Suit:
            for rank in range(1, 14):
                self.cards.append(Card(rank, suit))

    def __str__(self) -> str:
        return f"Deck({len(self.cards)} cards)" 