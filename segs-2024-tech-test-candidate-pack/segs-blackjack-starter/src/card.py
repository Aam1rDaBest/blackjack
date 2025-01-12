import os
import pygame

class Card:
    def __init__(self,suit,rank, face_up=False):
        self.suit = suit
        self.rank = rank
        self.image_path = os.path.join("assets", f"cards/{rank.lower()}_of_{suit.lower()}.png")
        self.image_path_two = os.path.join("assets","")
        self.face_up = face_up

    def flip(self):
        self.face_up = not self.face_up
        
    def __str__(self):
        return f"{self.rank} of {self.suit}" 
    
    def get_image(self):
        if self.face_up:
            return pygame.image.load(self.image_path)
        else:
            return pygame.image.load(os.path.join("assets", "card_back_red.png"))
    