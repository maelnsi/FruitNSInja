import pygame
from sliceable import Sliceable

class Bomb(Sliceable):
    def __init__(self, screen):
        super().__init__(screen, "assets/bomb.png")
        print("bomb", self.rect.x, self.velocity[0], self.velocity[1])
    
    def slice(self):
        self.sliced = True
        print("Game over!")