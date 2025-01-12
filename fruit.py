import pygame
from random import choice
from sliceable import Sliceable
from random import randint

class Fruit(Sliceable):
    def __init__(self, screen):
        # Pick random fruit
        self.screen = screen
        fruit_names = ["apple", "banana", "blueberry", "pineapple", "strawberry", "watermelon"]
        self.name = choice(fruit_names)

        # Pass the screen and image to the Sliceable class using super()
        super().__init__(screen, f"assets/images/fruits/{self.name}.png")

        self.sound = pygame.mixer.Sound("assets/sounds/slice.mp3")
        print(self.name, self.rect.x, self.velocity[0], self.velocity[1])

    def slice(self):
        self.sliced = True
        pygame.mixer.Sound.play(self.sound)

        # Create two Sliceable objects (representing the halves) using the screen from the parent (Sliceable)
        halfs = []
        for i in range(2):
            halfs.append(Sliceable(self.screen, f"assets/images/fruits/{self.name}_sliced_{i+1}.png"))

        # Set the position of the halves to match the original fruit's position
        for half in halfs:
            half.rect.center = self.rect.center
            half.sliced = True

        # Change halfs velocities
        for half in halfs:
            half.velocity = self.velocity.copy()
            for i in (0, 1):
                half.velocity[i] += randint(-200, 200)

        return halfs