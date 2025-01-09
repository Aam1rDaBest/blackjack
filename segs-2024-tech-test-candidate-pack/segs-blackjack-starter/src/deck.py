import random
from .card import Card
import pygame

class Deck:
    def __init__(self):
        self.cards= self.create_deck()
    
    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        cards = [Card(s, r) for s in suits for r in ranks]
        return cards

    def shuffle(self):
        random.shuffle(self.cards)
    
    def draw_card(self):
        if not self.cards:
            raise ValueError("No cards left in the deck")
        return self.cards.pop()
    
    def draw_visual_stack(self, screen, card_back_image, x, y):
        # Draw the deck stack (back of cards)
        screen.blit(card_back_image, (x, y))

    