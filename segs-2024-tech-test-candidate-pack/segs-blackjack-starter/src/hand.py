class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

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