from typing import List, Optional
from .cards import Card, Suit
from .player import Player
from .game import Game
import random

def simulate_game(player_names: List[str]) -> None:
    """Simulate a complete game of cribbage between the given players."""
    # Create players
    players = [Player(name) for name in player_names]
    game = Game(players)
    game.start()
    
    print("Starting new game of cribbage!")
    print(game)
    
    while not game.is_game_over():
        # Discard phase
        print("\nDiscard phase:")
        for player in game.players:
            # In 3-player games, each player discards 1 card
            # In 2-player games, each player discards 2 cards
            num_discards = 1 if len(players) == 3 else 2
            cards = random.sample(player.get_playable_cards(), num_discards)
            game.discard_to_crib(player, cards)
            print(f"{player.name} discarded {', '.join(str(card) for card in cards)} to the crib")
            
        # Play phase
        print("\nPlay phase:")
        while not game.current_round.is_round_over():
            current_player = game.current_round.get_current_player()
            playable_cards = current_player.get_playable_cards()
            
            # Find valid plays
            valid_plays = []
            for card in playable_cards:
                if game.current_round.board.play_count + card.value <= 31:
                    valid_plays.append(card)
                    
            if valid_plays:
                # Play a random valid card
                card = random.choice(valid_plays)
                game.play_card(current_player, card)
                print(f"{current_player.name} played {card}")
            else:
                # Say "go" if no valid plays
                game.player_says_go(current_player)
                print(f"{current_player.name} says 'go'")
                
        # Score phase
        print("\nScoring phase:")
        game.score_hands()
        print(game)
        
        # Advance to next round
        game.advance_round()
        
    # Game over
    winner = game.get_winner()
    print(f"\nGame over! {winner.name} wins with {winner.score} points!")

if __name__ == "__main__":
    # Example usage with 2 players
    print("=== 2 Player Game ===")
    simulate_game(["Alice", "Bob"])
    
    # Example usage with 3 players
    print("\n=== 3 Player Game ===")
    simulate_game(["Alice", "Bob", "Charlie"]) 