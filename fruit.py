import pygame
from random import choice
from sliceable import Sliceable
from random import randint

class Fruit(Sliceable):
    def __init__(self, screen,menu=False, menu_x=0, menu_y=0, menu_size=180):
        # Pick random fruit
        self.screen = screen
        fruit_names = ["apple", "banana", "cherry", "dragonfruit", "lime"]
        self.name = choice(fruit_names)
        self.menu=menu
        # Pass the screen and image to the Sliceable class using super()
        super().__init__(screen, f"assets/images/fruits/{self.name}.png")
        self.sound = pygame.mixer.Sound("assets/sounds/slice.mp3")
        self.sound.set_volume(0.5)
        if menu:
            self.rect.x=menu_x
            self.rect.y=menu_y
            self.velocity=[0,0]
            self.gravity=0
            self.image=self.resize_image(self.image, menu_size)
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
            if self.menu:
                half.image=half.resize_image(half.image, self.image.get_width())
            half.rect.center = self.rect.center
            half.sliced = True
            half.velocity = self.velocity.copy() # Change halfs velocities
            for i in (0, 1):
                half.velocity[i] += randint(-200, 200)
        
        return halfs