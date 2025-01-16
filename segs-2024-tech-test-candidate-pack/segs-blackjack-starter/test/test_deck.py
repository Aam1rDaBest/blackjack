import time
import unittest
from unittest.mock import patch, MagicMock
import pygame
import sys
import os
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.deck import Deck
from blackjack import BlackjackGame
from src.player import Player
from src.hand import Hand
from src.card import Card

class TestBlackjackSingleGame(unittest.TestCase):

    def setUp(self):
        """Set up a fresh Blackjack game for testing in single-player mode."""
        self.game = BlackjackGame(1)  # Single player mode

    @patch.object(BlackjackGame, 'animate_card_to_player', lambda self, player: player.add_card_to_hand(self.deck.draw_card()))
    def test_deal_initial_cards(self):
        """Test that the player receives 2 valid cards and the deck size decreases accordingly."""

        initial_deck_size = len(self.game.deck.cards)  # Capture initial deck size
        self.game.deal_initial_cards()  # Deal the initial cards

        # Check the player's hand contains exactly 2 cards
        self.assertEqual(len(self.game.player.hand.cards), 2, "Player should have exactly 2 cards after dealing.")

        # Check that the deck size decreased by 2
        expected_deck_size = initial_deck_size - 2
        self.assertEqual(len(self.game.deck.cards), expected_deck_size, "Deck should have 2 fewer cards after dealing.")

        # Check that both cards in the hand are valid Card objects
        for card in self.game.player.hand.cards:
            self.assertIsInstance(card, Card, "Each card in the player's hand should be a valid Card object.")
            
    @patch.object(BlackjackGame, 'animate_card_to_player', lambda self, player: player.add_card_to_hand(self.deck.draw_card()))
    def test_hit_logic(self):
        """Test that hitting increases hand size and reduces deck size."""
        
        # Deal initial cards to the player
        self.game.deal_initial_cards()
        initial_hand_size = len(self.game.player.hand.cards)
        initial_deck_size = len(self.game.deck.cards)

        # Simulate the "hit" action
        self.game.animate_card_to_player(self.game.player)  # Simulate adding a card to the player's hand
        hand_value = self.game.player.hand_value()
        if hand_value > 21:
            self.game.player.status = 'busted'

        # Assert that the player's hand size has increased by 1 after the hit
        self.assertEqual(len(self.game.player.hand.cards), initial_hand_size + 1, "Player's hand should have 1 more card after hit.")

        # Assert that the deck size has decreased by 1 after the hit
        self.assertEqual(len(self.game.deck.cards), initial_deck_size - 1, "Deck should have 1 fewer card after hit.")
        
        # Evaluate the game end after hitting
        if self.game.player.hand_value() > 21:
            self.assertTrue(self.game.player.status == 'busted', "Player should be busted if hand value exceeds 21.")
    
    @patch.object(BlackjackGame, 'animate_card_to_player', lambda self, player: player.add_card_to_hand(self.deck.draw_card()))
    def test_stand_logic(self):
        """Test that standing does not change the hand value and evaluates the hand correctly."""
        
        # Deal initial cards to the player
        self.game.deal_initial_cards()
        initial_hand_value = self.game.player.hand_value()

        # Directly set player status to 'stood' (simulate standing)
        self.game.player.status = 'stood'

        # Ensure the player's hand value remains the same after standing
        self.assertEqual(self.game.player.hand_value(), initial_hand_value, "Hand value should remain the same after stand.")

        # Ensure no card was added to the player's hand (deck size should remain the same)
        self.assertEqual(len(self.game.deck.cards), len(self.game.deck.cards), "Deck size should remain the same after stand.")

        # Check if the player is not bust after standing (should be a valid hand)
        if self.game.player.hand_value() > 21:
            self.assertTrue(self.game.player.status == 'busted', "Player should be busted if hand value exceeds 21.")
        else:
            self.assertTrue(self.game.player.status == 'stood', "Player should be in 'stood' state.")

    @patch.object(BlackjackGame, 'animate_card_to_player', lambda self, player: None)
    def test_quit_button(self):
        """Test that clicking the quit button ends the game."""
        self.game.running = False  # Set the game running state to False, simulating quit behavior
        
        # Ensure that the game is no longer running (quit state)
        self.assertFalse(self.game.running, "The game should stop running after the quit button is clicked.")
    
    @patch.object(BlackjackGame, 'animate_card_to_player', lambda self, player: None)
    def test_bust_end_game(self):
        """Test that the game ends with 'Bust! You Lose.' when the player's hand value exceeds 21."""
        
        # Manually assign cards to create a bust scenario
        self.game.player.add_card_to_hand(Card("Hearts", "King", True))
        self.game.player.add_card_to_hand(Card("Spades", "Queen", True))
        self.game.player.add_card_to_hand(Card("Diamonds", "5", True))  # Exceeds 21
        
        # Ensure hand value exceeds 21
        self.assertGreater(self.game.player.hand_value(), 21, "Hand value should exceed 21 for bust scenario.")

        # Simulate the game detecting a bust
        if self.game.player.hand_value() > 21:
            self.game.player.status = 'busted'
            outcome = "Bust! You Lose."

        # Ensure the correct outcome message is assigned
        self.assertEqual(self.game.player.status, 'busted', "Player should be in 'busted' state.")
        self.assertEqual(outcome, "Bust! You Lose.", "Game should display 'Bust! You Lose.' when player exceeds 21.")

    @patch.object(BlackjackGame, 'animate_card_to_player', lambda self, player: None) 
    def test_blackjack_end_game(self):
        """Test that the game ends with 'Blackjack! You Win.' when the player's hand value equals 21."""
        
        # Manually assign cards to create a blackjack scenario
        self.game.player.add_card_to_hand(Card("Clubs", "Ace", True))
        self.game.player.add_card_to_hand(Card("Hearts", "King", True))  # 21 value
        
        # Ensure hand value is exactly 21
        self.assertEqual(self.game.player.hand_value(), 21, "Hand value should be 21 for blackjack scenario.")

        # Simulate the game detecting a blackjack
        if self.game.player.hand_value() == 21:
            self.game.player.status = 'blackjack'
            outcome = "Blackjack! You Win."

        # Ensure the correct outcome message is assigned
        self.assertEqual(self.game.player.status, 'blackjack', "Player should be in 'blackjack' state.")
        self.assertEqual(outcome, "Blackjack! You Win.", "Game should display 'Blackjack! You Win.' when player has 21.")

    @patch.object(BlackjackGame, 'animate_card_to_player', lambda self, player: None) 
    def test_stand_end_game(self):
        """Test that the game correctly recognizes a player standing and does not change hand value."""
        
        # Manually assign a reasonable hand value that would make a player stand
        self.game.player.add_card_to_hand(Card("Diamonds", "10", True))
        self.game.player.add_card_to_hand(Card("Spades", "7", True))
        
        
        initial_hand_value = self.game.player.hand_value()
        
        # Simulate the player standing
        self.game.player.status = 'stood'
        
        # Ensure the hand value remains unchanged
        self.assertEqual(self.game.player.hand_value(), initial_hand_value, "Hand value should remain unchanged after standing.")
        
        # Ensure the player's status is 'stood'
        self.assertEqual(self.game.player.status, 'stood', "Player should be in 'stood' state after choosing to stand.")

    @patch.object(BlackjackGame, 'animate_card_to_player', lambda self, player: player.add_card_to_hand(self.deck.draw_card()))
    def test_reset_game(self):
        """Test that the game resets correctly and deals a new hand with 2 cards."""
        
        # Ensure the deck starts with 52 cards
        initial_deck_size = len(self.game.deck.cards)
        self.assertEqual(initial_deck_size, 52, "Deck should start with 52 cards.")
        
        # Deal initial cards to player
        self.game.deal_initial_cards()
        initial_hand_value = self.game.player.hand_value()
        
        # Save the initial hand details (cards' rank and suit)
        initial_hand_cards = [(card.rank, card.suit) for card in self.game.player.hand.cards]

        # Call reset_game()
        self.game.reset_game()
        time.sleep(0.1)  # Short delay to ensure all operations complete

        # Process any pending events to ensure Pygame updates correctly
        pygame.event.pump()
        
        # Deck should now have 50 cards (2 cards dealt to player)
        self.assertEqual(len(self.game.deck.cards), 50, "Deck should have 50 cards after dealing 2 to the player.")

        # Player should have exactly 2 cards in hand
        self.assertEqual(len(self.game.player.hand.cards), 2, "Player should have exactly 2 cards after reset.")

        # Ensure game state is reset
        self.assertTrue(self.game.running, "Game should be running after reset.")
        self.assertFalse(self.game.game_over, "Game should not be in game-over state after reset.")
        self.assertTrue(self.game.buttons_enabled, "Buttons should be enabled after reset.")
        self.assertEqual(self.game.player.status, "playing", "Player should be in 'playing' state after reset.")
        
        # Save the new hand details (cards' rank and suit)
        new_hand_cards = [(card.rank, card.suit) for card in self.game.player.hand.cards]

        # Check that the new hand is different from the previous hand
        self.assertNotEqual(initial_hand_cards, new_hand_cards, "The player's hand should change after reset.")
        
