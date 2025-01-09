import pygame
from random import choice
from sliceable import Sliceable

class Fruit(Sliceable):
    def __init__(self, screen):
        # Pick random fruit
        fruit_names = ["apple", "banana", "blueberry", "pineapple", "strawberry", "watermelon"]
        self.name = choice(fruit_names)
        super().__init__(screen, f"assets/fruits/{self.name}.png")
        self.sound = pygame.mixer.Sound("sfx/slice.mp3")
        print(self.name, self.rect.x, self.velocity[0], self.velocity[1])
    
    def slice(self):
        self.sliced = True
        pygame.mixer.Sound.play(self.sound)
        # Change image
        self.image = pygame.image.load(f"assets/fruits/{self.name}_sliced.png")
        self.image = self.resize_image(self.image, 80)