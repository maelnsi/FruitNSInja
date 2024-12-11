import cv2
import mediapipe as mp
import pygame
import numpy as np
from random import randint
from fruit import Fruit
from bomb import Bomb
from katana import Katana

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.dt = 0
        self.clock = pygame.time.Clock()

        self.sliceables = []
        self.next_wave = 0
        self.active_wave = False
        self.finger_pos = None
        
        self.katana = Katana()

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.sliceables.append(Fruit(self.screen))

    def hand_tracking(self):
        r, self.frame = capture.read()
        
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) # Convert the BGR image to RGB before processing.
        spotted_hands = hands.process(self.frame).multi_hand_landmarks
        if spotted_hands:
            hand = spotted_hands[0]
            mp_drawing.draw_landmarks(self.frame, hand, mp_hands.HAND_CONNECTIONS)
            
            # Computer finger coordinates
            finger = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            frame_h, frame_w, _ = self.frame.shape
            x = frame_w - (finger.x * frame_w)
            y = finger.y * frame_h
            self.finger_pos = [x, y]
            return True
        return False

    
    def update(self):
        now = pygame.time.get_ticks() / 1000

        # Move fruits/bombs
        despawn_idx = -1 # index of fruit that has to despawn
        for i in range(len(self.sliceables)):
            self.sliceables[i].update(self.dt)
            if self.sliceables[i].rect.y > screen.get_height() + 20:
                despawn_idx = i
        
        # Despawn fruits/bombs that are off-screen
        if despawn_idx != -1:
            self.sliceables.pop(despawn_idx)

        # Slice fruits/bombs
        if len(self.katana.trail) >= 2 and self.katana.vel >= self.katana.slice_vel:
            for sliceable in self.sliceables:
                if not sliceable.sliced and sliceable.rect.clipline(self.katana.trail[-1], self.katana.trail[-2]):
                    sliceable.slice()
                    # check if sliced a bomb
                    if isinstance(sliceable, Bomb):
                        self.running = False

        # Spawn fruits wave
        if self.active_wave:
            if len(self.sliceables) == 0:
                self.active_wave = False
                self.next_wave = now + (randint(500, 2000)/1000)
                print("Next wave in", self.next_wave - now)
        elif now >= self.next_wave:
            self.spawn_wave()
            self.active_wave = True

        # Hand tracking
        if self.hand_tracking():
            self.katana.update(self.finger_pos, now)
        else:
            self.katana.remove_oldest_pos()

    def display(self):
        # Convert OpenCV camera frame to Pygame image
        self.frame = np.rot90(self.frame)
        self.frame = pygame.surfarray.make_surface(self.frame)

        # Display camera frame with hands
        self.screen.blit(self.frame, (0, 0))

        # Display fruits
        for sliceable in self.sliceables:
            sliceable.draw(self.screen)

        # Display katana
        self.katana.draw(self.screen)
        
        # Update display
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handling_events()
            self.update()
            self.display()
            self.dt = self.clock.tick(30) / 1000
    
    def spawn_wave(self):
        print("Wave spawned !")
        for i in range(randint(1,5)):
            self.sliceables.append(Fruit(self.screen))
            if randint(0,10) == 0:
                self.sliceables.append(Bomb(self.screen))

# Hand tracking with mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

print("Starting video...")
capture = cv2.VideoCapture(0)

# Pygame
print("Starting Pygame...")
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Fruit NSInja")

game = Game(screen)
game.run()

pygame.quit()
cv2.destroyAllWindows()