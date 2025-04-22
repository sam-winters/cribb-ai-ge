from typing import List, Optional, Set
from .cards import Card

class Hand:
    def __init__(self):
        self.cards: List[Card] = []
        self.played_cards: Set[Card] = set()
        self.discarded_cards: Set[Card] = set()
        
    def add_card(self, card: Card) -> None:
        """Add a card to the hand."""
        self.cards.append(card)
        
    def play_card(self, card: Card) -> Optional[Card]:
        """
        Mark a card as played and return it if it exists in the hand and hasn't been played or discarded.
        Returns None if the card is not in the hand or has already been played/discarded.
        """
        if card in self.cards and card not in self.played_cards and card not in self.discarded_cards:
            self.played_cards.add(card)
            return card
        return None
            
    def discard_card(self, card: Card) -> Optional[Card]:
        """
        Mark a card as discarded and return it if it exists in the hand and hasn't been played or discarded.
        Returns None if the card is not in the hand or has already been played/discarded.
        """
        if card in self.cards and card not in self.played_cards and card not in self.discarded_cards:
            self.discarded_cards.add(card)
            return card
        return None
            
    def unplay_card(self, card: Card) -> None:
        """Unmark a card as played (useful for game state reversion)."""
        self.played_cards.discard(card)
        
    def undiscard_card(self, card: Card) -> None:
        """Unmark a card as discarded (useful for game state reversion)."""
        self.discarded_cards.discard(card)
        
    def clear(self) -> None:
        """Clear all cards from the hand and reset played/discarded cards."""
        self.cards = []
        self.played_cards.clear()
        self.discarded_cards.clear()
        
    def get_cards(self) -> List[Card]:
        """Return a list of all cards in the hand."""
        return self.cards.copy()
        
    def get_unplayed_cards(self) -> List[Card]:
        """Return a list of cards that haven't been played or discarded yet."""
        return [card for card in self.cards 
                if card not in self.played_cards and card not in self.discarded_cards]
        
    def get_played_cards(self) -> List[Card]:
        """Return a list of cards that have been played."""
        return list(self.played_cards)
        
    def get_discarded_cards(self) -> List[Card]:
        """Return a list of cards that have been discarded to the crib."""
        return list(self.discarded_cards)
        
    def count_points(self) -> int:
        """Count points in the hand. To be implemented with cribbage scoring rules."""
        # TODO: Implement cribbage scoring rules
        return 0
        
    def __len__(self) -> int:
        """Return the total number of cards in the hand (played, discarded, and unplayed)."""
        return len(self.cards)
        
    def __str__(self) -> str:
        """Display the hand, marking played cards with an asterisk (*) and discarded cards with a caret (^)."""
        card_strings = []
        for card in self.cards:
            if card in self.played_cards:
                card_strings.append(f"{card}*")
            elif card in self.discarded_cards:
                card_strings.append(f"{card}^")
            else:
                card_strings.append(str(card))
        return " ".join(card_strings) 