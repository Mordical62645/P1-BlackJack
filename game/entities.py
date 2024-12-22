import pygame

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        self.image = None

    def load_image(self):
        if self.image is None:
            self.image = pygame.image.load(f"graphics/Cards/{self.value}{self.suit}.png")

    def __repr__(self):
        return f"{self.value}{self.suit}"

