from src.deck import Deck
from src.hand import Hand
from src.card import Card
from src.player import Player

import pygame
import os
import time

class BlackjackGame:
    def __init__(self, num_players):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 700), pygame.NOFRAME)  # Screen dimensions
        pygame.display.set_caption("Blackjack Game")
        self.clock = pygame.time.Clock()
        self.running = True

        # Game assets
        self.card_back_image = pygame.image.load(os.path.join("assets", "card_back_red.png"))
        self.card_back_image = pygame.transform.scale(self.card_back_image, (175, 210))
        
        self.green_color = (34, 139, 34)
        self.action = None
        
        # Quit button dimensions and position
        self.quit_button_color = (255,0,0)  # Red color for 'X'
        self.quit_button_rect = pygame.Rect(self.screen.get_width() - 60, 20, 60, 40)
        
        # Hit and stand buttons
        self.hit_button_rect = pygame.Rect(self.screen.get_width() - 250, self.screen.get_height() - 190, 150, 50)
        self.stand_button_rect = pygame.Rect(self.screen.get_width() - 250, self.screen.get_height() - 110, 150, 50)
        self.buttons_enabled = True
        
        # Game objects
        self.deck = Deck()
        self.player = Player()
        self.deck.shuffle()
        
        self.initial_cards_dealt = False

    def deal_initial_cards(self):
        for _ in range(2):  # Player gets 2 cards initially
            self.animate_card_to_player()
            pygame.time.wait(500)
        self.initial_cards_dealt = True
        
        #self.player.add_card_to_hand(self.deck.draw_card())

    def animate_card_to_player(self):
        """Animates a card moving from the deck to the player's hand."""
        start_x, start_y = (self.screen.get_width() - 175) // 2, (self.screen.get_height() - 400) // 2
        end_x, end_y = (self.screen.get_width() - 350) // 2 + len(self.player.hand.cards) * 50, self.screen.get_height() - 250

        card_image = self.card_back_image
        current_x, current_y = start_x, start_y
        step_x = (end_x - start_x) / 20
        step_y = (end_y - start_y) / 20

        # Static background rendering to avoid re-drawing static objects repeatedly
        background_surface = pygame.Surface(self.screen.get_size())
        background_surface.fill(self.green_color)
        self.deck.draw_visual_stack(background_surface, self.card_back_image, start_x, start_y)
        self.player.hand.draw_hand(background_surface, (self.screen.get_width() - 350) // 2, self.screen.get_height() - 250)

        # Animation for moving the card
        for _ in range(20):
            self.screen.blit(background_surface, (0, 0))  # Draw static background
            self.screen.blit(card_image, (current_x, current_y))  # Draw moving card
            pygame.display.flip()

            # Update card position
            current_x += step_x
            current_y += step_y
            self.clock.tick(60)

        # Add the card to the player's hand after the animation
        new_card = self.deck.draw_card()
        self.player.add_card_to_hand(new_card)

        # Now flip the card after it's added to the player's hand
        self.flip_card_animation()

    def flip_card_animation(self):
        """Animates the card flip after it's added to the player's hand."""
        # Flip the last card in the player's hand
        self.player.hand.flip_last_card()

        # Allow time for the flip animation to be visible (this is critical)
        for i in range(20):
            self.screen.fill(self.green_color)
            
            # Draw the deck stack and the player's hand
            self.deck.draw_visual_stack(self.screen, self.card_back_image, (self.screen.get_width() - 175) // 2, (self.screen.get_height() - 400) // 2)
            self.player.hand.draw_hand(self.screen, (self.screen.get_width() - 350) // 2, self.screen.get_height() - 250)

            # Draw the flipped card (or back image if not flipped)
            self.player.hand.draw_hand(self.screen, (self.screen.get_width() - 350) // 2, self.screen.get_height() - 250)
            
            # Redraw the current hand value
            font = pygame.font.Font(None, 36)
            text = font.render(f"Hand Value: {self.player.hand_value()}", True, (255, 255, 255))
            self.screen.blit(text, (50, 50))

            # Draw the quit button
            self.draw_quit_button()

            # Update the screen
            pygame.display.flip()
            
            # Pause for the flip animation to be visible
            self.clock.tick(60)

        # After the flip, check for game-ending conditions
        self.check_game_end_conditions()

    def check_game_end_conditions(self):
        """Check if the game should end based on the player's hand value."""
        hand_value = self.player.hand_value()

        if hand_value > 21:
            self.end_game_screen("Bust! You Lose.")
        elif hand_value == 21:
            self.end_game_screen("Blackjack! You Win!")
        
    def draw_screen(self):
        # Draw the table background
        self.screen.fill(self.green_color)

        self.player.hand.draw_hand(self.screen, (self.screen.get_width() - 350) // 2, self.screen.get_height() - 250)

        # Display game status
        font = pygame.font.Font(None, 36)
        text = font.render(f"Hand Value: {self.player.hand_value()}", True, (255, 255, 255))
        self.screen.blit(text, (50, 50))
        
        # Draw the deck stack
        self.deck.draw_visual_stack(self.screen, self.card_back_image, (self.screen.get_width() - 175) // 2, (self.screen.get_height() - 400) // 2)

        # Draw the quit button (red X)
        self.draw_quit_button()
        self.draw_buttons()
        pygame.display.flip()
        
    def draw_quit_button(self):
        # Draw the red 'X' button at the top-right corner
        font = pygame.font.SysFont(None, 60)
        quit_text = font.render('X', True, (255, 0, 0))
        self.screen.blit(quit_text, (self.quit_button_rect.x + 2, self.quit_button_rect.y - 2)) 
    
    def draw_buttons(self):
        """Draws the Hit and Stand buttons."""
        if self.buttons_enabled:
            hit_color = (0, 123, 255)
            stand_color = (255, 0, 0)
        else:
            hit_color = stand_color = (150, 150, 150)

        pygame.draw.rect(self.screen, hit_color, self.hit_button_rect)
        pygame.draw.rect(self.screen, stand_color, self.stand_button_rect)

        font = pygame.font.Font(None, 36)
        hit_text = font.render("Hit", True, (255, 255, 255))
        stand_text = font.render("Stand", True, (255, 255, 255))
        self.screen.blit(hit_text, (self.hit_button_rect.x + 50, self.hit_button_rect.y + 10))
        self.screen.blit(stand_text, (self.stand_button_rect.x + 35, self.stand_button_rect.y + 10))
        
    def reset_game(self):
        """Resets the game state for a new round."""
        self.deck = Deck()
        self.player = Player()
        self.deck.shuffle()
        self.buttons_enabled = True
        self.initial_cards_dealt = False
        self.deal_initial_cards()
        self.running = True
    
    def end_game_screen(self, outcome):

        overlay_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay_surface.fill((0, 0, 0, 210))
        self.screen.blit(overlay_surface, (0, 0))

        font_large = pygame.font.Font(None, 60)
        font_small = pygame.font.Font(None, 36)

        outcome_text = font_large.render(outcome, True, (255, 255, 255))
        hand_value = self.player.hand_value()
        print(self.player)

        if hand_value > 21:
            validity_message = "Hand is Invalid"
        elif hand_value == 21:
            validity_message = "21 Score Achieved"
        else:
            validity_message = "Hand is Valid"

        validity_text = font_small.render(validity_message, True, (255, 255, 255))
        hand_value_text = font_small.render(f"Hand Value: {hand_value}", True, (255, 255, 255))

        play_again_button = pygame.Rect((self.screen.get_width() // 2 - 150, 350, 300, 80))
        exit_button = pygame.Rect((self.screen.get_width() // 2 - 150, 450, 300, 80))

        button_font = pygame.font.Font(None, 50)

        running_end_screen = True
        while running_end_screen:
            self.screen.blit(hand_value_text, (50, 50))
            self.screen.blit(validity_text, ((self.screen.get_width() - validity_text.get_width()) // 2, 150))
            self.screen.blit(outcome_text, ((self.screen.get_width() - outcome_text.get_width()) // 2, 200))

            pygame.draw.rect(self.screen, (0, 255, 0), play_again_button)
            pygame.draw.rect(self.screen, (255, 0, 0), exit_button)
            play_again_text = button_font.render("Play Again", True, (0, 0, 0))
            exit_text = button_font.render("Exit", True, (0, 0, 0))
            self.screen.blit(play_again_text,
                            (play_again_button.x + (play_again_button.width - play_again_text.get_width()) // 2,
                            play_again_button.y + (play_again_button.height - play_again_text.get_height()) // 2))
            self.screen.blit(exit_text,
                            (exit_button.x + (exit_button.width - exit_text.get_width()) // 2,
                            exit_button.y + (exit_button.height - exit_text.get_height()) // 2))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if play_again_button.collidepoint(mouse_pos):
                        self.buttons_enabled = True
                        running_end_screen = False
                        self.reset_game()
                    elif exit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        exit()
    
    

    def handle_input(self):
        mouse_pos = None  # Ensure mouse_pos is defined before use
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if self.buttons_enabled:
                    if self.hit_button_rect.collidepoint(mouse_pos):
                        self.buttons_enabled = False
                        self.animate_card_to_player()
                        self.buttons_enabled = True

                    elif self.stand_button_rect.collidepoint(mouse_pos):
                        self.buttons_enabled = False
                        self.end_game_screen("You Chose to Stand.")

                if self.quit_button_rect.collidepoint(mouse_pos):  # Check if click is inside 'X'
                    self.running = False

                    
    def play(self):
        """self.deal_initial_cards()
        print(self.player)
        while self.player.hand_value() < 21:
            action = input(f"Do you want to hit (h) or stand (s)? ")
            if action.lower() == 'h':
                self.player.add_card_to_hand(self.deck.draw_card())
                print(self.player)
            elif action.lower() == 's':
                print("Final",self.player)
                print("Game Over")
                break
            else:
                print("Invalid Response")
                print("Game Over")
                break

        self.determine_winner()"""
        self.deal_initial_cards()
        while self.running:
            self.handle_input()

            """# Game logic based on player action
            if self.action == 'h':
                try:
                    self.player.add_card_to_hand(self.deck.draw_card())
                    self.action = None
                except ValueError:
                    print("Deck is empty!")
                    self.running = False
            """
            # Render the screen
            self.draw_screen()
            self.clock.tick(30)  # 30 FPS
        
        #self.determine_winner()
        pygame.quit()

    def determine_winner(self):
        player_value = self.player.hand_value()
        if player_value > 21:
            print(f"Bust!")
        elif player_value == 21:
            print(f"Winner!")


if __name__ == '__main__':
    initial = BlackjackGame(1)
    initial.play()
