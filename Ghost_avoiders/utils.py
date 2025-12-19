# utils.py
import pygame
import os

def laad_afbeelding(pad, breedte, hoogte, kleur):
    try:
        # .convert_alpha() zorgt dat doorzichtige delen ook echt doorzichtig zijn
        plaatje = pygame.image.load(pad).convert_alpha()
        # Juiste grootte
        plaatje = pygame.transform.scale(plaatje, (breedte, hoogte))
        return plaatje
    except pygame.error as e:
        print(f"Fout: Kan afbeelding op {pad} niet laden. {e}")
        # Maak een tijdelijk gekleurd vlak als het plaatje ontbreekt
        oppervlak = pygame.Surface((breedte, hoogte))
        oppervlak.fill(kleur)
        return oppervlak
       
def laad_highscore():
    if os.path.exists("highscore.txt"):
        try:
            with open("highscore.txt", "r") as bestand:
                inhoud = bestand.read().strip()
                return int(inhoud) if inhoud else 0
        except ValueError:
            return 0
    return 0

def sla_highscore_op(nieuwe_score):
    with open("highscore.txt", "w") as bestand:
        bestand.write(str(nieuwe_score))

def teken_tekst(scherm, tekst, x, y, font, kleur=(255,255,255), gecentreerd=False):
    img = font.render(str(tekst), True, kleur)
    rect = img.get_rect()
    if gecentreerd:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    scherm.blit(img, rect)