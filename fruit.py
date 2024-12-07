import pygame
import random

fruit_names = ["apple", "banana", "blueberry", "pineapple", "strawberry", "watermelon"]

class Fruit:
    def __init__(self, screen):
        # Pick random fruit
        self.name = random.choice(fruit_names)

        # Load image
        self.image = pygame.image.load(f"img/fruits/{self.name}.png")
        size = (100, 100)
        self.image = pygame.transform.scale(self.image, size)

        # Spawn fruit
        x = random.randint(0, screen.get_width() - self.image.get_width())
        y = screen.get_height()
        self.rect = self.image.get_rect(x=x, y=y) # Hitbox

        # Throw fruit
        x_vel = random.randint(-10, 10)
        y_vel = random.randint(-400, -300)
        self.velocity = [x_vel, y_vel] # Vel
        self.gravity = 50
    
    def move(self, dt):
        self.rect.x += self.velocity[0] * dt
        self.rect.y += self.velocity[1] * dt

        # Physics
        self.velocity[1] += self.gravity * dt
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)