import pygame

class FloatingText:

    def __init__(self, text, pos, color=(255,255,0), lifespan=60, rise_speed=1.5, font_size=24):

        self.text = text
        self.pos = pygame.math.Vector2(pos)
        self.color = color
        self.lifespan = lifespan
        self.rise_speed = rise_speed
        self.font = pygame.font.Font(None, font_size)

    def update(self):

        self.pos.y -= self.rise_speed
        self.lifespan -= 1

        return self.lifespan > 0

    def draw(self, surface):

        text_surf = self.font.render(self.text, True, self.color)

        rect = text_surf.get_rect(center=(self.pos.x, self.pos.y))

        surface.blit(text_surf, rect)