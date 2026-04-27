import pygame
import pygame.freetype
import random, math
from pygame.sprite import Sprite
from pygame.rect import Rect
from random import randint

from global_variables import *

# Helper function
def create_surface_with_text(text, font_size, text_rgb, bg_rgb, padding=12):
    font = pygame.freetype.SysFont("music&text/BlackWitcher.otf", font_size, bold=True)
    text_surface, _ = font.render(text, fgcolor=text_rgb)

    width = text_surface.get_width() + padding * 2
    height = text_surface.get_height() + padding * 2

    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill(bg_rgb)
    surface.blit(text_surface, (padding, padding))
    return surface.convert_alpha()

# UI Button class
class UIElement(Sprite):
    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        super().__init__()
        self.action = action
        self.text = text
        self.font_size = font_size
        self.bg_rgb = bg_rgb
        self.text_rgb = text_rgb
        self.center_position = center_position
        self.render_text()
        self.mouse_over = False

        self.images = [
            create_surface_with_text(text, font_size, text_rgb, bg_rgb),
            create_surface_with_text(text, int(font_size * 1.15), text_rgb, bg_rgb)
        ]

        self.rects = [
            self.images[0].get_rect(center=center_position),
            self.images[1].get_rect(center=center_position)
        ]
        
    def render_text(self):
        self.images = [
            create_surface_with_text(self.text, self.font_size, self.text_rgb, self.bg_rgb),
            create_surface_with_text(self.text, int(self.font_size * 1.15), self.text_rgb, self.bg_rgb)
        ]
        self.rects = [img.get_rect(center=self.center_position) for img in self.images]
    
    def set_text(self, text):
        self.text = text
        self.render_text()

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
        
# Slider class
class Slider:
    def __init__(self, pos, size, label, value=0.5):
        self.x, self.y = pos
        self.width, self.height = size
        self.label = label
        self.value = value
        self.dragging = False
        self.track_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.knob_radius = self.height // 2 + 4

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.track_rect.collidepoint(event.pos):
            self.dragging = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        if event.type == pygame.MOUSEMOTION and self.dragging:
            rel_x = max(self.x, min(event.pos[0], self.x + self.width))
            self.value = (rel_x - self.x) / self.width

    def draw(self, screen):
        font = pygame.font.Font(None, 28)
        label_surf = font.render(self.label, True, WHITE)
        screen.blit(label_surf, (self.x, self.y - 30))
        pygame.draw.rect(screen, WHITE, self.track_rect, 2)
        knob_x = self.x + int(self.value * self.width)
        knob_y = self.y + self.height // 2
        pygame.draw.circle(screen, WHITE, (knob_x, knob_y), self.knob_radius)
        
# Floating Text class
class FloatingText:
    def __init__(self, text, pos, color=(255, 255, 0), lifespan=60, rise_speed=1.5, font_size=24):
        self.text = text
        self.pos = pygame.math.Vector2(pos)
        self.color = color
        self.lifespan = lifespan  # frames before disappearing
        self.rise_speed = rise_speed
        self.font = pygame.font.Font(None, font_size)

    def update(self):
        """Move the text upward and decrease lifespan."""
        self.pos.y -= self.rise_speed
        self.lifespan -= 1
        return self.lifespan > 0  # True if still alive

    def draw(self, surface):
        text_surf = self.font.render(self.text, True, self.color)
        rect = text_surf.get_rect(center=(self.pos.x, self.pos.y))
        surface.blit(text_surf, rect)
        

        