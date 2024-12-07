import cv2
import mediapipe as mp
import pygame
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Fruit NSInja")
clock = pygame.time.Clock()

apple_img = pygame.image.load("img/fruits/apple.png").convert_alpha()
apple_img = pygame.transform.scale(apple_img, (100, 100))

banana_xy = [300, 480]
banana_vel = 40

gravity = 2

capture = cv2.VideoCapture(0)
running = True

while running:
    r, frame = capture.read()
    
    results = hands.process(frame)
    
    hand1 = None 
    hand2 = None
    
    if results.multi_hand_landmarks:
        hand1 = results.multi_hand_landmarks[0]
        if len(results.multi_hand_landmarks) > 1:
            hand2 = results.multi_hand_landmarks[1]
    
    if(hand1):
        mp_drawing.draw_landmarks(frame, hand1, mp_hands.HAND_CONNECTIONS)
    if(hand2):
        mp_drawing.draw_landmarks(frame, hand2, mp_hands.HAND_CONNECTIONS)
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)
    
    screen.blit(frame, (0, 0))
    screen.blit(apple_img, banana_xy)
    pygame.display.update()
    
    banana_xy[1] -= banana_vel
    banana_vel -= gravity
    
    clock.tick(30)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
cv2.destroyAllWindows()