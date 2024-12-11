import pygame
from sliceable import Sliceable

class Bomb(Sliceable):
    def __init__(self, screen):
        super().__init__(screen, "assets/bomb.png")
    
    def slice(self):
        self.sliced = True
        print("Lost")