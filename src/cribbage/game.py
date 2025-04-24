from typing import List, Optional
from .player import Player
from .round import Round
from .cards import Card
from .scorer import Scorer

class Game:
    def __init__(self, players: List[Player]):
        self.players = players
        self.current_round: Optional[Round] = None
        self.dealer_index = 0
        
    def start(self) -> None:
        """Start a new game of cribbage."""
        # Reset all player scores
        for player in self.players:
            player.reset_score()
            
        # Start first round
        self.start_new_round()
        
    def start_new_round(self) -> None:
        """Start a new round of cribbage."""
        self.current_round = Round(self.players, self.dealer_index)
        self.current_round.start()
        
    def discard_to_crib(self, player: Player, cards: List[Card]) -> bool:
        """Discard cards to the crib. Returns True if successful."""
        if not self.current_round:
            return False
            
        # Must discard the correct number of cards
        # 2 cards in 2-player games, 1 card in 3-player games
        required_discards = 2 if len(self.players) == 2 else 1
        if len(cards) != required_discards:
            return False
            
        # Verify player has these cards
        if not all(card in player.get_playable_cards() for card in cards):
            return False
            
        # Add cards to crib
        for card in cards:
            player.discard_card(card)
            self.current_round.board.add_to_crib(card)
            
        return True
        
    def play_card(self, player: Player, card: Card) -> bool:
        """Play a card during the play phase. Returns True if successful."""
        if not self.current_round:
            return False
            
        new_count, should_reset = self.current_round.play_card(player, card)
        return new_count != -1
        
    def player_says_go(self, player: Player) -> bool:
        """Player says "go" during the play phase. Returns True if successful."""
        if not self.current_round:
            return False
            
        return self.current_round.player_says_go(player)
        
    def score_hands(self) -> None:
        """Score all hands and the crib at the end of the round."""
        if not self.current_round:
            return
            
        board = self.current_round.board
        starter = board.starter_card
        
        # Score non-dealer hands first
        for player in self.players:
            if not player.is_dealer:
                scoring_cards = player.get_scoring_cards()
                print(f"Scoring {player.name}'s hand: {scoring_cards}")
                score = Scorer.score_hand(scoring_cards, starter)
                player.add_points(score)
                
        # Score dealer's hand
        dealer = self.current_round.get_dealer()
        scoring_cards = dealer.get_scoring_cards()
        print(f"Scoring dealer's hand: {scoring_cards}")
        dealer_score = Scorer.score_hand(scoring_cards, starter)
        dealer.add_points(dealer_score)
        
        # Score crib
        crib_cards = board.get_crib_cards()
        print(f"Scoring crib: {crib_cards}")
        crib_score = Scorer.score_hand(crib_cards, starter, is_crib=True)
        dealer.add_points(crib_score)
        
    def is_game_over(self) -> bool:
        """Check if the game is over (someone reached 121 points)."""
        return any(player.score >= 121 for player in self.players)
        
    def get_winner(self) -> Optional[Player]:
        """Get the winner of the game, if any."""
        for player in self.players:
            if player.score >= 121:
                return player
        return None
        
    def advance_round(self) -> None:
        """Advance to the next round."""
        if not self.current_round:
            return
            
        # Score the hands
        self.score_hands()
        
        # Move dealer to next player
        self.dealer_index = (self.dealer_index + 1) % len(self.players)
        
        # Start new round
        self.start_new_round()
        
    def __str__(self) -> str:
        game_state = [f"Game State:"]
        for player in self.players:
            dealer_status = " (Dealer)" if player.is_dealer else ""
            game_state.append(f"{player}{dealer_status}")
        if self.current_round:
            game_state.append(str(self.current_round))
        return "\n".join(game_state) 