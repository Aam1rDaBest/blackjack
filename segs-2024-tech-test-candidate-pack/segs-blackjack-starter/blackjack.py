from src.deck import Deck
from src.hand import Hand
from src.card import Card
from src.player import Player

import pygame
import os

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
        
        # Game objects
        self.deck = Deck()
        self.player = Player()
        self.deck.shuffle()

    def deal_initial_cards(self):
        for _ in range(2):  # Player gets 2 cards initially
            self.player.add_card_to_hand(self.deck.draw_card())

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
        

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:  # Hit
                    self.player.add_card_to_hand(self.deck.draw_card())
                elif event.key == pygame.K_s:  # Stand
                    print("Player chose to stand.")
                    self.running = False
            
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
        while self.running:
            self.handle_input()

            # Game logic based on player action
            if self.action == 'h':
                try:
                    self.player.add_card_to_hand(self.deck.draw_card())
                    self.action = None
                except ValueError:
                    print("Deck is empty!")
                    self.running = False

            elif self.action == 's':
                print("Player chose to stand.")
                self.running = False

            # Check hand value
            if self.player.hand_value() > 21:
                print("Bust! Player loses.")
                self.running = False
            elif self.player.hand_value() == 21:
                print("Blackjack! Player wins.")
                self.running = False

            # Render the screen
            self.draw_screen()
            self.clock.tick(30)  # 30 FPS
        
        self.determine_winner()
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
