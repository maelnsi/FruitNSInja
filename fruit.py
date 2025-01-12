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
        
        # Create two Sliceable objects for the halves
        halves = []
        for i in range(2):
            halves.append(Sliceable(self.screen, f"assets/images/fruits/{self.name}_sliced_{i+1}.png"))

        # Set the position of the halves to match the original fruit's position
        for half in halves:
            if self.menu:
                half.image=half.resize_image(half.image, self.image.get_width())
            half.rect.center = self.rect.center
            half.sliced = True

            if randint(0,1):
                half.velocity[0] = self.velocity[0] + randint(50, 300)
            else:
                half.velocity[0] = self.velocity[0] - randint(50, 300)

            half.velocity[1] = randint(0, 100)
        
        return halves