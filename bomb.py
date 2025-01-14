import pygame
from sliceable import Sliceable

class Bomb(Sliceable):
    def __init__(self, screen):
        super().__init__(screen, "assets/images/bomb/bomb_0.png")
        self.frames=[]
        for i in range(3):
            img = pygame.image.load(f'assets/images/bomb/bomb_{i}.png')
            self.frames.append(self.resize_image(img, 75))
        self.frame_idx=0
        self.frame_interval=0.1
        self.last_frame=0
        
        self.explosion_frames = []
        for i in range(7):
            img = pygame.image.load(f'assets/images/bomb/explosion_{i}.png')
            self.explosion_frames.append(self.resize_image(img, 120))
        self.explosion_idx=0
        self.explosion_interval=0.05
        self.explosion_last_frame=0
        
        print("bomb", self.rect.x, self.velocity[0], self.velocity[1])
    
    def animate(self,now):
        if self.sliced:
            if self.explosion_idx < 7 and now - self.explosion_last_frame >= self.explosion_interval:
                self.image=self.explosion_frames[self.explosion_idx]
                self.explosion_last_frame = now
                self.explosion_idx+=1
        elif now - self.last_frame >= self.frame_interval:
            self.image=self.frames[self.frame_idx]
            self.last_frame = now
            self.frame_idx+=1
            if self.frame_idx > 2:
                self.frame_idx = 0
    
    def slice(self):
        self.sliced = True
        print("Game over!")