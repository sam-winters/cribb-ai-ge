from typing import List, Optional, Tuple
from .cards import Card, Deck
from .player import Player
from .board import Board

class Round:
    def __init__(self, players: List[Player], dealer_index: int):
        self.players = players
        self.dealer_index = dealer_index
        self.board = Board()
        self.deck = Deck()
        self.current_player_index = (dealer_index + 1) % len(players)
        
        # Set dealer
        for i, player in enumerate(players):
            player.is_dealer = (i == dealer_index)
            
    def start(self) -> None:
        """Start a new round of cribbage."""
        # Reset the board
        self.board.clear_play_area()
        self.board.clear_crib()
        
        # Reset and shuffle the deck
        self.deck.reset()
        self.deck.shuffle()
        
        # Clear all hands
        for player in self.players:
            player.clear_hand()
            
        # Deal cards
        self._deal_cards()
        
        # Cut for starter
        starter = self.deck.draw()
        if starter:
            self.board.set_starter_card(starter)
            # Set starter card for all players' hands
            for player in self.players:
                player.hand.set_starter_card(starter)
                
    def _deal_cards(self) -> None:
        """Deal cards to all players."""
        cards_per_player = 6 if len(self.players) == 2 else 5
        
        for _ in range(cards_per_player):
            for player in self.players:
                card = self.deck.draw()
                if card:
                    player.receive_card(card)

        # In 3-player games, deal a card directly to the crib
        if len(self.players) == 3:
            crib_card = self.deck.draw()
            if crib_card:
                self.board.set_crib_card(crib_card)
                    
    def get_current_player(self) -> Player:
        """Get the current player."""
        return self.players[self.current_player_index]
        
    def get_dealer(self) -> Player:
        """Get the current dealer."""
        return self.players[self.dealer_index]
        
    def next_player(self) -> None:
        """Move to the next player."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        
    def play_card(self, player: Player, card: Card) -> Tuple[int, bool]:
        """
        Attempt to play a card. Returns a tuple of:
        - The new count (or -1 if the play is invalid)
        - Whether the play area should be reset (reached 31 or all players said "go")
        """
        if player != self.get_current_player():
            return -1, False
            
        new_count = self.board.add_to_play_area(card)
        if new_count == -1:
            return -1, False
            
        # Remove the card from the player's hand
        player.play_card(card)
        
        # Check if we need to reset the play area
        should_reset = False
        if new_count == 31:
            # Player gets 2 points for reaching 31 exactly
            player.add_points(2)
            should_reset = True
        elif self.board.is_play_round_over(len(self.players)):
            # Last player to play gets 1 point when all players say "go"
            player.add_points(1)
            should_reset = True
            
        if should_reset:
            self.board.reset_play_area()
        else:
            # Only move to next player if we're not resetting
            self.next_player()
            
        return new_count, should_reset
        
    def player_says_go(self, player: Player) -> bool:
        """
        Record that a player has said "go".
        Returns True if the play area should be reset (all players have said "go").
        """
        if player != self.get_current_player():
            return False
            
        self.board.player_says_go(self.current_player_index)
        self.next_player()
        
        if self.board.is_play_round_over(len(self.players)):
            self.board.reset_play_area()
            return True
        return False
        
    def is_round_over(self) -> bool:
        """Check if the round is over (all cards played)."""
        return all(len(player.get_playable_cards()) == 0 for player in self.players)
        
    def __str__(self) -> str:
        round_state = [f"Round State:"]
        for player in self.players:
            dealer_status = " (Dealer)" if player.is_dealer else ""
            current_status = " *" if player == self.get_current_player() else ""
            round_state.append(f"{player}{dealer_status}{current_status}")
        round_state.append(str(self.board))
        return "\n".join(round_state) 