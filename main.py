import cv2
import mediapipe as mp
import pygame
import numpy as np
from random import randint
from fruit import Fruit

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.dt = 0
        self.clock = pygame.time.Clock()

        self.fruits = []
        self.next_wave = 0
        self.active_wave = False

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.fruits.append(Fruit(self.screen))

    def hand_tracking(self):
        self.hand1 = None
        self.hand2 = None

        r, self.frame = capture.read()
        spotted_hands = hands.process(self.frame).multi_hand_landmarks
        if spotted_hands:
            self.hand1 = spotted_hands[0]
            if len(spotted_hands) > 1:
                self.hand2 = spotted_hands[1]
    
    def update(self):
        self.hand_tracking()

        # Move fruits
        despawn_idx = -1 # index of fruit that has to despawn
        for i in range(len(self.fruits)):
            self.fruits[i].move(self.dt)

            if self.fruits[i].rect.y > screen.get_height() + 20:
                despawn_idx = i
        
        if despawn_idx != -1:
            self.fruits.pop(despawn_idx)

        if self.active_wave:
            if len(self.fruits) == 0:
                self.active_wave = False
                self.next_wave = now + randint(500, 3000)
                print("Next wave in", (self.next_wave - now)/1000)
        elif now >= self.next_wave:
            self.spawn_wave()
            self.active_wave = True

    def display(self):
        # Draw hands on camera frame
        if self.hand1:
            mp_drawing.draw_landmarks(self.frame, self.hand1, mp_hands.HAND_CONNECTIONS)
        if self.hand2:
            mp_drawing.draw_landmarks(self.frame, self.hand2, mp_hands.HAND_CONNECTIONS)

        # Convert OpenCV camera frame to Pygame image
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
        self.frame = np.rot90(self.frame)
        self.frame = pygame.surfarray.make_surface(self.frame)

        # Display camera frame with hands
        self.screen.blit(self.frame, (0, 0))

        # Display fruits
        for fruit in self.fruits:
            fruit.draw(self.screen)
            
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handling_events()
            self.update()
            self.display()
            self.dt = self.clock.tick(30) / 1000
    
    def spawn_wave(self):
        print("Wave spawned !")
        for i in range(randint(1,6)):
            self.fruits.append(Fruit(self.screen))

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