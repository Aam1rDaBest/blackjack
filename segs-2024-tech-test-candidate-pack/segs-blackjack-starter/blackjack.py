import random
from src.deck import Deck
from src.hand import Hand
from src.card import Card
from src.player import Player

import pygame
import os
import time

class BlackjackGame:
    def __init__(self, num_players=1):
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
        
        if num_players != 1:
            self.num_players = num_players
            self.opponent_one = Player()
            self.opponent_two = Player()
            self.turn = 'player'  # Set initial turn to the player
            self.player_status = 'playing'
            self.opponent_one_status = 'playing'
            self.opponent_two_status = 'playing'
        else:
            self.num_players = 1
            self.player_status = 'playing'
            self.turn = 'player'
        self.turns_completed = 0

    def deal_initial_cards(self):
        """Deal 2 cards to each player (player and opponents)."""
        for _ in range(2):  # Deal 2 cards to each player initially
            self.animate_card_to_player(self.player)
            if self.num_players > 1:
                self.animate_card_to_player(self.opponent_one)
                self.animate_card_to_player(self.opponent_two)
        self.initial_cards_dealt = True

    def animate_card_to_player(self, player):
        """Animates a card moving from the deck to the player's hand."""
        # Determine starting and ending positions based on the player
        card_image = self.card_back_image
        if player == self.player:
            start_x, start_y = (self.screen.get_width() - 175) // 2, (self.screen.get_height() - 400) // 2
            end_x, end_y = (self.screen.get_width() - 350) // 2 + len(self.player.hand.cards) * 50, self.screen.get_height() - 250
        elif player == self.opponent_one:
            start_x, start_y = (self.screen.get_width() - 175) // 2, (self.screen.get_height() - 400) // 2
            end_x = (self.screen.get_width() // 4) - 87
            end_y = 200 + len(self.opponent_one.hand.cards) * 40
            card_image = pygame.transform.scale(card_image,  (int(175 * 0.9), int(210 * 0.75)))
            # Scale and rotate adjustments for opponent_one
            scaled_width = int(175 * 0.75)
            scaled_height = int(210 * 0.6)
        elif player == self.opponent_two:
            start_x, start_y = (self.screen.get_width() - 175) // 2, (self.screen.get_height() - 400) // 2
            end_x = (self.screen.get_width() * 3 // 4) - 47
            end_y = self.screen.get_height() - 400 - len(self.opponent_two.hand.cards) * 40
            card_image = pygame.transform.scale(card_image,  (int(175 * 0.9), int(210 * 0.75)))
            
            # Scale and rotate adjustments for opponent_two
            scaled_width = int(175 * 0.9)
            scaled_height = int(210 * 0.75)

        current_x, current_y = start_x, start_y
        step_x = (end_x - start_x) / 20
        step_y = (end_y - start_y) / 20

        # Static background rendering to avoid re-drawing static objects repeatedly
        background_surface = pygame.Surface(self.screen.get_size())
        background_surface.fill(self.green_color)
        self.deck.draw_visual_stack(background_surface, self.card_back_image, start_x, start_y)

        # Draw all hands for all players
        self.player.hand.draw_hand(background_surface, (self.screen.get_width() - 350) // 2, self.screen.get_height() - 250, 'horizontal')

        if self.num_players > 1:
            self.opponent_one.hand.draw_hand(background_surface, (self.screen.get_width() // 4) - 87, 200, 'vertical', facing='left')
        if self.num_players > 2:
            self.opponent_two.hand.draw_hand(background_surface, (self.screen.get_width() * 3 // 4) - 47, self.screen.get_height() - 400,'vertical', facing='right')

        # Animation for moving the card
        for _ in range(20):
            self.screen.blit(background_surface, (0, 0))  # Draw static background
            self.screen.blit(card_image, (current_x, current_y))  # Draw moving card

            # Apply rotation and scaling for opponent cards
            if player == self.opponent_one:
                rotated_card = pygame.transform.rotate(card_image, 90)
                rotated_card = pygame.transform.scale(rotated_card, (scaled_width, scaled_height))
            elif player == self.opponent_two:
                rotated_card = pygame.transform.rotate(card_image, -90)
                rotated_card = pygame.transform.scale(rotated_card, (scaled_width, scaled_height))
            else:
                rotated_card = card_image

            # Draw the rotated/scaled card on the background surface
            self.screen.blit(rotated_card, (current_x, current_y))
            pygame.display.flip()

            # Update card position
            current_x += step_x
            current_y += step_y
            self.clock.tick(60)

        # Add the card to the player's hand after the animation
        new_card = self.deck.draw_card()
        player.add_card_to_hand(new_card)

        # Now flip the card after it's added to the player's hand
        self.flip_card_animation(player)

    def flip_card_animation(self, player):
        """Animates the card flip after it's added to the player's hand."""
        # Flip the last card in the player's hand
        player.hand.flip_last_card()

        # Allow time for the flip animation to be visible
        for i in range(20):
            self.screen.fill(self.green_color)
            
            # Draw the deck stack and all players' hands
            self.deck.draw_visual_stack(self.screen, self.card_back_image, (self.screen.get_width() - 175) // 2, (self.screen.get_height() - 400) // 2)
            self.player.hand.draw_hand(self.screen, (self.screen.get_width() - 350) // 2, self.screen.get_height() - 250, 'horizontal')

            if self.num_players > 1:
                self.opponent_one.hand.draw_hand(self.screen, (self.screen.get_width() // 4) - 87, 200, 'vertical', facing='left')
            if self.num_players > 2:
                self.opponent_two.hand.draw_hand(self.screen, (self.screen.get_width() * 3 // 4) - 47, self.screen.get_height() - 400, 'vertical', facing='right')

            # Redraw the current hand value for the respective player
            font = pygame.font.Font(None, 36)
            text = font.render(f"Hand Value: {self.player.hand_value()}", True, (255, 255, 255))
            self.screen.blit(text, (50, 50))

            # Draw the quit button
            self.draw_quit_button()

            # Update the screen
            pygame.display.flip()

            # Pause for the flip animation to be visible
            self.clock.tick(60)

        # After the flip, check for game-ending conditions for the player
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

        # Draw the player hand (bottom of the screen, left to right)
        self.player.hand.draw_hand(self.screen, (self.screen.get_width() - 350) // 2, self.screen.get_height() - 250, 'horizontal')

        # Draw the opponent one hand (top of the screen, top to bottom)
        if self.num_players > 1:  # If there is more than one player
            self.opponent_one.hand.draw_hand(self.screen, (self.screen.get_width() // 4) - 87, 200, 'vertical', facing='left')

        # Draw the opponent two hand (bottom of the screen, bottom to top)
        if self.num_players > 2:  # If there is more than two players
            self.opponent_two.hand.draw_hand(self.screen, (self.screen.get_width() * 3 // 4) - 47, self.screen.get_height() - 400, 'vertical', facing='right')

        # Display game status (for the player)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Hand Value: {self.player.hand_value()}", True, (255, 255, 255))
        self.screen.blit(text, (50, 50))

        # Draw the deck stack
        self.deck.draw_visual_stack(self.screen, self.card_back_image, (self.screen.get_width() - 175) // 2, (self.screen.get_height() - 400) // 2)

        # Draw the quit button (red X)
        self.draw_quit_button()
        self.draw_buttons()

        # Update the display
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
        self.opponent_one = Player() 
        self.opponent_two = Player()  
        self.deck.shuffle()
        self.buttons_enabled = True
        self.initial_cards_dealt = False

        if self.num_players > 1:
            # Reset the hands for all players (including opponents)
            self.player.hand.cards = []  # Clear player's hand
            self.opponent_one.hand.cards = []  # Clear opponent one's hand
            self.opponent_two.hand.cards = []  # Clear opponent two's hand

            # Reset status of opponents (if needed)
            self.opponent_one.status = 'playing'
            self.opponent_two.status = 'playing'
        else:
            # For single player, reset just the player's hand
            self.player.hand.cards = []  # Clear player's hand

        self.deal_initial_cards()  # Deal the initial cards again
        self.running = True
    
    def end_game_screen(self, outcome):
        # Overlay surface for dimming the screen
        overlay_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay_surface.fill((0, 0, 0, 210))  # semi-transparent black
        self.screen.blit(overlay_surface, (0, 0))

        # Fonts for text rendering
        font_large = pygame.font.Font(None, 60)
        font_small = pygame.font.Font(None, 36)

        # Outcome text (e.g., "You win!" or "Game Over")
        outcome_text = font_large.render(outcome, True, (255, 255, 255))

        # Player's hand value and validity
        hand_value = self.player.hand_value()
        if hand_value > 21:
            validity_message = "Hand is Invalid"
        elif hand_value == 21:
            validity_message = "21 Score Achieved"
        else:
            validity_message = "Hand is Valid"

        validity_text = font_small.render(validity_message, True, (255, 255, 255))
        hand_value_text = font_small.render(f"Hand Value: {hand_value}", True, (255, 255, 255))

        # Buttons for "Play Again" and "Exit"
        play_again_button = pygame.Rect((self.screen.get_width() // 2 - 150, 350, 300, 80))
        exit_button = pygame.Rect((self.screen.get_width() // 2 - 150, 450, 300, 80))

        button_font = pygame.font.Font(None, 50)

        # Begin running the end screen
        running_end_screen = True
        while running_end_screen:
            self.screen.blit(hand_value_text, (50, 50))
            self.screen.blit(validity_text, ((self.screen.get_width() - validity_text.get_width()) // 2, 150))
            self.screen.blit(outcome_text, ((self.screen.get_width() - outcome_text.get_width()) // 2, 200))

            # Draw buttons
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
                        self.reset_game()  # Reset the game for a new round
                    elif exit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        exit()

            # Multi-Player Specific End Conditions
            if self.num_players > 1:
                # Evaluate the multi-player conditions (one player remaining or blackjack)
                remaining_players = [self.player] + [self.opponent_one, self.opponent_two]
                valid_players = [p for p in remaining_players if p.status != 'busted']
                
                if len(valid_players) == 1:  # Only one player left
                    winner = valid_players[0]
                    if winner == self.player:
                        outcome_text = font_large.render("You Win!", True, (0, 255, 0))
                    else:
                        outcome_text = font_large.render("Opponents Win!", True, (255, 0, 0))
                    self.buttons_enabled = True
                    running_end_screen = False
                    self.reset_game()
                    
                elif all(p.status != 'playing' for p in [self.player, self.opponent_one, self.opponent_two]):
                    # All players have finished playing, check for Blackjack or other conditions
                    if self.player.hand_value() == 21:
                        outcome_text = font_large.render("Blackjack! You Win!", True, (0, 255, 0))
                    elif self.opponent_one.hand_value() == 21:
                        outcome_text = font_large.render("Opponent 1 Has Blackjack! They Win!", True, (255, 0, 0))
                    elif self.opponent_two.hand_value() == 21:
                        outcome_text = font_large.render("Opponent 2 Has Blackjack! They Win!", True, (255, 0, 0))
                    else:
                        # Compare hand values if no one has Blackjack
                        player_score = self.player.hand_value()
                        opponent_1_score = self.opponent_one.hand_value()
                        opponent_2_score = self.opponent_two.hand_value()

                        if player_score > opponent_1_score and player_score > opponent_2_score:
                            outcome_text = font_large.render("You Win!", True, (0, 255, 0))
                        elif opponent_1_score > player_score and opponent_1_score > opponent_2_score:
                            outcome_text = font_large.render("Opponent 1 Wins!", True, (255, 0, 0))
                        elif opponent_2_score > player_score and opponent_2_score > opponent_1_score:
                            outcome_text = font_large.render("Opponent 2 Wins!", True, (255, 0, 0))
                        else:
                            outcome_text = font_large.render("It's a Tie!", True, (255, 255, 0))
                    
                    self.buttons_enabled = True
                    running_end_screen = False
                    self.reset_game()
    

    def handle_input(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if self.buttons_enabled:
                    if self.hit_button_rect.collidepoint(mouse_pos) and self.turn == 'player' and self.player_status == 'playing':
                        self.buttons_enabled = False
                        self.animate_card_to_player(self.player)
                        self.check_turn_end(self.player)
                        self.buttons_enabled = True

                    elif self.stand_button_rect.collidepoint(mouse_pos) and self.turn == 'player' and self.player_status == 'playing':
                        self.buttons_enabled = False
                        self.end_game_screen("You Chose to Stand.")
                        self.check_turn_end(self.player)
                        self.buttons_enabled = True

            # Quit button
            if self.quit_button_rect.collidepoint(mouse_pos) and event.type == pygame.MOUSEBUTTONDOWN:
                self.running = False

        # If in multi-play mode, handle opponents' turns after player action
        if self.num_players > 1:
            if self.turn == 'opponent_one' and self.opponent_one_status == 'playing':
                self.opponent_turn(self.opponent_one)
            elif self.turn == 'opponent_two' and self.opponent_two_status == 'playing':
                self.opponent_turn(self.opponent_two)
    
    def opponent_turn(self, opponent):
        """Simulate the opponent's turn (hit or stand)."""
        if opponent.status == 'playing':
            action = random.choice(['hit', 'stand'])  # Random choice for now (50% chance)
            
            if action == 'hit':
                self.animate_card_to_player(opponent)
                if opponent.hand_value() > 21:  # Check if opponent busts
                    opponent.status = 'busted'
                self.check_turn_end(opponent)  # End turn after hit
            elif action == 'stand':
                opponent.status = 'stood'
                self.check_turn_end(opponent)

    def check_turn_end(self, player):
        """Check if the current player's turn is over and switch to the next player."""
        if player.status == 'stood' or player.hand_value() > 21:
            # Increment the turns_completed counter
            self.turns_completed += 1
            
            # Switch turn to the next player
            if self.turn == 'player':
                self.turn = 'opponent_one'
            elif self.turn == 'opponent_one':
                self.turn = 'opponent_two'
            elif self.turn == 'opponent_two':
                self.turn = 'player'
            
            # Check if all turns are complete (if there are 3 players including the player)
            if self.num_players > 1 and self.turns_completed == 3:
                   self.end_game_screen("All players have completed their turn.")
                    
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
    initial = BlackjackGame(3)
    initial.play()
