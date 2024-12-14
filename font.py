import pygame
from os import listdir

class Font:
    def __init__(self, dir, size):
        self.font = {}
        for file_name in listdir(dir):
            char = file_name[0]
            img = pygame.image.load(dir + '/' + file_name)
            img = self.resize_image(img, size)
            self.font[char] = img
    
    def display(self, screen, text, x, y, spacing):
        new_x = x
        for char in text:
            img = self.font[char]
            screen.blit(img, (new_x, y))
            new_x += img.get_width() + spacing
    
    def resize_image(self, image, height):
        og_width, og_height = image.get_size()
        width = int(height * og_width / og_height) # Calculate new height maintaining the aspect ratio
        return pygame.transform.scale(image, (width, height))