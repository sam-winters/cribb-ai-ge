from typing import List
from ..cards import Card, Suit
from ..scorer import Scorer

def explain_score(hand: List[Card], starter: Card, is_crib: bool = False) -> str:
    """
    Generate a detailed explanation of how a cribbage hand is scored.
    
    Args:
        hand: List of 4 cards in the hand
        starter: The starter card
        is_crib: Whether this is the crib (affects flush scoring)
        
    Returns:
        A string explaining the scoring breakdown
    """
    all_cards = hand + [starter]
    explanation = []

    # Print the hand in a pretty format and starter card and whether or not its a crib
    explanation.append(f"Hand: {' '.join([str(card) for card in hand])} | Starter: {starter} | Crib: {is_crib}\n")
    
    # Score 15s
    fifteens = Scorer.find_fifteens(all_cards)
    if fifteens:
        explanation.append(f"Fifteens ({len(fifteens)} for 2 points each):")
        for combo in fifteens:
            cards_str = " + ".join(str(card) for card in combo)
            explanation.append(f"  {cards_str} = 15")
        explanation.append(f"  Total: {len(fifteens) * 2} points")
    else:
        explanation.append("No fifteens")
    
    # Score pairs
    pairs = Scorer.find_pairs(all_cards)
    if pairs:
        explanation.append(f"\nPairs ({len(pairs)} for 2 points each):")
        for card1, card2 in pairs:
            explanation.append(f"  {card1} and {card2}")
        explanation.append(f"  Total: {len(pairs) * 2} points")
    else:
        explanation.append("\nNo pairs")
    
    # Score runs
    run_length, run_cards, total_runs = Scorer.find_runs(all_cards)
    if run_length > 0:
        explanation.append(f"\nRun of {run_length} ({total_runs} for {run_length} points each):")
        for card in run_cards:
            explanation.append(f"  {card}")
        explanation.append(f"  Total: {run_length * total_runs} points")
    else:
        explanation.append("\nNo runs")
    
    # Score flush
    has_flush, flush_points = Scorer.find_flush(hand, starter, is_crib)
    if has_flush:
        if is_crib:
            explanation.append(f"\n5-card flush in crib: 5 points")
        else:
            if flush_points == 5:
                explanation.append(f"\n5-card flush: 5 points")
            else:
                explanation.append(f"\n4-card flush: 4 points")
    else:
        explanation.append("\nNo flush")
    
    # Score nobs
    has_nobs, nobs_card = Scorer.find_nobs(hand, starter)
    if has_nobs:
        explanation.append(f"\nNobs (Jack of {starter.suit.value}): 1 point")
    else:
        explanation.append("\nNo nobs")
    
    # Calculate total
    total = Scorer.score_hand(hand, starter, is_crib)
    explanation.append(f"\nTotal score: {total} points")
    
    return "\n".join(explanation)

def main():
    """Example usage of the explain_score function."""   
    # Example hand
    hand = [
        Card(3, Suit.DIAMONDS),
        Card(6, Suit.SPADES),
        Card(3, Suit.CLUBS),
        Card(7, Suit.DIAMONDS)
    ]
    starter = Card(5, Suit.HEARTS)
    
    print("Regular hand scoring:")
    print(explain_score(hand, starter, is_crib=False))
    print("\nCrib scoring:")
    print(explain_score(hand, starter, is_crib=True))


    # best possible cribbage hand
    hand = [
        Card(5, Suit.HEARTS),
        Card(5, Suit.DIAMONDS),
        Card(5, Suit.CLUBS),
        Card(11, Suit.SPADES)
    ]
    starter = Card(5, Suit.SPADES)
    print("Regular hand scoring:")
    print(explain_score(hand, starter, is_crib=False))

if __name__ == "__main__":
    main() 