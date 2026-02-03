import pygame
import pygame.freetype 
from pygame.sprite import Sprite
from pygame.rect import Rect

BLACK = (0, 0, 0)
ORANGE = (255, 140, 0)

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    #returns surface with text
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()