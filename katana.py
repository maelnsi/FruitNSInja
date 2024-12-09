import pygame
from math import sqrt

class Katana:
    def __init__(self):
        self.trail_len = 10
        self.trail = []
        self.width = 10
        self.rect = None
        self.last_pos = None
        self.last_pos_time = 0
        self.vel = 0 # in px/s
        self.slice_vel = 200 # in px/s, minimum velocity to slice fruits
    
    def update_pos(self, pos, now):
        if pos:
            # Calculate velocity
            if self.last_pos:
                dist = sqrt((pos[0]-self.last_pos[0])**2 + (pos[1]-self.last_pos[1])**2)
                dt = now - self.last_pos_time
                if dt > 0:
                    self.vel = dist/dt # in px/s
                    print(int(self.vel))

            self.rect = pygame.Rect(pos, (self.width, self.width))
            self.last_pos = pos
            self.last_pos_time = now
        else:
            self.rect = None

        self.trail.append(pos)
        if len(self.trail) > self.trail_len:
            self.trail.pop(0)
    
    def draw(self, screen):
        # Remove None
        trail = [point for point in self.trail if point]

        if len(trail) >= 2:
            pygame.draw.lines(screen, (100, 100, 100), False, trail, self.width)
            pygame.draw.lines(screen, (255, 255, 255), False, trail, self.width - 6)