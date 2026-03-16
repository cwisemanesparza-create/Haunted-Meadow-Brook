import pygame

def load_scaled(path, size):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, size)
