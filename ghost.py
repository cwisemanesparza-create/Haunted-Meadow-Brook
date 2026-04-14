import pygame
import random, math
from pygame.sprite import Sprite
from pygame.rect import Rect
from random import randint

# Ghost AI class
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
        self.home_radius = 10

        self.state = "wander"

        self.direction = pygame.math.Vector2(random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)]))
        self.timer = random.randint(400, 1200)

    def update(self, *args):
        if len(args) >= 2:
            dt, player = args[:2]
        else:
            return
        
        ghost_pos = pygame.math.Vector2(self.rect.center)
        player_pos = pygame.math.Vector2(player.rect.center)

        distance_to_player = ghost_pos.distance_to(player_pos)
        distance_to_home = ghost_pos.distance_to(self.home_pos)

        # Chase mode
        if self.state != "return" and distance_to_player <= self.chase_radius:
            self.state = "chase"

        # Wander mode
        if self.state == "wander":
            self.timer -= dt

            if self.timer <= 0:
                self.direction = pygame.math.Vector2(
                    random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
                )
                self.timer = random.randint(400, 1200)

            move = self.direction * self.wander_speed
            next_rect = self.rect.move(move.x, move.y)

            if self.room_rect.contains(next_rect):
                self.rect = next_rect
            else:
                self.timer = 0

        # Chase mode
        elif self.state == "chase":
            # if ghost catches player, switch to return mode
            if distance_to_player <= self.stop_radius:
                player.dead = True
                return

            direction = player_pos - ghost_pos
            if direction.length() > 0:
                direction = direction.normalize()

            move = direction * self.chase_speed
            self.rect.centerx += move.x
            self.rect.centery += move.y

            # if player escapes far enough, ghost returns home
            if distance_to_player > self.chase_radius * 1.5:
                self.state = "return"

        # Return mode
        elif self.state == "return":
            direction = self.home_pos - ghost_pos

            if direction.length() > 0:
                direction = direction.normalize()

            move = direction * self.return_speed
            self.rect.centerx += move.x
            self.rect.centery += move.y

            # once back home, start wandering again
            if distance_to_home <= self.home_radius:
                self.rect.center = (round(self.home_pos.x), round(self.home_pos.y))
                self.state = "wander"
                self.timer = random.randint(400, 1200)
    def reset(self):
        self.rect.center = (round(self.home_pos.x), round(self.home_pos.y))
        self.state = "wander"
        self.timer = random.randint(400,1200)