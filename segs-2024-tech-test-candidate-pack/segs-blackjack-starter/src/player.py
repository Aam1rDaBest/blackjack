from .hand import Hand

class Player:
    def __init__(self):
        self.hand = Hand()

    def add_card_to_hand(self, card):
        self.hand.add_card(card)

    def hand_value(self):
        return self.hand.calculate_value()

    def __str__(self):
        return f"Hand: {self.hand} (Value: {self.hand_value()})"