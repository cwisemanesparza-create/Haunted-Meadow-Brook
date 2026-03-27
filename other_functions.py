import pygame
import random, math
from random import randint

# Load Scaled function
def load_scaled(path, size):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, size)

# Random position function
def random_position(room_size, margin=100):
    x = random.randint(margin, room_size[0] - margin)
    y = random.randint(margin, room_size[1] - margin)
    return (x, y)
