class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []

    def add_card(self, card):
        self.hand.append(card)

    def play_card(self, card):
        if card in self.hand:
            self.hand.remove(card)
            return card
        raise ValueError("Card not in hand")

    def calculate_score(self, scoring_rules):
        # Implement scoring logic based on cribbage rules
        score = 0
        # Example scoring logic can be added here
        return score

    def reset_hand(self):
        self.hand = []