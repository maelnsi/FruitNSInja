import pygame
from random import randint

class Sliceable:
    def __init__(self, screen, img_path, menu=False, menu_x=0, menu_y=0):
        
        self.image = pygame.image.load(img_path)
        self.image = self.resize_image(self.image, 115)

        # Spawn
        margin_x = 80
        x = randint(margin_x, screen.get_width() - self.image.get_width() - margin_x)
        y = screen.get_height()
        self.rect = self.image.get_rect(x=x, y=y) # Hitbox

        # Throw
        x_vel = randint(0, 120)
        if self.rect.x > screen.get_width() - self.image.get_width() - margin_x * 2:
            x_vel *= -1
        elif self.rect.x > margin_x * 2 and randint(0, 1):
            x_vel *= -1
        self.velocity = [x_vel, randint(-600, -400)] # in px/s
        self.gravity = 400 # in px/s^2
        self.rotate_vel = randint(-200, 200) # in deg/s
        self.angle = randint(0, 360)
        self.sliced = False

    
    def update(self, dt):
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
    
    def resize_image(self, image, width):
        og_width, og_height = image.get_size()
        height = int(width * og_height / og_width) # Calculate new height maintaining the aspect ratio
        return pygame.transform.scale(image, (width, height))