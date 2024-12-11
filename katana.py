import pygame
from math import sqrt

class Katana:
    def __init__(self):
        self.trail = []
        self.trail_len = 10
        self.width = 10
        self.last_pos_time = 0
        self.vel = 0 # in px/s
        self.slice_vel = 200 # in px/s, minimum velocity to slice fruits

    def update_pos(self, pos, now):
        # Calculate velocity
        if len(self.trail):
            dist = sqrt((pos[0]-self.trail[-1][0])**2 + (pos[1]-self.trail[-1][1])**2)
            dt = now - self.last_pos_time
            self.vel = dist/dt # in px/s
            
        self.last_pos_time = now
        self.trail.append(pos)
        if len(self.trail) > self.trail_len:
            self.remove_oldest_pos()
    
    def remove_oldest_pos(self):
        if len(self.trail):
            self.trail.pop(0)
    
    def draw(self, screen):
        if len(self.trail) >= 2:
            pygame.draw.lines(screen, (100, 100, 100), False, self.trail, self.width)
            pygame.draw.lines(screen, (255, 255, 255), False, self.trail, self.width - 6)