import pygame
from global_variables_and_settings import SPEED

class Player(pygame.sprite.Sprite):

    def __init__(self, image, pos, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.speed = SPEED

        self.dead = False
        self.death_frame = 0
        self.death_finished = False

    def input(self):
        keys = pygame.key.get_pressed()

        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = -1
        if keys[pygame.K_d]:
            self.direction.x = 1
        if keys[pygame.K_w]:
            self.direction.y = -1
        if keys[pygame.K_s]:
            self.direction.y = 1

    def update(self):
        if self.dead:
            return

        self.input()
        self.rect.center += self.direction * self.speed

    def reset(self, pos):
        self.rect.center = pos
        self.dead = False
        self.death_frame = 0
        self.death_finished = False