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

class UIElement(Sprite):
    #interface Element

    def __init__(self, center_position, text, font_size, bg_rgb):
    
    #center_position - tuple (x, y)
    #text - string of text to write
    #font_size - int
    #bg_rgb (background colour) - tuple (r, g, b)
    #text_rgb (text colour) - tuple (r, g, b)

    self.mouse_over = False

    #image
    default_image = create_surafce_with_text(
        text=text, font_size=font_size, text_rgb=text_rgb, bg_rgb=bg_rgb
    )
     # create the image that shows when mouse is over the element
        highlighted_image = create_surface_with_text(
            text=text, font_size=font_size * 1.2, text_rgb=text_rgb, bg_rgb=bg_rgb
        )

    # add both images and their rects to lists
        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

    # calls init method
        super().__init__()