import os
import pygame

class Card:
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.image_path = os.path.join("assets", f"cards/{rank.lower()}_of_{suit.lower()}.png")

    def __str__(self):
        return f"{self.rank} of {self.suit}" 
    
    def get_image(self):
        return pygame.image.load(self.image_path)