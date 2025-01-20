import pygame
from random import randint

class Splash:
    def __init__(self, fruit, now):
        self.image = pygame.image.load(f"assets/images/splashes/{fruit.name}_splash_{randint(0, 2)}.png")
        self.image = self.resize_image(self.image, randint(100, 180))
        self.rect = self.image.get_rect(x=fruit.rect.x, y=fruit.rect.y) # Hitbox
        self.image = self.rotate_img(self.image, self.rect, randint(0, 360))

        self.opacity = 160
        self.image.set_alpha(self.opacity)

        self.start = now
        self.lifetime = randint(800, 2500) / 1000
        self.fading = False

    def update(self, now, dt):
        if self.fading:
            self.opacity -= dt * 200
            if self.opacity < 0:
                self.opacity = 0
            self.image.set_alpha(self.opacity)
        else:
            if now - self.start >= self.lifetime:
                self.fading = True
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def rotate_img(self, image, rect, angle):
        rotated_img = pygame.transform.rotate(image, angle)
        self.rect = rotated_img.get_rect(center=rect.center)
        return rotated_img
    
    def resize_image(self, image, width):
        og_width, og_height = image.get_size()
        height = int(width * og_height / og_width) # Calculate new height maintaining the aspect ratio
        return pygame.transform.scale(image, (width, height))