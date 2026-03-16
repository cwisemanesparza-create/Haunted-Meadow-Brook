import pygame
class SoundManager:

    def __init__(self):

        pygame.mixer.init()

        self.master_volume = 0.8
        self.music_volume = 0.6

    def play_sound(self, sound):
        sound.set_volume(self.master_volume)
        sound.play()

    def play_music(self, path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1)