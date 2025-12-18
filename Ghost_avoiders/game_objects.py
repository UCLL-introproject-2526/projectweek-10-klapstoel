import pygame
import random
from pathlib import Path  
from settings import *
from utils import laad_afbeelding 

# --- DE SPELER ---
class Speler(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        
        # 1. Bepaal de map waar DIT bestand (game_objects.py) staat
        BASE_DIR = Path(__file__).resolve().parent
        
        # 2. Bouw het pad naar het plaatje
        # Let op: Zorg dat de mapnaam 'images' of 'img' klopt met jouw mappen!
        SPACESHIP_PATH = BASE_DIR / "images" / "spaceship copy.png"
        
        # 3. Laden
        # We zetten het pad om naar een string met str() voor de zekerheid
        self.image = laad_afbeelding(str(SPACESHIP_PATH), 60, 60, BLAUW)
        
        # 4. Hitbox maken
        self.rect = self.image.get_rect()
        self.rect.center = (BREEDTE // 2, HOOGTE - 50) 
        
    def update(self):
        toetsen = pygame.key.get_pressed()
        if toetsen[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= SPELER_SNELHEID
        if toetsen[pygame.K_RIGHT] and self.rect.right < BREEDTE:
            self.rect.x += SPELER_SNELHEID

# --- HET SPOOK ---
class Spook(pygame.sprite.Sprite):
    def __init__(self, snelheid):
        super().__init__() 
        
        BASE_DIR = Path(__file__).resolve().parent
        IMAGE_DIR = BASE_DIR / "images"

        # Lijst met bestandsnamen
        mogelijke_bestanden = [
            "enemy-removebg-preview.png",
            "enemy2-removebg-preview.png",
            "enemy3-removebg-preview.png"
        ]
        
        gekozen_bestand = random.choice(mogelijke_plaatjes)
        
        # Plak het pad aan elkaar

        self.image = laad_afbeelding(str(FULL_PATH), 50, 50, ROOD)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, BREEDTE - 50) 
        self.rect.y = -50 
        self.snelheid = snelheid

    def update(self):
        self.rect.y += self.snelheid