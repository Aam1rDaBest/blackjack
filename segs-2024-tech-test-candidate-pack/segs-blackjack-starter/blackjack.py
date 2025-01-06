from src.deck import Deck
from src.hand import Hand
from src.card import Card
from src.player import Player


class BlackjackGame:
    def __init__(self, num_players):
        self.deck = Deck()
        self.player = Player()
        self.deck.shuffle()

    def deal_initial_cards(self):
        for _ in range(2):  # Player gets 2 cards initially
            self.player.add_card_to_hand(self.deck.draw_card())

    def play(self):
        self.deal_initial_cards()
        print(self.player)
        while self.player.hand_value() < 21:
            action = input(f"Do you want to hit (h) or stand (s)? ")
            if action.lower() == 'h':
                self.player.add_card_to_hand(self.deck.draw_card())
                print(self.player)
            else:
                print("Final",self.player)
                break

        self.determine_winner()

    def determine_winner(self):
        player_value = self.player.hand_value()
        if player_value > 21:
            print(f"Bust!")
        elif player_value == 21:
            print(f"Winner!")


if __name__ == '__main__':
    initial = BlackjackGame(1)
    initial.play()
