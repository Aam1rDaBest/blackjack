from .card import Card
import pygame

class Hand:
    def __init__(self):
        """Initialise hand as array of card objects."""
        
        self.cards = []

    def add_card(self, card):
        """Add card to hand."""
        
        self.cards.append(card)
    
    def draw_hand(self, screen, x, y, orientation, facing='normal'):
        """Draw each card in the hand at a given position (x, y) with specified orientation."""
        
        for index, card in enumerate(self.cards):
            card_image = card.get_image()
            card_image = pygame.transform.scale(card_image, (175, 210))
            
            # Draw horizontally for the player (left to right)
            if orientation == 'horizontal':
                screen.blit(card_image, (x + index * 50, y))
            
            # Draw vertically for the opponents
            elif orientation == 'vertical':
                
                # Rotate the card 90 degrees clockwise to face the opponent
                if facing == 'left':
                    rotated_card = pygame.transform.rotate(card_image, 90)
                    rotated_card = pygame.transform.scale(rotated_card, (int(175 * 0.9), int(210 * 0.75)))
                    screen.blit(rotated_card, (x, y + index * 50))
                
                # Rotate the card 90 degrees clockwise to face the opponent
                elif facing == 'right':
                    rotated_card = pygame.transform.rotate(card_image, -90)
                    rotated_card = pygame.transform.scale(rotated_card, (int(175 * 0.9), int(210 * 0.75)))
                    screen.blit(rotated_card, (x, y - index * 50)) 

                # Default orientation (normal)
                else:
                    screen.blit(card_image, (x, y + index * 50))
                    
    def flip_last_card(self):
        """Flip card to reveal value in the hand."""
        
        if self.cards:
            self.cards[-1].flip()
        
    def calculate_value(self):
        """Calculates the values of the hands based on the cards."""
        
        # Initialise hand value and ace counter
        value = 0
        aces = 0
        
        # Loop through each card in the player's hand
        # Assign the value based on the card
        for card in self.cards:
            if card.rank in ['Jack', 'Queen', 'King']:
                value += 10
            elif card.rank == 'Ace':
                aces += 1
                value += 11 
                
                # Decrement ace 11 value to 1 when it causes a bust 
                while value > 21 and aces:
                    value -= 10
                    aces -= 1
            
            # Apply the value
            else:
                value += int(card.rank)
        
        return value

    def __str__(self):
        """String method for the hand"""
        
        return ', '.join(str(card) for card in self.cards)