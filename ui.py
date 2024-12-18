import pygame
from font import Font
from random import randint

class UserInterface:
    def __init__(self):
        self.font = Font('assets/font', 60)

        self.x_blue = pygame.image.load('assets/x_blue.png')
        self.x_blue = self.resize_image(self.x_blue, 50)
        self.x_red = pygame.image.load('assets/x_red.png')
        self.x_red = self.resize_image(self.x_red, 50)
        
        self.x_red_frames = []
        for i in range(3):
            self.x_red_frames.append(self.resize_image(pygame.image.load(f'assets/x_red_{i}.png'), 50))
        self.animating_x_red = False
        self.x_red_anim_idx = 0
        self.x_red_anim_start = 0
        self.x_red_anim_interval = 0.2
        self.next_x_red_anim = 0

    def update(self, now):
        if self.animating_x_red:
            if now - self.x_red_anim_start >= self.x_red_anim_interval*(self.x_red_anim_idx + 1):
                self.x_red_anim_idx += 1
                if self.x_red_anim_idx > len(self.x_red_frames) - 1:
                    self.animating_x_red = False
                    self.next_x_red_anim = now + (randint(2000, 8000)/1000)
        elif now >= self.next_x_red_anim:
            self.x_red_anim_idx = 0
            self.x_red_anim_start = now
            self.animating_x_red = True

    def draw(self, screen, score, lives):
        self.font.display(screen, str(score), 20, 20, 2)

        for i in range(3):
            if lives > i:
                screen.blit(self.x_blue, (screen.get_width() - (i+1)*60, 20))
            else:
                if self.animating_x_red:
                    screen.blit(self.x_red_frames[self.x_red_anim_idx], (screen.get_width() - (i+1)*60, 20))
                else:
                    screen.blit(self.x_red, (screen.get_width() - (i+1)*60, 20))
    
    def resize_image(self, image, width):
        og_width, og_height = image.get_size()
        height = int(width * og_height / og_width) # Calculate new height maintaining the aspect ratio
        return pygame.transform.scale(image, (width, height))