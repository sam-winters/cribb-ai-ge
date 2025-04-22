from typing import List, Optional
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
        
    def play_card(self, player: Player, card: Card) -> int:
        """
        Attempt to play a card. Returns the new count or -1 if the play is invalid.
        """
        return self.board.add_to_play_area(card)
        
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