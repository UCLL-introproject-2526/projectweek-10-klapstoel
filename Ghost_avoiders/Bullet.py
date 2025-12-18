import pygame
import sys
import random
from settings import *
from utils import * 
from game_objects import Speler, Spook
from bullets import Bullet, Explosie  # NIEUW!
from pathlib import Path


pygame.init()
scherm = pygame.display.set_mode((BREEDTE, HOOGTE))
pygame.display.set_caption("Ghost Avoider")
klok = pygame.time.Clock()

font_klein = pygame.font.Font(None, 36)
font_groot = pygame.font.Font(None, 72)

BASE_DIR = Path(__file__).resolve().parent
IMAGE_PATH = BASE_DIR / "images" / "background.png"
achtergrond = laad_afbeelding(IMAGE_PATH, BREEDTE, HOOGTE, ZWART)

def start_scherm(highscore):
    """Het start scherm van het spel"""
    intro = True
    while intro:
        scherm.blit(achtergrond, (0,0))
        teken_tekst(scherm, "GHOST AVOIDER", BREEDTE//2, HOOGTE//2 - 50, font_groot, WIT, True)
        teken_tekst(scherm, f"Highscore: {highscore}", BREEDTE//2, HOOGTE//2 + 20, font_klein, GEEL, True)
        teken_tekst(scherm, "Druk SPATIE om te starten", BREEDTE//2, HOOGTE//2 + 80, font_klein, WIT, True)
        teken_tekst(scherm, "Hou SPATIE ingedrukt om te schieten!", BREEDTE//2, HOOGTE//2 + 120, font_klein, GRIJS, True)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False

def game_over_scherm(score, highscore):
    """Het game over scherm"""
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
                    return

def main():
    highscore = laad_highscore()
    
    while True:
        start_scherm(highscore)
        
        speler = Speler()
        alle_sprites = pygame.sprite.Group()
        alle_sprites.add(speler)
        
        spoken_groep = pygame.sprite.Group()
        bullets_groep = pygame.sprite.Group()  
        explosies_groep = pygame.sprite.Group()  
        score = 0
        huidige_spook_snelheid = BASIS_SPOOK_SNELHEID
        spook_timer = 0
        spel_actief = True
        
     
        while spel_actief:
            klok.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
            
            toetsen = pygame.key.get_pressed()
            if toetsen[pygame.K_SPACE]:  
                if speler.kan_schieten():  
                   
                    bullet = Bullet(speler.rect.centerx, speler.rect.top)
                    bullets_groep.add(bullet)
                    alle_sprites.add(bullet)
                    speler.reset_cooldown()  
          
            spook_timer += 1
            if spook_timer >= max(20, SPOOK_INTERVAL - (score // 2)):
                spook = Spook(huidige_spook_snelheid)
                spoken_groep.add(spook)
                alle_sprites.add(spook)
                spook_timer = 0
            

            alle_sprites.update()
            explosies_groep.update()
            
            for bullet in bullets_groep:
                geraakt = pygame.sprite.spritecollide(bullet, spoken_groep, True)
                if geraakt:  
                    explosie = Explosie(bullet.rect.centerx, bullet.rect.centery)
                    explosies_groep.add(explosie)
                    alle_sprites.add(explosie)
                    
                    
                    bullet.kill()
                    
                    
                    score += 5
            
           
            for spook in spoken_groep:
                if spook.rect.top > HOOGTE: 
                    score += 1
                    spook.kill()
                    
                
                    if score % 10 == 0:
                        huidige_spook_snelheid += 0.5

            
            if pygame.sprite.spritecollide(speler, spoken_groep, False):
                spel_actief = False  
            
            
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