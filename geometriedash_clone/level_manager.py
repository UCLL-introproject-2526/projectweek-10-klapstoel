
import pygame
import random
import math
from settings import *

class LevelManager:
    def __init__(self):
        self.objects = []
        self.score = 0
        self.scroll_speed = 0
        self.total_scroll_x = 0
        self.current_level_num = 1
        self.finish_spawned = False
        
        self.cur_ceiling_y = 100
        self.cur_floor_y = HEIGHT - 100
        
        self.ship_timer = 0
        self.exit_portal_spawned = False

    def reset(self, level_num):
        self.objects = []
        self.score = 0
        self.finish_spawned = False
        self.current_level_num = level_num
        self.scroll_speed = LEVEL_DATA[level_num]["speed"]
        self.total_scroll_x = 0
        self.cur_ceiling_y = 100
        self.cur_floor_y = HEIGHT - 100
    
        self.ship_timer = 0
        self.exit_portal_spawned = False

    def get_borders(self, mode):
        if mode == 'cube':
            return 100, HEIGHT - 100
        else:
            wave = math.sin(self.total_scroll_x * 0.003) * 100
            center_y = (HEIGHT / 2) + wave
            breath = math.sin(self.total_scroll_x * 0.002) 
            tunnel_height = 180 + (breath * 60) 
            
            ceil = center_y - (tunnel_height / 2)
            flr = center_y + (tunnel_height / 2)
            
            self.cur_ceiling_y = ceil
            self.cur_floor_y = flr
            
            return ceil, flr

    def get_safe_y(self):
        wave = math.sin(self.total_scroll_x * 0.003) * 100
        return (HEIGHT / 2) + wave

    def update(self):
        self.total_scroll_x += self.scroll_speed
        
        for obj in self.objects:
            obj['rect'].x -= self.scroll_speed
            if 'spike' in obj['type']: 
                obj['hitbox'].x = obj['rect'].x + 10
            else: 
                obj['hitbox'].x = obj['rect'].x
                
            if obj['rect'].right < 100 and not obj['passed']:
                if obj['type'] != 'finish_line':
                    self.score += 1
                obj['passed'] = True
                
        self.objects = [obj for obj in self.objects if obj['rect'].right > 0]

    def spawn_objects(self, mode):
        if self.finish_spawned: return
        
        if mode == 'ship':
            self.ship_timer += 1
            
            if self.total_scroll_x % 60 == 0 and self.score < WIN_SCORE:
                self.score += 1
            
            if self.ship_timer >= 180 and not self.exit_portal_spawned:
                if not self.objects: 
                    r = pygame.Rect(WIDTH, 0, 50, 100)
                    
                    safe_y = self.get_safe_y()
                    r.centery = safe_y
                    
                    self.objects.append({'rect': r, 'hitbox': r, 'type': 'fly_portal', 'passed': False})
                    self.exit_portal_spawned = True
            
            return 

        
        
        if self.ship_timer > 0:
            self.ship_timer = 0
            self.exit_portal_spawned = False

        last_x = self.objects[-1]['rect'].x if self.objects else 0
        
        if self.score >= WIN_SCORE and not self.finish_spawned:
            if WIDTH - last_x > 600:
                r = pygame.Rect(WIDTH, 0, 40, HEIGHT)
                self.objects.append({'rect': r, 'hitbox': r, 'type': 'finish_line', 'passed': False})
                self.finish_spawned = True
            return

        last_type = self.objects[-1]['type'] if self.objects else None
        min_g, max_g = LEVEL_DATA[self.current_level_num]["gap"]
        actual_gap = random.randint(min_g, max_g)
        
        if last_type == 'fly_portal': actual_gap += 400
        if last_type == 'double_spike_part1': actual_gap = 40

        if WIDTH - last_x > actual_gap or not self.objects:
            choices = ['spike', 'platform', 'double_spike']
            if self.current_level_num >= 2: choices = ['spike', 'double_spike', 'platform'] 

            
            choices.append('jumppad_combo') 
            choices.append('fly_portal')

            if 'fly_portal' in choices and random.random() < 0.7: 
                choices.remove('fly_portal')

            obj_type = random.choice(choices)
            
            
            final_type = obj_type
            if obj_type == 'double_spike':
                final_type = 'double_spike_part1'
                obj_type = 'spike'

            
            if obj_type == 'jumppad_combo':
                
                r_pad = pygame.Rect(WIDTH, HEIGHT - 100 - 10, 40, 10)
                self.objects.append({'rect': r_pad, 'hitbox': r_pad, 'type': 'jumppad', 'passed': False})
                
                
                r_spike = pygame.Rect(WIDTH + 250, HEIGHT - 100 - 40, 40, 40)
                hb_spike = pygame.Rect(WIDTH + 250 + 10, HEIGHT - 100 - 40 + 10, 20, 30)
                self.objects.append({'rect': r_spike, 'hitbox': hb_spike, 'type': 'spike', 'passed': False})
                return 

           
            new_obj = None
            w, h = 40, 40
            floor_y = HEIGHT - 100

            if obj_type == 'spike':
                r = pygame.Rect(WIDTH, floor_y - h, w, h)
                hb = pygame.Rect(WIDTH + 10, floor_y - h + 10, w - 20, h - 10)
                new_obj = {'rect': r, 'hitbox': hb, 'type': final_type if final_type == 'double_spike_part1' else 'spike', 'passed': False}
            elif obj_type == 'platform':
                elev = random.choice([80, 130])
                r = pygame.Rect(WIDTH, floor_y - elev, random.randint(100, 200), 20)
                new_obj = {'rect': r, 'hitbox': r, 'type': obj_type, 'passed': False}
            elif obj_type == 'fly_portal':
                r = pygame.Rect(WIDTH, HEIGHT/2 - 50, 50, 100)
                new_obj = {'rect': r, 'hitbox': r, 'type': obj_type, 'passed': False}

            if new_obj: self.objects.append(new_obj)

    def draw_background(self, screen, mode):
        screen.fill(BG_DARK)
        grid_size = 60
        bg_scroll = self.total_scroll_x * 0.5
        offset = int(bg_scroll % grid_size)
        
        for x in range(-offset, WIDTH, grid_size):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, HEIGHT), 1)
        for y in range(0, HEIGHT, grid_size):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (WIDTH, y), 1)
            
        ceil_y, flr_y = self.get_borders(mode)
        
        pygame.draw.rect(screen, WALL_COLOR, (0, flr_y, WIDTH, HEIGHT - flr_y))
        pygame.draw.line(screen, WHITE, (0, flr_y), (WIDTH, flr_y), 2)
        pygame.draw.rect(screen, WALL_COLOR, (0, 0, WIDTH, ceil_y))
        pygame.draw.line(screen, WHITE, (0, ceil_y), (WIDTH, ceil_y), 2)

    def draw_objects(self, screen):
        for obj in self.objects:
            t = obj['type']
            r = obj['rect']
            if 'spike' in t:
                pygame.draw.polygon(screen, RED, [(r.left, r.bottom), (r.right, r.bottom), (r.centerx, r.top)])
            elif t == 'platform': pygame.draw.rect(screen, GREEN, r)
            elif t == 'jumppad': pygame.draw.rect(screen, ORANGE, r)
            elif t == 'fly_portal': pygame.draw.rect(screen, PORTAL_COLOR, r, 8)
            elif t == 'finish_line':
                pygame.draw.rect(screen, WHITE, r)
                for cy in range(0, HEIGHT, 20):
                    if (cy // 20) % 2 == 0: pygame.draw.rect(screen, BLACK, (r.x, cy, r.width, 20))

    def draw_ui(self, screen, fonts):
        bar_width = 400; bar_height = 20
        x = (WIDTH - bar_width) // 2; y = 50
        percent = min(1.0, self.score / WIN_SCORE)
        pygame.draw.rect(screen, BLACK, (x, y, bar_width, bar_height))
        pygame.draw.rect(screen, WHITE, (x, y, bar_width, bar_height), 2)
        pygame.draw.rect(screen, GREEN, (x + 2, y + 2, int(bar_width * percent) - 4, bar_height - 4))
        txt = fonts['ui'].render(f"{int(percent * 100)}%", True, WHITE)
        screen.blit(txt, (x + bar_width + 10, y))
        score_txt = fonts['ui'].render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_txt, (20, 20))