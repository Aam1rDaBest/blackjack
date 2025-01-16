from .hand import Hand

class Player:
    def __init__(self):
        """Initialises player properties."""
        
        self.hand = Hand()
        self.status = 'playing'

    def add_card_to_hand(self, card):
        """Add card to player's hand."""
        
        self.hand.add_card(card)

    def hand_value(self):
        """Calculate player's hand value."""
        
        return self.hand.calculate_value()

    def __str__(self):
        """String method for player's hand."""
        
        return f"Hand: {self.hand} (Value: {self.hand_value()})"