import pygame
import sys
import random

# ==========================================
# MODULE 1: CONFIGURATIE & SETTINGS
# ==========================================
# Hier passen we de "regels" van het spel aan.
# Als je de snelheid wilt veranderen, hoef je alleen hier te zijn.
class Settings:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    BG_COLOR = (30, 30, 30) # Donkergrijs
    
    # Speler settings
    PLAYER_SPEED = 5
    PLAYER_COLOR = (0, 255, 0) # Groen
    
    # Kogel settings
    BULLET_SPEED = 7
    BULLET_COLOR = (255, 255, 0) # Geel
    MAX_BULLETS = 3 # Max aantal kogels tegelijk op scherm
    
    # Vijand settings
    ENEMY_BG_COLOR = (255, 0, 0) # Rood
    ENEMY_SPEED_X = 2
    ENEMY_DROP_SPEED = 10 # Hoeveel ze zakken als ze de rand raken
    ENEMY_ROWS = 4
    ENEMY_COLS = 8

settings = Settings()

# ==========================================
# MODULE 2: DE KOGEL (BULLET)
# ==========================================
# Een simpele klasse die alleen maar omhoog of omlaag beweegt.
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        # Maak een simpele rechthoek als kogel
        self.image = pygame.Surface((5, 15))
        self.image.fill(settings.BULLET_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        
        # direction is -1 voor omhoog (speler), 1 voor omlaag (vijand)
        self.speed_y = settings.BULLET_SPEED * direction

    def update(self):
        # Beweeg de kogel
        self.rect.y += self.speed_y
        # Verwijder de kogel als hij buiten beeld is om geheugen te besparen
        if self.rect.bottom < 0 or self.rect.top > settings.SCREEN_HEIGHT:
            self.kill()

# ==========================================
# MODULE 3: DE SPELER (PLAYER)
# ==========================================
# Handelt input en positie van het ruimteschip af.
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Maak een simpel ruimteschip (een blokje)
        self.image = pygame.Surface((60, 20))
        self.image.fill(settings.PLAYER_COLOR)
        self.rect = self.image.get_rect()
        # Startpositie: midden onderin
        self.rect.midbottom = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 20)
        self.speed = settings.PLAYER_SPEED
        self.bullets_group = pygame.sprite.Group()

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < settings.SCREEN_WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        # Schiet alleen als we het maximum nog niet bereikt hebben
        if len(self.bullets_group) < settings.MAX_BULLETS:
            new_bullet = Bullet(self.rect.centerx, self.rect.top, -1)
            self.bullets_group.add(new_bullet)

    def update(self):
        self.get_input()
        self.bullets_group.update()

# ==========================================
# MODULE 4: DE VIJAND (ENEMY)
# ==========================================
# Een enkele alien.
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(settings.ENEMY_BG_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self, speed_x):
        self.rect.x += speed_x

# ==========================================
# MODULE 5: GAME MANAGER
# ==========================================
# Dit is de 'controller'. Het beheert de logica die de modules verbindt.
class GameManager:
    def __init__(self):
        # Sprite groepen voor efficiënt beheer
        self.player_group = pygame.sprite.GroupSingle()
        self.player = Player()
        self.player_group.add(self.player)
        
        self.enemy_group = pygame.sprite.Group()
        self.setup_enemies()
        self.enemy_direction = 1 # 1 = rechts, -1 = links

        self.game_over = False
        self.score = 0
        self.font = pygame.font.Font(None, 36)

    def setup_enemies(self):
        # Creëer een grid van vijanden
        start_x = 50
        start_y = 50
        gap_x = 60
        gap_y = 50
        for row in range(settings.ENEMY_ROWS):
            for col in range(settings.ENEMY_COLS):
                x = start_x + (col * gap_x)
                y = start_y + (row * gap_y)
                enemy = Enemy(x, y)
                self.enemy_group.add(enemy)

    def _check_enemy_movements(self):
        # Controleer of een vijand de rand raakt
        move_down = False
        for enemy in self.enemy_group.sprites():
            if enemy.rect.right >= settings.SCREEN_WIDTH or enemy.rect.left <= 0:
                move_down = True
                break
        
        if move_down:
            # Verander richting en ga een stapje omlaag
            self.enemy_direction *= -1
            for enemy in self.enemy_group.sprites():
                enemy.rect.y += settings.ENEMY_DROP_SPEED

    def _check_collisions(self):
        # Botsing: Speler kogel raakt Vijand
        # groupcollide checkt twee groepen tegen elkaar. True, True betekent dat beide verdwijnen bij een botsing.
        hits = pygame.sprite.groupcollide(self.player.bullets_group, self.enemy_group, True, True)
        if hits:
            for hit in hits:
                self.score += 10
        
        # Botsing: Vijand raakt speler (Game Over)
        if pygame.sprite.spritecollideany(self.player, self.enemy_group):
            self.game_over = True

        # Check of vijanden de bodem raken (Game Over)
        for enemy in self.enemy_group.sprites():
             if enemy.rect.bottom >= settings.SCREEN_HEIGHT:
                 self.game_over = True
                 
        # Check of alle vijanden op zijn (Gewonnen - voor nu ook game over status)
        if not self.enemy_group:
            # Hier zou je een nieuw level kunnen starten
            self.game_over = True


    def run_game_frame(self, screen):
        if not self.game_over:
            # 1. Updates
            self.player_group.update()
            self._check_enemy_movements()
            self.enemy_group.update(settings.ENEMY_SPEED_X * self.enemy_direction)
            self._check_collisions()

            # 2. Tekenen (Drawing)
            # Teken speler en zijn kogels
            self.player_group.draw(screen)
            self.player.bullets_group.draw(screen)
            # Teken vijanden
            self.enemy_group.draw(screen)
            
            # Teken score
            score_surf = self.font.render(f'Score: {self.score}', True, (255,255,255))
            screen.blit(score_surf, (10,10))

        else:
            # Game over scherm
            game_over_surf = self.font.render('GAME OVER - Druk op R om te herstarten', True, (255,255,255))
            game_over_rect = game_over_surf.get_rect(center=(settings.SCREEN_WIDTH/2, settings.SCREEN_HEIGHT/2))
            screen.blit(game_over_surf, game_over_rect)


# ==========================================
# MODULE 6: MAIN ENTRY POINT
# ==========================================
# Zet het scherm op en start de loop.
def main():
    pygame.init()
    screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    pygame.display.set_caption("Modulaire Space Invaders")
    clock = pygame.time.Clock()

    game_manager = GameManager()

    while True:
        # Event Handling (Input die niet direct beweging is, zoals afsluiten of schieten)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_manager.game_over:
                    game_manager.player.shoot()
                if event.key == pygame.K_r and game_manager.game_over:
                     # Reset de game
                     game_manager = GameManager()

        # Achtergrond vullen
        screen.fill(settings.BG_COLOR)
        
        # Draai de game logica voor dit frame
        game_manager.run_game_frame(screen)

        # Scherm verversen en snelheid limiteren
        pygame.display.flip()
        clock.tick(60) # Max 60 FPS

if __name__ == "__main__":
    main()