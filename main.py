import cv2
import mediapipe as mp
import pygame
import numpy as np
from random import randint
from fruit import Fruit
from bomb import Bomb
from katana import Katana
from ui import UserInterface

class Game:
    def __init__(self, screen, capture):
        # Pygame
        self.screen = screen
        self.running = True
        self.clock = pygame.time.Clock()
        self.dt = 0
        
        # Game components
        self.score = 0
        self.lives = 3
        self.sliceables = []
        self.next_wave = 999999
        self.active_wave = False
        self.finger_pos = None
        self.katana = Katana()
        self.ui = UserInterface()
        self.ingame = False
        self.died = False
        
        # Hand tracking with mediapipe
        self.capture = capture
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.4, min_tracking_confidence=0.1)
    	
        # Music
        self.whoosh=pygame.mixer.Sound("assets/sounds/whoosh.mp3")
        self.bomb_sound=pygame.mixer.Sound("assets/sounds/fuse.mp3")
        self.bomb_explosion=pygame.mixer.Sound("assets/sounds/explosion.mp3")
        self.strike=pygame.mixer.Sound("assets/sounds/strike.mp3")
        pygame.mixer.music.load('assets/sounds/beijing.mp3')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        self.load_menu()

    def start(self,now):
        self.score = 0
        self.lives = 3
        self.next_wave = now + 3 
        self.active_wave = False
        self.ingame = True
    
    def stop(self, now):
        self.active_wave = False
        self.next_wave = 99999999999999
        self.died = True
        self.menu_time = now + 1

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.sliceables.append(Fruit(self.screen))
    
    def update(self):
        now = pygame.time.get_ticks() / 1000

        # Move fruits/bombs
        despawn_idx = -1 # index of fruit that has to despawn
        for i in range(len(self.sliceables)):
            self.sliceables[i].update(self.dt)
            if self.sliceables[i].rect.y > screen.get_height() + 20:
                despawn_idx = i
            if isinstance(self.sliceables[i],Bomb):
                self.sliceables[i].animate(now)

        # Despawn fruits/bombs that are off-screen
        if despawn_idx != -1:
            # Lose a life if fruit not sliced
            if isinstance(self.sliceables[despawn_idx], Fruit) and not self.sliceables[despawn_idx].sliced:
               self.lives -= 1
               pygame.mixer.Sound.play(self.strike)
               if self.lives == 0:
                    self.stop(now)
                    self.load_menu()
            if self.ingame:
                self.sliceables.pop(despawn_idx)

        # Slice fruits/bombs
        if not self.died and len(self.katana.trail) >= 2 and self.katana.vel >= self.katana.slice_vel:
            for sliceable in self.sliceables:
                if not sliceable.sliced and sliceable.rect.clipline(self.katana.trail[-1], self.katana.trail[-2]):
                    # Check if sliced a bomb
                    if isinstance(sliceable, Bomb):
                        sliceable.slice()
                        pygame.mixer.Sound.play(self.bomb_explosion)
                        self.stop(now)
                        
                        # Freeze time
                        for s in self.sliceables:
                            s.velocity = [0, 0]
                            s.gravity = 0
                            s.rotate_vel = 0
                    else:
                        halfs = sliceable.slice()
                        # Add fruit halfs to sliceables list
                        for half in halfs:
                            self.sliceables.append(half)
                        if self.ingame:
                            self.score += 1
                            # Gain a life each 100 points
                            if self.score % 100 == 0 and self.lives < 3:
                                self.lives += 1
                        else:
                            self.start(now)
                            self.sliceables.pop(0)
                            
        if self.died and now >= self.menu_time:
            self.load_menu()
            self.died = False

        # Spawn fruits wave
        if self.active_wave:
            if self.wave_spawned_sliceables < self.wave_size:
                if now - self.wave_last_sliceable >= self.wave_interval:
                    if randint(1, 6) == 1:
                        self.sliceables.append(Bomb(self.screen))
                        pygame.mixer.Sound.play(self.bomb_sound)
                    else:
                        self.sliceables.append(Fruit(self.screen))
                    pygame.mixer.Sound.play(self.whoosh)
                    self.wave_spawned_sliceables += 1
                    self.wave_last_sliceable = now
            # End wave
            elif self.wave_spawned_sliceables >= self.wave_size and len(self.sliceables) == 0:
                self.active_wave = False
                self.next_wave = now + randint(500,3000)/1000
                print("Next wave in", self.next_wave - now)

        elif now >= self.next_wave:
            if randint(0, 1):
                # Wave with all fruits at the same time
                self.wave_size = randint(1,4)
                self.wave_interval = 0
            else:
                # Wave with interval between fruits
                self.wave_size = randint(2,8)
                self.wave_interval = randint(400, 1000) / 1000

            self.wave_spawned_sliceables = 0
            self.wave_last_sliceable = 0
            self.active_wave = True

        # UI
        self.ui.update(now)

        # Hand tracking
        if self.hand_tracking():
            self.katana.update(self.finger_pos, now)
        else:
            self.katana.remove_oldest_pos()
    
    def load_menu(self):
        self.ingame = False
        self.sliceables = []
        play_fruit=Fruit(screen, True, 250, 250, 150)
        self.sliceables.append(play_fruit)

    def display(self):
        # Convert OpenCV camera frame to Pygame image
        self.frame = np.rot90(self.frame)
        self.frame = pygame.surfarray.make_surface(self.frame)

        # Display camera frame with hands
        self.screen.blit(self.frame, (0, 0))
        
        # Display fruits
        for sliceable in self.sliceables:
            if isinstance(sliceable, Fruit) and sliceable.sliced:
                continue
            sliceable.draw(self.screen)
        
        # Display UI
        if self.ingame:    
            self.ui.draw_game(self.screen, self.score, self.lives)
        else:
            self.ui.draw_menu(self.screen) #Main Menu
            
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
    
    def hand_tracking(self):
        r, self.frame = self.capture.read()
        
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) # Convert the BGR image to RGB before processing.
        spotted_hands = self.hands.process(self.frame).multi_hand_landmarks
        if spotted_hands:
            hand = spotted_hands[0]
            #self.mp_drawing.draw_landmarks(self.frame, hand, self.mp_hands.HAND_CONNECTIONS)
            
            # Computer finger coordinates
            finger = hand.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
            frame_h, frame_w, _ = self.frame.shape
            x = frame_w - (finger.x * frame_w)
            y = finger.y * frame_h
            self.finger_pos = [x, y]
            return True
        return False

# Start webcam
capture = cv2.VideoCapture(0)

# Pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Fruit NSInja")

# Game
game = Game(screen, capture)
game.run()

# Deinitialize
pygame.quit()

cv2.destroyAllWindows()

# combos
# speed up
# game over
# splash
