# player.py
import pygame
from settings import *

class Player:
    def __init__(self):
        self.size = 40
        self.start_x = 100
        self.floor_y = HEIGHT - 100
        self.ceiling_y = 100
        self.rect = pygame.Rect(self.start_x, self.floor_y - self.size, self.size, self.size)
        
        self.y_velocity = 0
        self.is_jumping = False
        self.is_holding_space = False
        self.mode = 'cube'
        
        self.gravity = 0.8
        self.jump_force = -16
        self.boost_force = -25
        
        # AANGEPAST: Standaardwaarden voor Ship (worden in reset overschreven)
        self.ship_gravity = 0.25
        self.ship_lift = 0.4
        self.ship_max_speed = 4

    def reset(self, gravity_mod, level_num):
        self.floor_y = HEIGHT - 100
        self.ceiling_y = 100
        self.rect.y = self.floor_y - self.size
        self.y_velocity = 0
        self.is_jumping = False
        self.is_holding_space = False
        self.mode = 'cube'
        
        self.gravity = 0.8 * gravity_mod
        self.jump_force = -16 * gravity_mod
        self.boost_force = -25
        
        # --- AANGEPAST: VEEL TRAGERE SHIP FYSICA ---
        # Vroeger was dit 0.6 en 1.0. Nu veel lager voor meer controle.
        self.ship_gravity = 0.25 * gravity_mod
        self.ship_lift = 0.4 * gravity_mod
        self.ship_max_speed = 5 + level_num  # Max snelheid ook omlaag

    def jump(self):
        # Alleen springen als we niet al aan het springen zijn
        if self.mode == 'cube' and not self.is_jumping:
            self.y_velocity = self.jump_force
            self.is_jumping = True
    
    def boost_jump(self):
        self.y_velocity = self.boost_force
        self.is_jumping = True

    def toggle_mode(self):
        if self.mode == 'cube':
            self.mode = 'ship'
            self.rect.y = HEIGHT / 2
            self.y_velocity = 0
            keys = pygame.key.get_pressed()
            self.is_holding_space = keys[pygame.K_SPACE]
        else:
            self.mode = 'cube'
            self.is_holding_space = False
            self.rect.y = HEIGHT - 100 - self.size

    def update(self):
        # Input checken (voor auto-jump en ship control)
        keys = pygame.key.get_pressed()
        
        if self.mode == 'cube':
            # --- NIEUW: AUTO-JUMP ---
            # Als spatie is ingedrukt EN we staan op de grond (niet springen), spring dan!
            if keys[pygame.K_SPACE] and not self.is_jumping:
                self.jump()

            self.y_velocity += self.gravity
            self.rect.y += self.y_velocity
            
            floor_limit = HEIGHT - 100
            if self.rect.bottom >= floor_limit:
                self.rect.bottom = floor_limit
                self.y_velocity = 0
                self.is_jumping = False
                
        elif self.mode == 'ship':
            # Update holding status voor main loop logica
            self.is_holding_space = keys[pygame.K_SPACE]
            
            if self.is_holding_space:
                self.y_velocity -= self.ship_lift
            else:
                self.y_velocity += self.ship_gravity
            
            # Snelheid begrenzen (zodat je niet te hard gaat)
            if self.y_velocity > self.ship_max_speed: self.y_velocity = self.ship_max_speed
            if self.y_velocity < -self.ship_max_speed: self.y_velocity = -self.ship_max_speed
            
            self.rect.y += self.y_velocity

    def check_death(self, current_ceiling, current_floor):
        if self.mode == 'ship':
            if self.rect.top <= current_ceiling + 5 or self.rect.bottom >= current_floor - 5:
                return True
        return False

    def draw(self, screen):
        color = BLUE if self.mode == 'cube' else PURPLE
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)