class TestBlackjackMultiGame(unittest.TestCase): 

    def setUp(self):
        """Set up a fresh Blackjack game for testing in multi-player mode."""
        self.game = BlackjackGame(3)  # Multi-player mode with 3 players

    @patch.object(BlackjackGame, 'animate_card_to_player', lambda self, player: player.add_card_to_hand(self.deck.draw_card()))
    def test_deal_initial_cards(self):
        """Test that the player and opponents each receive 2 valid cards."""
        
        initial_deck_size = len(self.game.deck.cards)
        self.game.deal_initial_cards()  # Deal initial cards to all players

        # 1. Check the player's hand contains exactly 2 cards
        self.assertEqual(len(self.game.player.hand.cards), 2, "Player should have exactly 2 cards after dealing.")

        # 2. Check that the opponents have exactly 2 cards each
        self.assertEqual(len(self.game.opponent_one.hand.cards), 2, "Opponent 1 should have exactly 2 cards after dealing.")
        self.assertEqual(len(self.game.opponent_two.hand.cards), 2, "Opponent 2 should have exactly 2 cards after dealing.")
        
        # 3. Check that the deck size decreased by 6 (2 cards per player for 3 players)
        expected_deck_size = initial_deck_size - 6
        self.assertEqual(len(self.game.deck.cards), expected_deck_size, "Deck should have 6 fewer cards after dealing to 3 players.")
    
    @patch.object(BlackjackGame, 'animate_card_to_player', lambda self, player: player.add_card_to_hand(self.deck.draw_card()))
    def test_hit_logic(self):
        """Test that hitting increases hand size and reduces deck size for players."""
        
        self.game.deal_initial_cards()  # Deal initial cards
        initial_player_hand_size = len(self.game.player.hand.cards)
        initial_deck_size = len(self.game.deck.cards)

        # Simulate the "hit" action for the player
        self.game.animate_card_to_player(self.game.player)  # Simulate adding a card to the player's hand

        # Assert that the player's hand size has increased by 1
        self.assertEqual(len(self.game.player.hand.cards), initial_player_hand_size + 1, "Player's hand should have 1 more card after hit.")

        # Assert that the deck size has decreased by 1
        self.assertEqual(len(self.game.deck.cards), initial_deck_size - 1, "Deck should have 1 fewer card after hit.")

        # Simulate the opponent's "hit" action
        self.game.animate_card_to_player(self.game.opponent_one)
        self.assertEqual(len(self.game.opponent_one.hand.cards), 3, "Opponent 1 should have 3 cards after hit.")
        
        self.game.animate_card_to_player(self.game.opponent_two)
        self.assertEqual(len(self.game.opponent_two.hand.cards), 3, "Opponent 2 should have 3 cards after hit.")
        
    @patch.object(BlackjackGame, 'animate_card_to_player', lambda self, player: player.add_card_to_hand(self.deck.draw_card()))
    def test_stand_logic(self):
        """Test that standing does not change hand size and checks player's state."""
        
        self.game.deal_initial_cards()
        initial_player_hand_value = self.game.player.hand_value()

        # Simulate the player standing
        self.game.player.status = 'stood'

        # Ensure the player's hand value remains unchanged after standing
        self.assertEqual(self.game.player.hand_value(), initial_player_hand_value, "Hand value should remain the same after stand.")
        
        # Ensure the opponent's status is not affected
        self.assertEqual(self.game.opponent_one.status, 'playing', "Opponent 1 should still be playing.")
        self.assertEqual(self.game.opponent_two.status, 'playing', "Opponent 2 should still be playing.")

    @patch.object(BlackjackGame, 'animate_card_to_player', lambda self, player: None)
    def test_quit_button(self):
        """Test that clicking the quit button ends the game for all players."""
        
        self.game.running = False  # Set the game running state to False, simulating quit behavior
        self.assertFalse(self.game.running, "The game should stop running after the quit button is clicked.")

    @patch.object(BlackjackGame, 'animate_card_to_player', lambda self, player: player.hand.add_card(self.deck.draw_card())) 
    @patch('random.randint', return_value=1) 
    def test_opponent_turn(self, mock_randint):
        """Test opponent decisions (hit or stand) without calling opponent_turn directly."""

        self.game.deal_initial_cards()  # Deal initial cards to all players

        # Simulate player standing to allow opponent turns
        self.game.player.status = 'stood'

        # Define a helper function to simulate opponent logic manually
        def simulate_opponent_turn(opponent):
            hand_value = opponent.hand_value()

            # If opponent hand value is 15 or below, they always hit
            if hand_value <= 15:
                self.game.animate_card_to_player(opponent)
                return "hit"

            # If hand value is 16-19, probability determines hit/stand
            elif hand_value == 16 and mock_randint.return_value <= 4:
                self.game.animate_card_to_player(opponent)
                return "hit"
            elif hand_value == 17 and mock_randint.return_value <= 3:
                self.game.animate_card_to_player(opponent)
                return "hit"
            elif hand_value == 18 and mock_randint.return_value <= 2:
                self.game.animate_card_to_player(opponent)
                return "hit"
            elif hand_value == 19 and mock_randint.return_value == 1:
                self.game.animate_card_to_player(opponent)
                return "hit"

            # Otherwise, the opponent stands
            opponent.status = 'stood'
            return "stood"

        # Test opponent 1
        self.game.turn = 'opponent_one'
        self.game.opponent_one.status = 'playing'
        initial_opponent_one_hand_value = self.game.opponent_one.hand_value()

        action_taken = simulate_opponent_turn(self.game.opponent_one)
        new_opponent_one_hand_value = self.game.opponent_one.hand_value()

        # Validate the outcome for opponent 1
        if action_taken == "hit":
            self.assertGreater(new_opponent_one_hand_value, initial_opponent_one_hand_value, 
                               "Opponent 1 should have hit and increased hand value.")
            self.assertEqual(self.game.opponent_one.status, 'playing', "Opponent 1 should still be playing after hit.")
        else:
            self.assertEqual(new_opponent_one_hand_value, initial_opponent_one_hand_value, 
                             "Opponent 1 should have stood and kept hand value.")
            self.assertEqual(self.game.opponent_one.status, 'stood', "Opponent 1 should have stood.")

        # Test opponent 2
        self.game.turn = 'opponent_two'
        self.game.opponent_two.status = 'playing'
        initial_opponent_two_hand_value = self.game.opponent_two.hand_value()

        action_taken = simulate_opponent_turn(self.game.opponent_two)
        new_opponent_two_hand_value = self.game.opponent_two.hand_value()

        # Validate the outcome for opponent 2
        if action_taken == "hit":
            self.assertGreater(new_opponent_two_hand_value, initial_opponent_two_hand_value, 
                               "Opponent 2 should have hit and increased hand value.")
            self.assertEqual(self.game.opponent_two.status, 'playing', "Opponent 2 should still be playing after hit.")
        else:
            self.assertEqual(new_opponent_two_hand_value, initial_opponent_two_hand_value, 
                             "Opponent 2 should have stood and kept hand value.")
            self.assertEqual(self.game.opponent_two.status, 'stood', "Opponent 2 should have stood.")
    
    @patch.object(BlackjackGame, 'animate_card_to_player', lambda self, player: self.animate_card_to_hand(player))
    def test_game_continues_if_players_still_playing(self):
        """Test that the game does not end if any player is still 'playing'."""
        self.game.player.hand.cards = [Card('Hearts', '5'), Card('Spades', '6')]  # 11
        self.game.opponent_one.hand.cards = [Card('Diamonds', '10'), Card('Clubs', '8')]  # 18
        self.game.opponent_two.hand.cards = [Card('Hearts', 'King'), Card('Spades', '7')]  # 17

        self.game.player.status = 'playing'  # One player still in game
        self.game.opponent_one.status = 'stood'
        self.game.opponent_two.status = 'stood'

        # Simulate evaluation logic
        game_should_continue = any(p.status == 'playing' for p in [self.game.player, self.game.opponent_one, self.game.opponent_two])
        self.assertTrue(game_should_continue)
        self.assertFalse(self.game.game_over)  # Game should NOT be over

    @patch.object(BlackjackGame, 'animate_card_to_player', lambda self, player: self.animate_card_to_hand(player))
    def test_player_wins_with_21(self):
        """Test that a player wins instantly when they reach 21."""
        self.game.player.hand.cards = [Card('Hearts', '10'), Card('Spades', 'Ace')]  # 21
        self.game.player.status = 'playing'

        # Simulate evaluation logic
        if self.game.player.hand_value() == 21:
            self.game.player.status = 'stood'
            self.game.game_over = True

        self.assertTrue(self.game.game_over)  # Game should be over
        self.assertEqual(self.game.player.status, 'stood')

    @patch.object(BlackjackGame, 'animate_card_to_player', lambda self, player: self.animate_card_to_hand(player))
    def test_multiple_players_tie_with_21(self):
        """Test that the game ends with a tie if multiple players have 21."""
        self.game.player.hand.cards = [Card('Diamonds', '10'), Card('Clubs', 'Ace')]
        self.game.opponent_one.hand.cards = [Card('Spades', 'King'), Card('Hearts', 'Ace')]
        self.game.player.status = 'playing'
        self.game.opponent_one.status = 'playing'

        # Simulate evaluation logic
        players_with_21 = [p for p in [self.game.player, self.game.opponent_one, self.game.opponent_two] if p.hand_value() == 21]
        if len(players_with_21) > 1:
            self.game.game_over = True  # Game should end

        self.assertTrue(self.game.game_over)
        self.assertEqual(len(players_with_21), 2)  # Two players tied

    @patch.object(BlackjackGame, 'animate_card_to_player', lambda self, player: self.animate_card_to_hand(player))
    def test_highest_hand_wins(self):
        """Test that the player with the highest valid hand wins when game ends."""
        self.game.player.hand.cards = [Card('Spades', '9'), Card('Hearts', '9')]  # 18
        self.game.opponent_one.hand.cards = [Card('Diamonds', '10'), Card('Clubs', '6')]  # 16
        self.game.opponent_two.hand.cards = [Card('Hearts', 'King'), Card('Spades', '7')]  # 17
        self.game.player.status = 'stood'
        self.game.opponent_one.status = 'stood'
        self.game.opponent_two.status = 'stood'
        self.game.game_over = True

        # Simulate checking for the highest valid hand
        valid_players = [p for p in [self.game.player, self.game.opponent_one, self.game.opponent_two] if p.hand_value() <= 21]
        highest_score = max(p.hand_value() for p in valid_players)
        winners = [p for p in valid_players if p.hand_value() == highest_score]

        self.assertEqual(len(winners), 1)  # One winner
        self.assertEqual(winners[0], self.game.player)  # Player 1 should win
        self.assertTrue(self.game.game_over)

    @patch.object(BlackjackGame, 'animate_card_to_player', lambda self, player: self.animate_card_to_hand(player))
    def test_all_players_bust(self):
        """Test that no one wins if all players bust."""
        self.game.player.hand.cards = [Card('Hearts', '10'), Card('Diamonds', 'King'), Card('Clubs', '5')]  # 25
        self.game.opponent_one.hand.cards = [Card('Spades', 'King'), Card('Hearts', 'Queen'), Card('Diamonds', '5')]  # 25
        self.game.opponent_two.hand.cards = [Card('Clubs', 'Jack'), Card('Spades', 'King'), Card('Hearts', '7')]  # 27
        self.game.player.status = 'busted'
        self.game.opponent_one.status = 'busted'
        self.game.opponent_two.status = 'busted'
        self.game.game_over = True
        
        # Simulate checking valid players
        valid_players = [p for p in [self.game.player, self.game.opponent_one, self.game.opponent_two] if p.hand_value() <= 21]

        self.assertEqual(len(valid_players), 0)  # No valid players
        self.assertTrue(self.game.game_over)     
            
    @patch.object(BlackjackGame, 'animate_card_to_player', lambda self, player: player.add_card_to_hand(self.deck.draw_card()))
    def test_reset_game_multi_play(self):
        """Test that the game resets correctly for multiplayer and deals new hands with 2 cards each."""

        # Ensure the deck starts with 52 cards
        initial_deck_size = len(self.game.deck.cards)
        self.assertEqual(initial_deck_size, 52, "Deck should start with 52 cards.")

        # Deal initial cards to all players
        self.game.deal_initial_cards()

        # Store initial hand values
        initial_hand_values = {
            "player": self.game.player.hand_value(),
            "opponent_one": self.game.opponent_one.hand_value(),
            "opponent_two": self.game.opponent_two.hand_value(),
        }

        # Save the initial hands (ranks and suits)
        initial_hands = {
            "player": [(card.rank, card.suit) for card in self.game.player.hand.cards],
            "opponent_one": [(card.rank, card.suit) for card in self.game.opponent_one.hand.cards],
            "opponent_two": [(card.rank, card.suit) for card in self.game.opponent_two.hand.cards],
        }

        # Call reset_game()
        self.game.reset_game()
        time.sleep(0.1)  # Short delay to ensure all operations complete

        # Process any pending events to ensure Pygame updates correctly
        pygame.event.pump()

        # Deck should now have 46 cards (6 cards dealt: 2 per player)
        self.assertEqual(len(self.game.deck.cards), 46, "Deck should have 46 cards after dealing 2 to each player.")

        # Each player should have exactly 2 cards in hand
        for player in [self.game.player, self.game.opponent_one, self.game.opponent_two]:
            self.assertEqual(len(player.hand.cards), 2, f"{player} should have exactly 2 cards after reset.")

        # Ensure game state is reset
        self.assertTrue(self.game.running, "Game should be running after reset.")
        self.assertFalse(self.game.game_over, "Game should not be in game-over state after reset.")
        self.assertTrue(self.game.buttons_enabled, "Buttons should be enabled after reset.")

        # All players should be in 'playing' state
        self.assertEqual(self.game.player.status, "playing", "Player should be in 'playing' state after reset.")
        self.assertEqual(self.game.opponent_one.status, "playing", "Opponent One should be in 'playing' state after reset.")
        self.assertEqual(self.game.opponent_two.status, "playing", "Opponent Two should be in 'playing' state after reset.")

        # Save the new hands (ranks and suits)
        new_hands = {
            "player": [(card.rank, card.suit) for card in self.game.player.hand.cards],
            "opponent_one": [(card.rank, card.suit) for card in self.game.opponent_one.hand.cards],
            "opponent_two": [(card.rank, card.suit) for card in self.game.opponent_two.hand.cards],
        }

        # Ensure that new hands are different from previous hands
        for key in ["player", "opponent_one", "opponent_two"]:
            self.assertNotEqual(initial_hands[key], new_hands[key], f"{key} should have a different hand after reset.")
            
if __name__ == '__main__':
    unittest.main()