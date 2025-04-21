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
            return NotImplemented
        return self.rank == other.rank and self.suit == other.suit


class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self.reset()

    def reset(self) -> None:
        """Resets the deck to a full set of 52 cards."""
        self.cards = [
            Card(rank, suit)
            for suit in Suit
            for rank in range(1, 14)
        ]

    def shuffle(self) -> None:
        """Shuffles the deck randomly."""
        random.shuffle(self.cards)

    def draw(self) -> Optional[Card]:
        """Draws a card from the top of the deck."""
        if not self.cards:
            return None
        return self.cards.pop()

    def draw_multiple(self, count: int) -> List[Card]:
        """Draws multiple cards from the deck."""
        drawn = []
        for _ in range(count):
            card = self.draw()
            if card:
                drawn.append(card)
        return drawn

    def __len__(self) -> int:
        return len(self.cards)

    def __str__(self) -> str:
        return f"Deck({len(self.cards)} cards)" 