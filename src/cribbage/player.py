from typing import List, Optional
from .cards import Card
from .hand import Hand

class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand = Hand()
        self.score = 0
        self.is_dealer = False
        
    def receive_card(self, card: Card) -> None:
        """Add a card to the player's hand."""
        self.hand.add_card(card)
        
    def play_card(self, card: Card) -> Optional[Card]:
        """Play a card from the player's hand."""
        return self.hand.play_card(card)
        
    def discard_card(self, card: Card) -> Optional[Card]:
        """Discard a card from the player's hand to the crib."""
        return self.hand.discard_card(card)
        
    def get_playable_cards(self) -> List[Card]:
        """Get list of cards that haven't been played or discarded yet."""
        return self.hand.get_unplayed_cards()
        
    def get_discarded_cards(self) -> List[Card]:
        """Get list of cards that have been discarded to the crib."""
        return self.hand.get_discarded_cards()
        
    def add_points(self, points: int) -> None:
        """Add points to the player's score."""
        self.score += points
        
    def get_score(self) -> int:
        """Get the player's current score."""
        return self.score
        
    def clear_hand(self) -> None:
        """Clear the player's hand."""
        self.hand.clear()
        
    def __str__(self) -> str:
        return f"{self.name} (Score: {self.score})" 