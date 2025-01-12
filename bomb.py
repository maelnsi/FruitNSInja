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
        self.frame_interval=0.4
        self.last_frame=0
        print("bomb", self.rect.x, self.velocity[0], self.velocity[1])
    
    
    def animate(self,now):
        if now - self.last_frame >= self.frame_interval:
            self.frame_idx+=1
            if self.frame_idx > 2:
                self.frame_idx = 0
            self.image=self.frames[self.frame_idx]
    
    def slice(self):
        self.sliced = True
        print("Game over!")