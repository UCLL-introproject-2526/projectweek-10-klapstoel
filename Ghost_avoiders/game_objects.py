import pygame
import random
from pathlib import Path  
from settings import *
from utils import laad_afbeelding 

# --- DE SPELER ---
class Speler(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        
        BASE_DIR = Path(__file__).resolve().parent
        SPACESHIP_PATH = BASE_DIR / "images" / "spaceship copy.png"
        
        self.image = laad_afbeelding(str(SPACESHIP_PATH), 60, 60, BLAUW)
        self.rect = self.image.get_rect()
        self.rect.center = (BREEDTE // 2, HOOGTE - 60) 
        
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
        
        mogelijke_bestanden = [
            "enemy-removebg-preview.png",
            "enemy2-removebg-preview.png",
            "enemy3-removebg-preview.png"
        ]
        
        gekozen_bestand = random.choice(mogelijke_bestanden)
        FULL_PATH = IMAGE_DIR / gekozen_bestand
        
        self.image = laad_afbeelding(str(FULL_PATH), 50, 50, ROOD)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, BREEDTE - 50) 
        self.rect.y = -50 
        self.snelheid = snelheid

    def update(self):
        self.rect.y += self.snelheid
