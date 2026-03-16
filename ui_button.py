import pygame
import pygame.freetype
from pygame.sprite import Sprite

def create_surface_with_text(text, font_size, text_rgb, bg_rgb, padding=12):
    font = pygame.freetype.SysFont("music&text/BlackWitcher.otf", font_size, bold=True)
    text_surface, _ = font.render(text, fgcolor=text_rgb)

    width = text_surface.get_width() + padding * 2
    height = text_surface.get_height() + padding * 2

    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill(bg_rgb)
    surface.blit(text_surface, (padding, padding))
    return surface.convert_alpha()


class UIElement(Sprite):

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):

        super().__init__()

        self.action = action
        self.mouse_over = False

        self.images = [
            create_surface_with_text(text, font_size, text_rgb, bg_rgb),
            create_surface_with_text(text, int(font_size * 1.15), text_rgb, bg_rgb)
        ]

        self.rects = [
            self.images[0].get_rect(center=center_position),
            self.images[1].get_rect(center=center_position)
        ]

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up=False):

        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up and self.action:
                return self.action
        else:
            self.mouse_over = False

        return None

    def draw(self, surface):
        surface.blit(self.image, self.rect)