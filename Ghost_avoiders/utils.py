# utils.py
import pygame
import os

def laad_afbeelding(naam, breedte, hoogte, kleur):
    
    # De computer plakt de map 'images' en de naam aan elkaar.
    pad = os.path.join('images', naam)
        # .convert_alpha() zorgt dat doorzichtige delen ook echt doorzichtig zijn
    plaatje = pygame.image.load(pad).convert_alpha()
        
        #  Juiste grootte
    plaatje = pygame.transform.scale(plaatje, (breedte, hoogte))
    return plaatje
        # Maak een nep-plaatje (een gekleurd blokje) zodat het spel niet crasht
def laad_highscore():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as bestand:
            return int(bestand.read())

def sla_highscore_op(nieuwe_score):
    with open("highscore.txt", "w") as bestand:
        bestand.write(str(nieuwe_score))

def teken_tekst(scherm, tekst, x, y, font, kleur=(255,255,255), gecentreerd=False):
    img = font.render(tekst, True, kleur)
    rect = img.get_rect()
    if gecentreerd:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    scherm.blit(img, rect)