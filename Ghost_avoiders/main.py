import pygame
import sys
import random
from pathlib import Path
from settings import *
from utils import * 
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

# --- AFBEELDINGEN LADEN ---
BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "images"

# Laad de normale achtergrond voor tijdens het spelen
IMAGE_PATH = IMAGE_DIR / "background.png"
achtergrond = laad_afbeelding(str(IMAGE_PATH), BREEDTE, HOOGTE, ZWART)

# Laad de poster voor het startscherm
POSTER_PATH = IMAGE_DIR / "poster.png" 
poster_afbeelding = laad_afbeelding(str(POSTER_PATH), BREEDTE, HOOGTE, ZWART)

def start_scherm(highscore):
    intro = True
    while intro:
        # Toon de poster op het startscherm
        scherm.blit(poster_afbeelding, (0, 0))
        
        # De titel staat al op de poster, dus we tonen alleen de highscore en instructie
        # Deze plaatsen we onderaan zodat ze de poster niet blokkeren
        teken_tekst(scherm, f"Highscore: {highscore}", BREEDTE//2, HOOGTE - 100, font_klein, FELGEEL, True)
        teken_tekst(scherm, "Druk op SPATIE om te starten", BREEDTE//2, HOOGTE - 50, font_klein, ROOD, True)
        
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
        # Gebruik de poster ook als achtergrond voor game over of de normale? 
        # Hier gebruiken we de normale achtergrond voor duidelijkheid
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
    startscherm = True
    while startscherm: 
        # Toon eerst het startscherm met de poster
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
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        # Schieten
                        from game_objects import Kogel # Import Kogel hier als het nodig is
                        kogel = Kogel(speler.rect.centerx, speler.rect.top)
                        alle_sprites.add(kogel)
                        kogels_groep.add(kogel)

            # Spoken spawnen
            spook_timer += 1
            if spook_timer >= max(20, SPOOK_INTERVAL - (score // 2)):
                nieuw_spook = Spook(huidige_spook_snelheid)
                spoken_groep.add(nieuw_spook)
                alle_sprites.add(nieuw_spook)
                spook_timer = 0
            
            alle_sprites.update()
            
            # Botsingen
            geraakte_spoken = pygame.sprite.groupcollide(spoken_groep, kogels_groep, True, True)
            for spook in geraakte_spoken:
                score += 1
                if score % 10 == 0: huidige_spook_snelheid += 0.5

            for spook in spoken_groep:
                if spook.rect.top > HOOGTE: 
                    score += 1
                    spook.kill() 
                    if score % 10 == 0: huidige_spook_snelheid += 0.5

            if pygame.sprite.spritecollide(speler, spoken_groep, False):
                geluid.stop_muziek()
                geluid.speel_game_over()
                spel_actief = False 
            
            # Tekenen: Gebruik de normale achtergrond tijdens het spel
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