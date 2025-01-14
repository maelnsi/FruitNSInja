import pygame
from font import Font
from random import randint
from math import cos,radians

class UserInterface:
    def __init__(self):
        self.logo = pygame.image.load("assets/images/ui/logo.png")
        self.logosize = 500
        self.logo = self.resize_image(self.logo, self.logosize)

        self.font = Font('assets/images/font', 60)

        self.score_icon = pygame.image.load("assets/images/ui/score_icon.png")
        self.score_icon = self.resize_image(self.score_icon, 85)
        self.score_icon = pygame.transform.rotate(self.score_icon, 50)

        self.x_blue_images = []
        img = pygame.image.load('assets/images/ui/x_blue.png')
        for i in range(3):
            self.x_blue_images.append(self.resize_image(img, 70-i*10))

        self.x_red_images = []
        img = pygame.image.load('assets/images/ui/x_red.png')
        for i in range(3):
            self.x_red_images.append(self.resize_image(img, 70-i*10))
        
        self.x_red_frames = []
        for i in range(3):
            self.x_red_frames.append([])
            for j in range(3):
                img = pygame.image.load(f'assets/images/ui/x_red_{j}.png')
                self.x_red_frames[i].append(self.resize_image(img, 70-i*10))

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
        self.logosize += cos(radians(now)*150)*4
       

    def draw_menu(self,screen):
        resizedlogo = self.resize_image(self.logo, self.logosize)
        screen.blit(resizedlogo,(screen.get_width() / 2 - resizedlogo.get_width() / 2, 50))
    
    
    def draw_game(self, screen, score, lives):
        screen.blit(self.score_icon, (-30, -25))
        self.font.display(screen, str(score), 80, 12, 2)

        x = screen.get_width() - 8
        for i in range(3):
            x -= self.x_blue_images[i].get_width()
            if i>0:
                x -= 5

            if lives > i:
                screen.blit(self.x_blue_images[i], (x, 8))
            else:
                if self.animating_x_red:
                    screen.blit(self.x_red_frames[i][self.x_red_anim_idx], (x, 8))
                else:
                    screen.blit(self.x_red_images[i], (x, 8))
    
    def resize_image(self, image, width):
        og_width, og_height = image.get_size()
        height = int(width * og_height / og_width) # Calculate new height maintaining the aspect ratio
        return pygame.transform.scale(image, (width, height))