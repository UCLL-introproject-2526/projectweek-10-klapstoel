import pygame
import random
from utils import laad_afbeelding # Zorg dat dit klopt

# --- DE SPELER ---
class Speler(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
<<<<<<<<< Temporary merge branch 1:Ghost avoiders/game_objects.py
        self.image = laad_afbeelding("/Users/Ibrah/projectweek-10-klapstoel/Ghost avoiders/images/spaceship copy.png", 60, 60, (0, 0, 255))
=========
        self.image = laad_afbeelding("Ghost avoiders/images/spaceship copy.png", 50, 50, (0, 0, 255))
>>>>>>>>> Temporary merge branch 2:Ghost_avoiders/game_objects.py
        
        # Stap 2: Waar sta ik?
        self.rect = self.image.get_rect()
        self.rect.center = (400, 550) # Midden onderin
        
    def update(self):
        # Stap 3: Hoe beweeg ik?
        toetsen = pygame.key.get_pressed()
        if toetsen[pygame.K_LEFT]:
            self.rect.x -= 7
        if toetsen[pygame.K_RIGHT]:
            self.rect.x += 7

# --- HET SPOOK (MET VARIATIE) ---
class Spook(pygame.sprite.Sprite):
    def __init__(self, snelheid):
        super().__init__() 

        # STAP 1: Maak een lijstje van al je spook-afbeeldingen
        # Let op: Zorg dat deze bestanden ook echt bestaan op je computer!
        mogelijke_plaatjes = [
            "/Users/projectweek-10-klapstoel/Ghost avoiders/images/enemy-removebg-preview.png",
            "/Users/projectweek-10-klapstoel/Ghost avoiders/images/enemy2-removebg-preview.png",
            "/Users/projectweek-10-klapstoel/Ghost avoiders/images/enemy3-removebg-preview.png"
        ]
        
        # STAP 2: Kies willekeurig één plaatje uit de lijst
        gekozen_plaatje = random.choice(mogelijke_plaatjes)

        # STAP 3: Laad dat gekozen plaatje
        # (Als hij het plaatje niet vindt, wordt het een rood blokje)
        self.image = laad_afbeelding(gekozen_plaatje, 50, 50, (255, 0, 0))

        # STAP 4: De rest is hetzelfde als eerst
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 750) 
        self.rect.y = -50 
        self.snelheid = snelheid

    def update(self):
        # Alleen bewegen!
        self.rect.y += self.snelheid