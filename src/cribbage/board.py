from typing import List, Optional, Set
from .cards import Card

class Board:
    WINNING_SCORE = 121
    
    def __init__(self):
        self.play_area: List[Card] = []  # Cards currently in play
        self.play_count = 0  # Current count during play phase
        self.starter_card: Optional[Card] = None
        self.crib: List[Card] = []
        self.players_said_go: Set[int] = set()  # Track which players have said "go"
        
    def add_to_play_area(self, card: Card) -> int:
        """
        Add a card to the play area and return the new count.
        Returns -1 if adding the card would exceed 31.
        """
        if self.play_count + card.value > 31:
            return -1
            
        self.play_area.append(card)
        self.play_count += card.value
        return self.play_count
        
    def player_says_go(self, player_index: int) -> None:
        """Record that a player has said "go"."""
        self.players_said_go.add(player_index)
        
    def reset_play_area(self) -> None:
        """Reset the play area and count for a new round of play."""
        self.play_area = []
        self.play_count = 0
        self.players_said_go = set()
        
    def is_play_round_over(self, num_players: int) -> bool:
        """Check if the current round of play is over (all players have said "go")."""
        return len(self.players_said_go) == num_players
        
    def has_player_said_go(self, player_index: int) -> bool:
        """Check if a player has already said "go"."""
        return player_index in self.players_said_go
        
    def set_starter_card(self, card: Card) -> None:
        """Set the starter card (cut card)."""
        self.starter_card = card
        
    def add_to_crib(self, card: Card) -> None:
        """Add a card to the crib."""
        self.crib.append(card)
        
    def set_crib_card(self, card: Card) -> None:
        """Set a card directly to the crib (used in 3-player games)."""
        self.crib.append(card)
        
    def clear_play_area(self) -> None:
        """Clear the play area for a new round."""
        self.play_area = []
        self.play_count = 0
        self.players_said_go = set()
        
    def clear_crib(self) -> None:
        """Clear the crib."""
        self.crib = []
        
    def get_play_count(self) -> int:
        """Get the current play count."""
        return self.play_count
        
    def get_play_area_cards(self) -> List[Card]:
        """Get the cards currently in the play area."""
        return self.play_area.copy()
        
    def get_crib_cards(self) -> List[Card]:
        """Get the cards currently in the crib."""
        return self.crib.copy()
        
    def __str__(self) -> str:
        play_area_str = " ".join(str(card) for card in self.play_area)
        starter = str(self.starter_card) if self.starter_card else "None"
        return f"Play Area: {play_area_str} (Count: {self.play_count})\nStarter: {starter}" 