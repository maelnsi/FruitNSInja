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

        # Spawn fruit
        margin_x = 100
        x = randint(margin_x, screen.get_width() - self.image.get_width() - margin_x)
        y = screen.get_height()
        self.rect = self.image.get_rect(x=x, y=y) # Hitbox

        # Throw fruit
        self.velocity = [randint(-120, 120), randint(-800, -600)] # in px/s
        self.gravity = 800 # in px/s^2
        self.rotate_vel = randint(-180, 180) # in deg/s
        self.angle = randint(0,360)
        
        print(self.name, self.velocity[0], self.velocity[1], self.rotate_vel)
    
    def move(self, dt):
        # Physics
        self.rect.x += self.velocity[0] * dt
        self.rect.y += self.velocity[1] * dt
        self.velocity[1] += self.gravity * dt

        self.angle += self.rotate_vel * dt
    
    def draw(self, screen):
        screen.blit(self.rotate_img(self.image, self.rect, self.angle), self.rect)
    
    def rotate_img(self, image, rect, angle):
        rotated_img = pygame.transform.rotate(image, angle)
        self.rect = rotated_img.get_rect(center=rect.center)
        return rotated_img