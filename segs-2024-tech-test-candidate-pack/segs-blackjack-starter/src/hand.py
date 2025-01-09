from .card import Card
import pygame

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)
    
    def draw_hand(self, screen, x, y):
        # Draw each card in the hand at a given position (x, y)
        for index, card in enumerate(self.cards):
            card_image = card.get_image()
            card_image = pygame.transform.scale(card_image, (175, 210))
            screen.blit(card_image, (x + index * 50, y))

    def calculate_value(self):
        value = 0
        aces = 0
        for card in self.cards:
            if card.rank in ['Jack', 'Queen', 'King']:
                value += 10
            elif card.rank == 'Ace':
                aces += 1
                value += 11  # Assume Ace is 11 initially
            else:
                value += int(card.rank)
        
        # Adjust for Aces if value > 21
        while value > 21 and aces:
            value -= 10
            aces -= 1
        
        return value

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)