# main.py
import pygame
import sys
from settings import *
from sound_manager import SoundManager
from player import Player
from level_manager import LevelManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Geometry Dash - Safe Portal Fix")
        self.clock = pygame.time.Clock()
        
        self.sound_manager = SoundManager()
        self.player = Player()
        self.level_manager = LevelManager()
        
        self.fonts = {
            'title': pygame.font.SysFont('Arial', 50, bold=True),
            'menu': pygame.font.SysFont('Arial', 36),
            'ui': pygame.font.SysFont('Arial', 24)
        }
        
        self.state = "MENU"
        self.current_level = 1

    def start_level(self, level_num):
        self.current_level = level_num
        self.level_manager.reset(level_num)
        self.player.reset(LEVEL_DATA[level_num]["grav_mod"], level_num)
        self.state = "PLAYING"

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.state == "MENU":
                    if event.key == pygame.K_1: self.start_level(1)
                    if event.key == pygame.K_2: self.start_level(2)
                    if event.key == pygame.K_3: self.start_level(3)
                
                elif self.state == "PLAYING":
                    if event.key == pygame.K_SPACE:
                        if self.player.mode == 'cube': self.player.jump()
                        elif self.player.mode == 'ship': self.player.is_holding_space = True
                
                elif self.state in ["GAMEOVER", "VICTORY"]:
                    if event.key == pygame.K_r: self.start_level(self.current_level)
                    if event.key == pygame.K_m: self.state = "MENU"
            
            if event.type == pygame.KEYUP:
                if self.state == "PLAYING" and event.key == pygame.K_SPACE:
                    self.player.is_holding_space = False
        return True

    def check_collisions(self):
        player_rect = self.player.rect
        for obj in self.level_manager.objects:
            if player_rect.colliderect(obj['hitbox']):
                t = obj['type']
                
                if t == 'finish_line':
                    self.state = "VICTORY"
                    self.sound_manager.play_win()
                
                elif 'spike' in t:
                    self.state = "GAMEOVER"
                    self.sound_manager.play_crash()
                
                elif t == 'jumppad' and self.player.mode == 'cube':
                    self.player.boost_jump()
                    self.sound_manager.play_jump()
                
                elif t == 'fly_portal':
                    self.player.toggle_mode()
                    
                    # --- DE FIX IS HIER ---
                    if self.player.mode == 'ship':
                        # 1. Verwijder obstakels zodat je nergens tegenaan knalt
                        self.level_manager.objects.clear()
                        
                        # 2. Vraag aan LevelManager: Waar is het veilige midden NU?
                        safe_y = self.level_manager.get_safe_y()
                        
                        # 3. Zet de speler precies daar neer
                        self.player.rect.centery = safe_y
                        
                        # 4. Stop verticale snelheid voor een stabiele start
                        self.player.y_velocity = 0
                    
                    if obj in self.level_manager.objects:
                         self.level_manager.objects.remove(obj)
                    return
                
                elif t == 'platform':
                    if self.player.mode == 'cube':
                        if self.player.y_velocity >= 0 and player_rect.bottom < obj['rect'].top + 30:
                            self.player.rect.y = obj['rect'].top - self.player.size
                            self.player.y_velocity = 0
                            self.player.is_jumping = False
                        elif player_rect.top > obj['rect'].top:
                            self.state = "GAMEOVER"
                            self.sound_manager.play_crash()

    def update(self):
        if self.state == "PLAYING":
            self.player.update()
            
            # Check tunnel dood
            ceil, flr = self.level_manager.get_borders(self.player.mode)
            if self.player.check_death(ceil, flr):
                self.state = "GAMEOVER"
                self.sound_manager.play_crash()
                
            self.level_manager.update()
            self.level_manager.spawn_objects(self.player.mode)
            self.check_collisions()

    def draw(self):
        if self.state == "MENU":
            self.level_manager.draw_background(self.screen, 'cube')
            title = self.fonts['title'].render("GEOMETRY DASH CLONE", True, BLUE)
            self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
            
            t1 = self.fonts['menu'].render("[1] Level 1 - Easy", True, GREEN)
            t2 = self.fonts['menu'].render("[2] Level 2 - HARDCORE", True, YELLOW)
            t3 = self.fonts['menu'].render("[3] Level 3 - IMPOSSIBLE", True, RED)
            
            self.screen.blit(t1, (WIDTH//2 - t1.get_width()//2, 280))
            self.screen.blit(t2, (WIDTH//2 - t2.get_width()//2, 340))
            self.screen.blit(t3, (WIDTH//2 - t3.get_width()//2, 400))

        elif self.state == "PLAYING" or self.state == "GAMEOVER" or self.state == "VICTORY":
            self.level_manager.draw_background(self.screen, self.player.mode)
            
            self.player.draw(self.screen)
            self.level_manager.draw_objects(self.screen)
            self.level_manager.draw_ui(self.screen, self.fonts)
            
            if self.state == "GAMEOVER":
                txt = self.fonts['title'].render("GAME OVER", True, RED)
                self.screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 50))
                instr = self.fonts['ui'].render("[R] Restart  |  [M] Menu", True, WHITE)
                self.screen.blit(instr, (WIDTH//2 - instr.get_width()//2, HEIGHT//2 + 50))
                
            elif self.state == "VICTORY":
                txt = self.fonts['title'].render("LEVEL COMPLETE!", True, GREEN)
                self.screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - 50))
                instr = self.fonts['ui'].render("[R] Play Again  |  [M] Menu", True, BLUE)
                self.screen.blit(instr, (WIDTH//2 - instr.get_width()//2, HEIGHT//2 + 50))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()