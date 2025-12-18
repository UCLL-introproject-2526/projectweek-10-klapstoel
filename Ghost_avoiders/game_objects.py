import pygame
import random
from pathlib import Path  # <--- BELANGRIJK: Vergeet deze import niet!
from settings import *
from utils import laad_afbeelding 

# --- DE SPELER ---
class Speler(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 

        self.image = laad_afbeelding("Ghost avoiders/images/spaceship copy.png", 50, 50, (0, 0, 255))

        
        # Stap 2: Waar sta ik?
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

        # STAP 1: Maak een lijstje van al je spook-afbeeldingen
        # Let op: Zorg dat deze bestanden ook echt bestaan op je computer!
        mogelijke_plaatjes = [
            "/Users/arnedeboudt/Desktop/UCLL/introduction project/projectweek/projectweek-10-klapstoel/projectweek-10-klapstoel/space invaders/images/enemy-removebg-preview.png",
            "/Users/arnedeboudt/Desktop/UCLL/introduction project/projectweek/projectweek-10-klapstoel/projectweek-10-klapstoel/space invaders/images/enemy2-removebg-preview.png",
            "/Users/arnedeboudt/Desktop/UCLL/introduction project/projectweek/projectweek-10-klapstoel/projectweek-10-klapstoel/space invaders/images/enemy3-removebg-preview.png"
        ]
        
        gekozen_bestand = random.choice(mogelijke_bestanden)
        
        # Plak het pad aan elkaar
        FULL_PATH = IMAGE_DIR / gekozen_bestand

        self.image = laad_afbeelding(str(FULL_PATH), 50, 50, ROOD)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, BREEDTE - 50) 
        self.rect.y = -50 
        self.snelheid = snelheid

    def update(self):
        self.rect.y += self.snelheid