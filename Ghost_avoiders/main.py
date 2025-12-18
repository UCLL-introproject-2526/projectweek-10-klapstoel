import pygame
import sys
import random
from pathlib import Path
from settings import *
from utils import * # Let op: Kogel ook importeren!
from game_objects import Speler, Spook
from sounds_manager import SoundManager

# --- INITIALISATIE ---
pygame.init()
scherm = pygame.display.set_mode((BREEDTE, HOOGTE))
pygame.display.set_caption("Ghost Avoider")
klok = pygame.time.Clock()

geluid = SoundManager()

font_klein = pygame.font.Font(None, 36)
font_groot = pygame.font.Font(None, 72)

# Achtergrond laden
BASE_DIR = Path(__file__).resolve().parent
IMAGE_PATH = BASE_DIR / "images" / "background.png"
achtergrond = laad_afbeelding(str(IMAGE_PATH), BREEDTE, HOOGTE, ZWART)

def start_scherm(highscore):
    intro = True
    while intro:
        scherm.blit(achtergrond, (0,0))
        teken_tekst(scherm, "GHOST AVOIDER", BREEDTE//2, HOOGTE//2 - 50, font_groot, ROOD, True)
        teken_tekst(scherm, f"Highscore: {highscore}", BREEDTE//2, HOOGTE//2 + 20, font_klein, GEEL, True)
        teken_tekst(scherm, "Druk op SPATIE om te starten", BREEDTE//2, HOOGTE//2 + 80, font_klein, WIT, True)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    geluid.start_muziek()
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
                    geluid.start_muziek()
                    return 
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

def main():
    highscore = laad_highscore()
    
    while True: 
        start_scherm(highscore)
        
        speler = Speler()
        alle_sprites = pygame.sprite.Group() 
        alle_sprites.add(speler)
        
        spoken_groep = pygame.sprite.Group()
        kogels_groep = pygame.sprite.Group()
        
        score = 0
        huidige_spook_snelheid = BASIS_SPOOK_SNELHEID
        spook_timer = 0
        spel_actief = True
        
        # --- GAME LOOP ---
        while spel_actief:
            klok.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                
                # HIER IS DE SCHIET-KNOP WEER TERUG
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        # Maak een kogel
                        kogel = Kogel(speler.rect.centerx, speler.rect.top)
                        alle_sprites.add(kogel)
                        kogels_groep.add(kogel)

            # Spoken spawnen
            spook_timer += 1
            if spook_timer >= max(20, SPOOK_INTERVAL - (score // 2)):
                # --- HIER ZAT DE FOUT: ---
                # We maken eerst het spook...
                nieuw_spook = Spook(huidige_spook_snelheid)
                # ... en voegen hem DAN pas toe aan de groepen
                spoken_groep.add(nieuw_spook)
                alle_sprites.add(nieuw_spook)
                
                spook_timer = 0
            
            alle_sprites.update()
            
            # Kogel raakt Spook
            geraakte_spoken = pygame.sprite.groupcollide(spoken_groep, kogels_groep, True, True)
            for spook in geraakte_spoken:
                score += 1
                if score % 10 == 0: huidige_spook_snelheid += 0.5

            # Spook ontsnapt
            for spook in spoken_groep:
                if spook.rect.top > HOOGTE: 
                    score += 1
                    spook.kill() 
                    if score % 10 == 0: huidige_spook_snelheid += 0.5

            # Spook raakt Speler (DOOD)
            if pygame.sprite.spritecollide(speler, spoken_groep, False):
                geluid.stop_muziek()
                geluid.speel_game_over()
                spel_actief = False 
            
            # Tekenen
            scherm.blit(achtergrond, (0, 0))
            alle_sprites.draw(scherm) 
            teken_tekst(scherm, f"Score: {score}", 10, 10, font_klein)
            teken_tekst(scherm, f"Highscore: {highscore}", BREEDTE-200, 10, font_klein, GEEL)
            pygame.display.flip()
            
        if score > highscore:
            highscore = score
            sla_highscore_op(highscore)
            
        game_over_scherm(score, highscore)

if __name__ == "__main__":
    main()