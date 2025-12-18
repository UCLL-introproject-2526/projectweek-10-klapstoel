# utils.py
import pygame
import os

def laad_afbeelding(bestandsnaam, breedte, hoogte, vervangende_kleur):
    """Probeert een afbeelding uit de map 'img' te laden."""
    pad = os.path.join('images', bestandsnaam)
    try:
        afbeelding = pygame.image.load(pad).convert_alpha()
        afbeelding = pygame.transform.scale(afbeelding, (breedte, hoogte))
        return afbeelding
    except (FileNotFoundError, pygame.error):
        print(f"LET OP: Kan {bestandsnaam} niet vinden. Er wordt een blokje gebruikt.")
        afbeelding = pygame.Surface((breedte, hoogte))
        afbeelding.fill(vervangende_kleur)
        return afbeelding

def laad_highscore():
    if os.path.exists("highscore.txt"):
        try:
            with open("highscore.txt", "r") as bestand:
                return int(bestand.read())
        except:
            return 0
    return 0

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