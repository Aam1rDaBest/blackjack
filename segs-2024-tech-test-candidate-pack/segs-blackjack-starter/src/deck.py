import random
from .card import Card

class Deck:
    def __init__(self):
        """Initialise the deck."""
        
        self.cards= self.create_deck()
    
    def create_deck(self):
        """Builds deck as list of cards."""
        
        # Cards are formed by suits and rank
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Queen', 'King', 'Jack', 'Ace']
        cards = [Card(s, r) for s in suits for r in ranks]
        return cards

    def shuffle(self):
        """Shuffle the deck."""
        
        random.shuffle(self.cards)
    
    def draw_card(self):
        """Draw a card from the deck."""
        
        if not self.cards:
            raise ValueError("No cards left in the deck")
        return self.cards.pop()
    
    def draw_visual_stack(self, screen, card_back_image, x, y):
        """Display the deck stack (back of cards)."""
        
        screen.blit(card_back_image, (x, y))

    