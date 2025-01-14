from .card import Card
import pygame

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)
    
    def draw_hand(self, screen, x, y, orientation, facing='normal'):
        """Draw each card in the hand at a given position (x, y) with specified orientation."""
        for index, card in enumerate(self.cards):
            card_image = card.get_image()
            card_image = pygame.transform.scale(card_image, (175, 210))
            
            if orientation == 'horizontal':
                # Draw horizontally for the player (left to right)
                screen.blit(card_image, (x + index * 50, y))
            
            elif orientation == 'vertical':
                # Draw vertically for the opponents
                if facing == 'left':
                    # Draw top to bottom for opponent one (top left of the screen)
                    # Rotate the card 90 degrees clockwise to face the opponent
                    rotated_card = pygame.transform.rotate(card_image, 90)
                    rotated_card = pygame.transform.scale(rotated_card, (int(175 * 0.9), int(210 * 0.75)))
                    screen.blit(rotated_card, (x, y + index * 50))  # Adjust vertical positioning
                elif facing == 'right':
                    # Draw bottom to top for opponent two (bottom right of the screen)
                    # Rotate the card 90 degrees counter-clockwise to face the opponent
                    rotated_card = pygame.transform.rotate(card_image, -90)
                    rotated_card = pygame.transform.scale(rotated_card, (int(175 * 0.9), int(210 * 0.75)))
                    screen.blit(rotated_card, (x, y - index * 50))  # Adjust vertical positioning
                else:
                    # Default orientation (normal)
                    screen.blit(card_image, (x, y + index * 50))
                    
    def flip_last_card(self):
        if self.cards:
            self.cards[-1].flip()
        
    def calculate_value(self):
        value = 0
        aces = 0
        
        for card in self.cards:
            if card.rank in ['Jack', 'Queen', 'King']:
                value += 10
            elif card.rank == 'Ace':
                aces += 1
                value += 11  # Assume Ace is 11 initially
                while value > 21 and aces:
                    value -= 10
                    aces -= 1
            else:
                value += int(card.rank)
        
        return value

    def __str__(self):
        return ', '.join(str(card) for card in self.cards)