class Card:
    SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank} of {self.suit}"


import random

class Deck:
    def __init__(self):
        self.cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]
        self.reset()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, number):
        return [self.cards.pop() for _ in range(number)]

    def reset(self):
        self.shuffle()
        self.cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]