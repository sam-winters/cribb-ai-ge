from typing import List, Optional
from .cards import Card
from .player import Player
from .round import Round
from .board import Board

class Game:
    def __init__(self, player_names: List[str]):
        if not 2 <= len(player_names) <= 4:
            raise ValueError("Cribbage requires 2-4 players")
            
        self.players = [Player(name) for name in player_names]
        self.current_dealer_index = 0
        self.current_round: Optional[Round] = None
        
        # Set initial dealer
        self.players[self.current_dealer_index].is_dealer = True
        
    def start_round(self) -> None:
        """Start a new round of cribbage."""
        self.current_round = Round(self.players, self.current_dealer_index)
        self.current_round.start()
        
    def next_dealer(self) -> None:
        """Move to the next dealer."""
        self.current_dealer_index = (self.current_dealer_index + 1) % len(self.players)
        
    def get_current_player(self) -> Optional[Player]:
        """Get the current player."""
        if self.current_round:
            return self.current_round.get_current_player()
        return None
        
    def get_dealer(self) -> Optional[Player]:
        """Get the current dealer."""
        if self.current_round:
            return self.current_round.get_dealer()
        return None
        
    def play_card(self, player: Player, card: Card) -> int:
        """
        Attempt to play a card. Returns the new count or -1 if the play is invalid.
        """
        if self.current_round:
            return self.current_round.play_card(player, card)
        return -1
        
    def is_game_over(self) -> bool:
        """Check if any player has won the game."""
        return any(player.score >= Board.WINNING_SCORE for player in self.players)
        
    def get_winner(self) -> Optional[Player]:
        """Get the winning player if the game is over."""
        for player in self.players:
            if player.score >= Board.WINNING_SCORE:
                return player
        return None
        
    def __str__(self) -> str:
        game_state = [f"Game State:"]
        for player in self.players:
            dealer_status = " (Dealer)" if player.is_dealer else ""
            current_status = " *" if player == self.get_current_player() else ""
            game_state.append(f"{player}{dealer_status}{current_status}")
        if self.current_round:
            game_state.append(str(self.current_round))
        return "\n".join(game_state) 