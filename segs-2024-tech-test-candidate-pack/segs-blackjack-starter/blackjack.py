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
        self.animating = False

        # Game assets
        self.card_back_image = pygame.image.load(os.path.join("assets", "card_back_red.png"))
        self.card_back_image = pygame.transform.scale(self.card_back_image, (175, 210))
        
        self.green_color = (34, 139, 34)
        self.action = None
        
        # Quit button dimensions and position
        self.quit_button_color = (255,0,0)  # Red color for 'X'
        self.quit_button_rect = pygame.Rect(self.screen.get_width() - 60, 20, 60, 40)
        
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

        # Animation for moving the card
        for _ in range(20):
            # Clear the screen
            self.screen.fill(self.green_color)

            # Draw the deck stack
            self.deck.draw_visual_stack(self.screen, self.card_back_image, start_x, start_y)

            # Draw the player's hand
            self.player.hand.draw_hand(self.screen, (self.screen.get_width() - 350) // 2, self.screen.get_height() - 250)

            # Draw the moving card
            self.screen.blit(card_image, (current_x, current_y))

            # Draw the current hand value
            font = pygame.font.Font(None, 36)
            text = font.render(f"Hand Value: {self.player.hand_value()}", True, (255, 255, 255))
            self.screen.blit(text, (50, 50))

            # Draw the quit button
            self.draw_quit_button()

            # Update the screen
            pygame.display.flip()

            # Update card position
            current_x += step_x
            current_y += step_y

            # Cap the frame rate
            self.clock.tick(60)

        # Add the card to the player's hand
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
        
        pygame.display.flip()
        
    def draw_quit_button(self):
        # Draw the red 'X' button at the top-right corner
        font = pygame.font.SysFont(None, 60)
        quit_text = font.render('X', True, (255, 0, 0))
        self.screen.blit(quit_text, (self.quit_button_rect.x + 2, self.quit_button_rect.y - 2))  # Offset for centering
    
    def reset_game(self):
        """Resets the game state for a new round."""
        self.deck = Deck()
        self.player = Player()
        self.deck.shuffle()
        self.deal_initial_cards()
        self.running = True
    
    def end_game_screen(self, outcome):
        """Displays the end game screen with the outcome, hand value, and options to play again or exit."""
        
        # Create an overlay surface with transparency support
        overlay_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        
        # Fill the surface with semi-transparent black color (RGBA: Red, Green, Blue, Alpha)
        overlay_surface.fill((0, 0, 0, 210))  # RGBA: (0, 0, 0) for black, 120 for semi-transparency

        # Draw the overlay ONCE onto the screen
        self.screen.blit(overlay_surface, (0, 0))  # Draw the overlay on top of the screen

        # Fonts for text
        font_large = pygame.font.Font(None, 60)
        font_small = pygame.font.Font(None, 36)

        # Outcome text
        outcome_text = font_large.render(outcome, True, (255, 255, 255))

        # Hand validity message
        hand_value = self.player.hand_value()
        print(self.player)
        if hand_value > 21:
            validity_message = "Hand is Invalid"
        elif hand_value == 21:
            validity_message = "21 Score Achieved"
        else:
            validity_message = "Hand is Valid"

        validity_text = font_small.render(validity_message, True, (255, 255, 255))

        # Hand value text (to re-draw it in the top-left corner like during gameplay)
        hand_value_text = font_small.render(f"Hand Value: {hand_value}", True, (255, 255, 255))

        # Buttons for Play Again and Exit
        play_again_button = pygame.Rect((self.screen.get_width() // 2 - 150, 350, 300, 80))
        exit_button = pygame.Rect((self.screen.get_width() // 2 - 150, 450, 300, 80))

        button_font = pygame.font.Font(None, 50)

        running_end_screen = True
        while running_end_screen:
            # Draw the hand value in the top-left corner (same as during gameplay)
            self.screen.blit(hand_value_text, (50, 50))

            # Draw the hand validity message above the outcome text
            self.screen.blit(validity_text, ((self.screen.get_width() - validity_text.get_width()) // 2, 150))

            # Draw the outcome message
            self.screen.blit(outcome_text, ((self.screen.get_width() - outcome_text.get_width()) // 2, 200))

            # Draw buttons
            pygame.draw.rect(self.screen, (0, 255, 0), play_again_button)  # Green button
            pygame.draw.rect(self.screen, (255, 0, 0), exit_button)        # Red button
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
                        running_end_screen = False
                        self.reset_game()
                    elif exit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        exit()
    
    

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.initial_cards_dealt:  # Input only enabled after initial cards are dealt
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:  # Hit
                        self.animate_card_to_player()
                        if self.player.hand_value() > 21:
                            self.end_game_screen("Bust! You Lose.")
                        elif self.player.hand_value() == 21:
                            self.end_game_screen("Blackjack! You Win!")
                    elif event.key == pygame.K_s:  # Stand
                        self.end_game_screen("You Chose to Stand.")

            # Detect mouse clicks for the quit button
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
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
