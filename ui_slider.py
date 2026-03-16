import pygame
from global_variables_and_settings import WHITE

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