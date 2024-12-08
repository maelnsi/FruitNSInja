import pygame
from random import randint, choice

fruit_names = ["apple", "banana", "blueberry", "pineapple", "strawberry", "watermelon"]

class Fruit:
    def __init__(self, screen):
        # Pick random fruit
        self.name = choice(fruit_names)

        # Load image
        self.image = pygame.image.load(f"assets/fruits/{self.name}.png")
        self.image = self.resize_image(self.image, 80)

        # Spawn fruit
        margin_x = 80
        x = randint(margin_x, screen.get_width() - self.image.get_width() - margin_x)
        y = screen.get_height()
        self.rect = self.image.get_rect(x=x, y=y) # Hitbox

        # Throw fruit
        x_vel = randint(0, 120)
        if self.rect.x > screen.get_width() - self.image.get_width() - margin_x*2:
            x_vel *= -1
        elif self.rect.x > margin_x*2 and randint(0,1):
            x_vel *= -1
        self.velocity = [x_vel, randint(-600, -400)] # in px/s
        self.gravity = 400 # in px/s^2
        self.rotate_vel = randint(-200, 200) # in deg/s
        self.angle = randint(0,360)
        self.sliced = False
        
        print(self.name, self.rect.x, self.velocity[0], self.velocity[1])
    
    def move(self, dt):
        # Physics
        self.rect.x += self.velocity[0] * dt
        self.rect.y += self.velocity[1] * dt
        self.velocity[1] += self.gravity * dt

        self.angle += self.rotate_vel * dt
    
    def slice(self):
        self.sliced = True

        # Change image
        self.image = pygame.image.load(f"assets/fruits/{self.name}_sliced.png")
        self.image = self.resize_image(self.image, 80)
    
    def draw(self, screen):
        screen.blit(self.rotate_img(self.image, self.rect, self.angle), self.rect)
    
    def rotate_img(self, image, rect, angle):
        rotated_img = pygame.transform.rotate(image, angle)
        self.rect = rotated_img.get_rect(center=rect.center)
        return rotated_img
    
    def resize_image(self, image, width):
        og_width, og_height = image.get_size()
        height = int(width * og_height / og_width) # Calculate new height maintaining the aspect ratio
        return pygame.transform.scale(image, (width, height))