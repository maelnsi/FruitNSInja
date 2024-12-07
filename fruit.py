import pygame
from random import randint, choice

fruit_names = ["apple", "banana", "blueberry", "pineapple", "strawberry", "watermelon"]

class Fruit:
    def __init__(self, screen):
        # Pick random fruit
        self.name = choice(fruit_names)

        # Load image
        self.image = pygame.image.load(f"img/fruits/{self.name}.png")
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.image = pygame.transform.rotate(self.image, randint(0, 360))

        # Spawn fruit
        margin_x = 100
        x = randint(margin_x, screen.get_width() - self.image.get_width() - margin_x)
        y = screen.get_height()
        self.rect = self.image.get_rect(x=x, y=y) # Hitbox

        # Throw fruit
        self.velocity = [randint(-120, 120), randint(-800, -600)] # in px/s
        self.gravity = 800 # in px/s^2
        self.rotate_vel = randint(20, 200) # in deg/s
        
        print(self.name, self.velocity[0], self.velocity[1], self.rotate_vel)
    
    def move(self, dt):
        # Physics
        self.rect.x += self.velocity[0] * dt
        self.rect.y += self.velocity[1] * dt
        self.velocity[1] += self.gravity * dt
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)