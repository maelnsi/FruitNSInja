import cv2
import mediapipe as mp
import pygame
import numpy as np
from fruit import Fruit

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.dt = 0
        self.clock = pygame.time.Clock()

        self.fruit = Fruit(screen)

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

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

        # Move fruit
        self.fruit.move(self.dt)

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

        self.fruit.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handling_events()
            self.update()
            self.display()
            self.dt = self.clock.tick(30) / 1000

# Hand tracking with mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
capture = cv2.VideoCapture(0)

# Pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Fruit NSInja")

game = Game(screen)
game.run()

pygame.quit()
cv2.destroyAllWindows()