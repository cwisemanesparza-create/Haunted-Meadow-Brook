import pygame

class Collectible(pygame.sprite.Sprite):

    def __init__(self, pos, image, group):
        super().__init__(group)

        self.image = image
        self.rect = self.image.get_rect(center=pos)

    def collect(self):
        self.kill()