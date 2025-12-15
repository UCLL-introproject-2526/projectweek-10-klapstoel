import pygame


# Initialize Pygame
pygame.init()

# Tuple representing width and height in pixels
screen_size = (1024, 768)
def create_main_surface():
    # 1. INITIALISATIE EN VENSTER CREATIE (Dit moet EENMALIG gebeuren!)
    import pygame
    pygame.init() # Pygame moet eerst opgestart worden
    
    # DEFINIEER DE GROOTTE
    screen_size = (800, 600) 
    
    # MAAK HET SCHERM AAN (UIT de loop!)
    screen = pygame.display.set_mode(screen_size) 
    
    # Optioneel: Stel FPS in
    clock = pygame.time.Clock()
    
    running = True
    while running:
        # Limit de snelheid (bijv. tot 60 frames per seconde)
        clock.tick(60) 

        # 1. EVENT HANDLING: Luister naar het besturingssysteem
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # De loop stopt
        
        # 2. GAME LOGIC: Beweeg objecten, bereken nieuwe posities
        # ...

        # 3. RENDERING: Teken alles opnieuw op het scherm
        screen.fill((255, 255, 255)) # Maak het scherm wit
        # ... Teken hier je objecten ...
        
        # ESSENTIEEL: Update het scherm om veranderingen zichtbaar te maken
        pygame.display.flip() 
        
    pygame.quit() # Sluit Pygame netjes af

# Roep de functie aan om het spel te starten
if __name__ == '__main__':
    create_main_surface()
pygame.quit() # Sluit Pygame netjes af
