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
        super().__init__(screen, f"assets/fruits/{self.name}.png")

        self.sound = pygame.mixer.Sound("sfx/slice.mp3")
        print(self.name, self.rect.x, self.velocity[0], self.velocity[1])

    def slice(self):
        self.sliced = True
        pygame.mixer.Sound.play(self.sound)

        # Create two halves of the fruit and give them independent velocities
        self.split_fruit()

    def split_fruit(self):
        # Load the sliced fruit images (assuming the image name ends with _sliced.png)
        half1_image = pygame.image.load(f"assets/fruits/{self.name}_sliced_1.png")
        half2_image = pygame.image.load(f"assets/fruits/{self.name}_sliced_2.png")

        # Resize both halves
        half1_image = self.resize_image(half1_image, 80)
        half2_image = self.resize_image(half2_image, 80)

        # Create two Sliceable objects (representing the halves) using the screen from the parent (Sliceable)
        # Ensure we pass the correct screen here
        self.half1 = Sliceable(self.screen, half1_image)
        self.half2 = Sliceable(self.screen, half2_image)
        # Set the position of the halves to match the original fruit's position
        self.half1.rect.center = self.rect.center
        self.half2.rect.center = self.rect.center
        # Set different velocities and gravity for the halves
        self.half1.velocity = [randint(-100, 100), randint(-500, -300)]
        self.half2.velocity = [randint(-100, 100), randint(-500, -300)]

        # Optionally adjust the gravity, rotation, and other properties if needed
        self.half1.gravity = 400
        self.half2.gravity = 400

    def update(self, dt):
        # Update the original fruit and the two halves (if sliced)
        if not self.sliced:
            super().update(dt)  # Update the original fruit (falling, rotation)
        else:
            self.half1.update(dt)  # Update the first half
            self.half2.update(dt)  # Update the second half

    def draw(self, screen):
        # Draw the original fruit or the halves (if sliced)
        if not self.sliced:
            super().draw(screen)  # Draw the original fruit
        else:
            self.half1.draw(screen)  # Draw the first half
            self.half2.draw(screen)  # Draw the second half
