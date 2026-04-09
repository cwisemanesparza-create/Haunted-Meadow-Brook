import pygame
from pygame.sprite import Sprite

# Collectible class
class Collectible(pygame.sprite.Sprite):
    def __init__(self, pos, image, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.collected = False

        # Create a glow effect
        glow_radius = max(self.rect.width, self.rect.height)
        glow_surf = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (255, 255, 0, 60), (glow_radius, glow_radius), glow_radius)
        glow_surf = pygame.transform.smoothscale(glow_surf, (glow_radius, glow_radius))
        self.glow = glow_surf
        self.glow_rect = self.glow.get_rect(center=self.rect.center)

    def collect(self):
        self.collected = True
        self.kill()     

    def draw(self, surface, offset):
        # Draw glow first
        self.glow_rect.center = self.rect.center - offset
        surface.blit(self.glow, self.glow_rect)
        # Draw actual collectible image
        surface.blit(self.image, self.rect.topleft - offset)
        