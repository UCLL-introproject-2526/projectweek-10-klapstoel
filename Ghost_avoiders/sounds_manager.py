import pygame
import os

class SoundManager:
    def __init__(self):
        # 1. Start de mixer (de geluidsmotor van Pygame)
        pygame.mixer.init()
        
        # 2. Bepaal waar de map 'sounds' is (relatief aan dit bestand)
        base_path = os.path.dirname(__file__)
        self.sound_folder = os.path.join(base_path, 'sounds')
        
        # 3. Variabelen klaarzetten
        self.game_over_sound = None
        
        # 4. Probeer alles direct te laden
        self.laad_bestanden()

    def laad_bestanden(self):
        # Achtergrondmuziek laden
        mp3_pad = os.path.join(self.sound_folder, 'background.mp3')
        pygame.mixer.music.load(mp3_pad)
        pygame.mixer.music.set_volume(0.5) # 50% volume
       

        # Game Over geluid laden
        wav_pad = os.path.join(self.sound_folder, 'game_over.mp3')
        
        self.game_over_sound = pygame.mixer.Sound(wav_pad)
        self.game_over_sound.set_volume(0.8)
        
    def start_muziek(self):
        """Start de achtergrondmuziek als die nog niet speelt."""

        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1) # -1 = oneindig herhalen

    def stop_muziek(self):
        """Stopt de muziek direct."""
        pygame.mixer.music.stop()

    def speel_game_over(self):
        """Speelt het dood-geluidje."""
        if self.game_over_sound:
            self.game_over_sound.play()