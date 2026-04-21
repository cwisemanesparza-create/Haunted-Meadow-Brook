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
        self.original_image = image
        self.rect = self.image.get_rect(center=start_pos)

        self.room_rect = room_rect
        self.home_pos = pygame.math.Vector2(start_pos)
        self.start_pos = pygame.math.Vector2(start_pos)

        self.wander_speed = 2
        self.chase_speed = 4
        self.return_speed = 3

        self.chase_radius = 250
        self.stop_radius = 35
        self.home_radius = 10

        self.state = "wander"

        self.direction = pygame.math.Vector2(random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)]))
        self.timer = random.randint(400, 1200)

        self.captured = False
        self.capture_started = False
        self.capture_timer = 0
        self.capture_duration = 350
        self.capture_target = None

    def start_capture(self, player):
        if self.capture_started or self.captured:
            return

        self.capture_started = True
        self.capture_timer = 0
        self.capture_target = player
        self.state = "capturing"

    def update_capture(self, dt):
        if not self.capture_started or self.captured:
            return

        self.capture_timer += dt
        progress = min(1, self.capture_timer / self.capture_duration)

        if self.capture_target is not None:
            ghost_pos = pygame.math.Vector2(self.rect.center)
            player_pos = pygame.math.Vector2(self.capture_target.rect.center)
            pull = player_pos - ghost_pos
            if pull.length() > 0:
                ghost_pos += pull * min(0.35, progress + 0.08)

            scale = max(0.1, 1 - progress)
            width = max(1, int(self.original_image.get_width() * scale))
            height = max(1, int(self.original_image.get_height() * scale))
            self.image = pygame.transform.smoothscale(self.original_image, (width, height))
            self.rect = self.image.get_rect(center=(round(ghost_pos.x), round(ghost_pos.y)))

        if self.capture_timer >= self.capture_duration:
            self.captured = True

    def update(self, *args):
        if len(args) >= 2:
            dt, player = args[:2]
        else:
            return

        if self.capture_started:
            self.update_capture(dt)
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
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(round(self.start_pos.x), round(self.start_pos.y)))
        self.state = "wander"
        self.timer = random.randint(400,1200)
        self.captured = False
        self.capture_started = False
        self.capture_timer = 0
        self.capture_target = None
