import pygame

class Camera(pygame.sprite.Group):

    def __init__(self, viewport_size):
        super().__init__()

        self.display_surface = pygame.display.get_surface()

        self.viewport_width, self.viewport_height = viewport_size
        self.offset = pygame.math.Vector2()
        