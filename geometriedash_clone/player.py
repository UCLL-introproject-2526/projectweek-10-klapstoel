
import pygame
from settings import *

class Player:
    def __init__(self):
        self.size = 30
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
        self.ship_gravity = 0.5
        self.ship_lift = 0.8
        self.ship_max_speed = 8

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
        self.ship_gravity = 0.6 * gravity_mod
        self.ship_lift = 1.0 * gravity_mod
        self.ship_max_speed = 9 + (level_num * 1.5)

    def jump(self):
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
        if self.mode == 'cube':
            self.y_velocity += self.gravity
            self.rect.y += self.y_velocity
            
            floor_limit = HEIGHT - 100
            if self.rect.bottom >= floor_limit:
                self.rect.bottom = floor_limit
                self.y_velocity = 0
                self.is_jumping = False
                
        elif self.mode == 'ship':
            if self.is_holding_space:
                self.y_velocity -= self.ship_lift
            else:
                self.y_velocity += self.ship_gravity
            
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