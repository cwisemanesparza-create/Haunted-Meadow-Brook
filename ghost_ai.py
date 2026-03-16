import pygame
import random

class Ghost(pygame.sprite.Sprite):

    def __init__(self, start_pos, room_rect, image, group):
        super().__init__(group)

        self.image = image
        self.rect = self.image.get_rect(center=start_pos)

        self.room_rect = room_rect
        self.home_pos = pygame.math.Vector2(start_pos)

        self.wander_speed = 2
        self.chase_speed = 4
        self.return_speed = 3

        self.chase_radius = 250
        self.stop_radius = 35

        self.state = "wander"

    def update(self, dt, player):

        ghost_pos = pygame.math.Vector2(self.rect.center)
        player_pos = pygame.math.Vector2(player.rect.center)

        distance = ghost_pos.distance_to(player_pos)

        if distance < self.chase_radius:
            self.state = "chase"

        if self.state == "chase":

            if distance < self.stop_radius:
                player.dead = True
                return

            direction = player_pos - ghost_pos

            if direction.length() > 0:
                direction = direction.normalize()

            move = direction * self.chase_speed

            self.rect.centerx += move.x
            self.rect.centery += move.y