from typing import List, Optional, Set
from .cards import Card

class Hand:
    def __init__(self):
        self.cards = []
        self.played_cards = []
        self.discarded_cards = []
        
    def add_card(self, card: Card) -> None:
        """Add a card to the hand."""
        if len(self.cards) >= 4:
            raise ValueError("Hand cannot contain more than 4 cards")
        if card in self.cards:
            raise ValueError("Card already in hand")
        self.cards.append(card)
        
    def play_card(self, card: Card) -> Optional[Card]:
        """Play a card from the hand."""
        if card not in self.cards:
            return None
        if card in self.played_cards or card in self.discarded_cards:
            return None
        self.played_cards.append(card)
        return card
            
    def discard_card(self, card: Card) -> Optional[Card]:
        """Discard a card to the crib."""
        if card not in self.cards:
            return None
        if card in self.discarded_cards or card in self.played_cards:
            return None
        self.discarded_cards.append(card)
        return card
            
    def unplay_card(self, card: Card) -> None:
        """Unplay a card."""
        if card in self.played_cards:
            self.played_cards.remove(card)
        
    def undiscard_card(self, card: Card) -> None:
        """Undiscard a card."""
        if card in self.discarded_cards:
            self.discarded_cards.remove(card)
        
    def clear(self) -> None:
        """Clear all cards from the hand."""
        self.cards = []
        self.played_cards = []
        self.discarded_cards = []
        
    def get_cards(self) -> List[Card]:
        """Get all cards in the hand."""
        return self.cards
        
    def get_unplayed_cards(self) -> List[Card]:
        """Get all unplayed cards."""
        return [card for card in self.cards if card not in self.played_cards and card not in self.discarded_cards]
        
    def get_played_cards(self) -> List[Card]:
        """Get all played cards."""
        return self.played_cards
        
    def get_discarded_cards(self) -> List[Card]:
        """Get all discarded cards."""
        return self.discarded_cards
        
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