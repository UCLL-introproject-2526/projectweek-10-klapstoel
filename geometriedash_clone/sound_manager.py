
import pygame
import math
import random

class SoundManager:
    def __init__(self):
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
            self.audio_enabled = True
        except:
            print("Geen audio mogelijk.")
            self.audio_enabled = False

        self.explosion_fx = self._generate_arcade_explosion()
        self.jump_fx = self._generate_jump_sound()
        self.win_fx = self._generate_win_sound()

    def play_jump(self):
        if self.audio_enabled and self.jump_fx: self.jump_fx.play()

    def play_crash(self):
        if self.audio_enabled and self.explosion_fx: self.explosion_fx.play()

    def play_win(self):
        if self.audio_enabled and self.win_fx: self.win_fx.play()

    def _generate_arcade_explosion(self):
        if not self.audio_enabled: return None
        try:
            sample_rate = 44100; duration_sec = 0.6
            total_samples = int(sample_rate * duration_sec)
            buffer = bytearray(); phase = 0.0
            for i in range(total_samples):
                t = i / total_samples
                frequency = max(20, 150.0 - (130.0 * t**0.5))
                phase += (2 * math.pi * frequency) / sample_rate
                sine = math.sin(phase)
                noise = random.uniform(-1, 1)
                mix = (sine * 0.8) + (noise * (0.8 * (1.0 - t)))
                vol = 1.0 - (t * t)
                val = int(128 + (mix * vol * 127))
                buffer.append(max(0, min(255, val)))
            s = pygame.mixer.Sound(buffer=buffer); s.set_volume(0.6)
            return s
        except: return None

    def _generate_jump_sound(self):
        if not self.audio_enabled: return None
        try:
            sample_rate = 44100; duration_sec = 0.35
            total_samples = int(sample_rate * duration_sec)
            buffer = bytearray(); phase = 0.0
            for i in range(total_samples):
                t = i / total_samples
                frequency = 80.0 + (140.0 * t)
                phase += (2 * math.pi * frequency) / sample_rate
                sine = math.sin(phase)
                vol = t * 10 if t < 0.1 else 1.0 - ((t - 0.1) / 0.9)**2
                val = int(128 + (sine * vol * 127))
                buffer.append(max(0, min(255, val)))
            s = pygame.mixer.Sound(buffer=buffer); s.set_volume(0.6)
            return s
        except: return None

    def _generate_win_sound(self):
        if not self.audio_enabled: return None
        try:
            sample_rate = 44100; duration_sec = 1.5
            total_samples = int(sample_rate * duration_sec)
            buffer = bytearray(); phase = 0.0
            notes = [261.63, 329.63, 392.00, 523.25]
            for i in range(total_samples):
                t = i / total_samples
                note_idx = int(i / (sample_rate * 0.15))
                if note_idx >= len(notes): note_idx = len(notes) - 1
                freq = notes[note_idx]
                phase += (2 * math.pi * freq) / sample_rate
                sine = 1.0 if math.sin(phase) > 0 else -1.0
                vol = 1.0 - (t**2)
                val = int(128 + (sine * vol * 60))
                buffer.append(max(0, min(255, val)))
            s = pygame.mixer.Sound(buffer=buffer); s.set_volume(0.7)
            return s
        except: return None