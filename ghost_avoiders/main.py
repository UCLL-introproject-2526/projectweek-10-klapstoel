# main.py
import pygame
import sys
import random
from settings import *
from utils import * 
from game_objects import Speler, Spook 

# Initialisatie
pygame.init()
scherm = pygame.display.set_mode((BREEDTE, HOOGTE))
pygame.display.set_caption("Ghost Avoider")
klok = pygame.time.Clock()

# Fonts
font_klein = pygame.font.Font(None, 36)
font_groot = pygame.font.Font(None, 72)

# Achtergrond laden
achtergrond = laad_afbeelding("/Users/arnedeboudt/Desktop/UCLL/introduction project/projectweek/projectweek-10-klapstoel/projectweek-10-klapstoel/space invaders/images/background.png", BREEDTE, HOOGTE, ZWART)

def start_scherm(highscore):
    intro = True
    while intro:
        scherm.blit(achtergrond, (0,0))
        teken_tekst(scherm, "GHOST AVOIDER", BREEDTE//2, HOOGTE//2 - 50, font_groot, WIT, True)
        teken_tekst(scherm, f"Highscore: {highscore}", BREEDTE//2, HOOGTE//2 + 20, font_klein, GEEL, True)
        teken_tekst(scherm, "Druk op SPATIE om te starten", BREEDTE//2, HOOGTE//2 + 80, font_klein, WIT, True)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False

def game_over_scherm(score, highscore):
    while True:
        scherm.blit(achtergrond, (0,0))
        teken_tekst(scherm, "GAME OVER", BREEDTE//2, HOOGTE//2 - 50, font_groot, ROOD, True)
        teken_tekst(scherm, f"Score: {score}", BREEDTE//2, HOOGTE//2 + 20, font_klein, WIT, True)
        
        if score >= highscore and score > 0:
            teken_tekst(scherm, "NIEUWE HIGHSCORE!", BREEDTE//2, HOOGTE//2 + 60, font_klein, GEEL, True)
            
        teken_tekst(scherm, "Druk SPATIE voor restart", BREEDTE//2, HOOGTE//2 + 100, font_klein, GRIJS, True)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return # Terug naar de main loop
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

def main():
    highscore = laad_highscore()
    
    while True: # Grote loop voor herstarten spel
        start_scherm(highscore)
        
        # --- SPEL SETUP ---
        speler = Speler()
        alle_sprites = pygame.sprite.Group() # Groep voor makkelijk tekenen
        alle_sprites.add(speler)
        
        spoken_groep = pygame.sprite.Group() # Groep voor botsingen
        
        score = 0
        huidige_spook_snelheid = BASIS_SPOOK_SNELHEID
        spook_timer = 0
        spel_actief = True
        
        # --- GAMEPLAY LOOP ---
        while spel_actief:
            klok.tick(FPS)
            
            # 1. Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
            
            # 2. Update Logica
            spook_timer += 1
            if spook_timer >= max(20, SPOOK_INTERVAL - (score // 2)):
                spook = Spook(huidige_spook_snelheid)
                spoken_groep.add(spook)
                alle_sprites.add(spook)
                spook_timer = 0
            
            alle_sprites.update() # Beweegt speler én alle spoken automatisch!
            
            # Score checken (spoken die het scherm uit zijn)
            for spook in spoken_groep:
                if spook.rect.top > HOOGTE: 
                    score += 1
                    spook.kill() # Verwijder spook uit geheugen
                    
                    # Snelheid verhogen
                    if score % 10 == 0:
                        huidige_spook_snelheid += 0.5

            # Botsingen
            if pygame.sprite.spritecollide(speler, spoken_groep, False):
                spel_actief = False # Dood
            
            # 3. Tekenen
            scherm.blit(achtergrond, (0, 0))
            alle_sprites.draw(scherm) # Tekent alles in 1 keer!
            
            teken_tekst(scherm, f"Score: {score}", 10, 10, font_klein)
            teken_tekst(scherm, f"Highscore: {highscore}", BREEDTE-200, 10, font_klein, GEEL)
            
            pygame.display.flip()
            
        # --- EINDE SPEL ---
        if score > highscore:
            highscore = score
            sla_highscore_op(highscore)
            
        game_over_scherm(score, highscore)

if __name__ == "__main__":
    main()