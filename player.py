import pygame
import pygame.freetype
import random, math
import os
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from random import randint

from global_variables import *

# Player movement variables
walk_offset = 0
walk_timer = 0
current_direction = "forward"
current_frame = 0
frame_timer = 0

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect(center = pos)
        self.direction = pygame.math.Vector2()
        
        self.speed = SPEED
        self.extra_hits = 0
        self.slow_aura = False
        
        self.can_dash = False
        self.dash_speed = 25
        self.dash_cooldown = 0
        
        self.dead = False
        self.death_frame = 0
        self.death_frame_timer = 0
        self.death_finished = False
        
        self.spawn_protection = 1000   # milliseconds (1 second)
        self.spawn_timer = 0
        
        self.has_key = False
        self.has_vacuum = False
        
    def input(self):
        keys = pygame.key.get_pressed()
        
        self.direction.x = 0
        self.direction.y = 0
        
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
            
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y = 1
            
        # Dash
        if self.can_dash and keys[pygame.K_LSHIFT] and self.dash_cooldown <= 0:
            self.rect.center += self.direction * self.dash_speed
            self.dash_cooldown = 30
    
    def update(self, *args):
        if (self.dead):
            return
        
        if self.dash_cooldown > 0:
            self.dash_cooldown -= 1
            
        self.input()
        self.rect.center += self.direction * self.speed
        
    def reset(self, pos):
        self.rect.center = pos
        self.dead = False
        self.death_frame = 0
        self.death_frame_timer = 0
        self.death_finished = False
        # Run persistence: inventory stays with the player after death/retry.
        
# Animation images function
def animation_images(load_scaled):
    
    animations = {
        "forward": [
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_forward.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_forward_left_foot.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_forward.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_forward_right_foot.png", PLAYER_SIZE),
        ],
        "back": [
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_back.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_back_left_foot.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_back.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_back_right_foot.png", PLAYER_SIZE),
        ],
        "left": [
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_left.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_left_left_foot.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_left.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_left_right_foot.png", PLAYER_SIZE),
        ],
        "right": [
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_right.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_right_left_foot.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_right.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_right_right_foot.png", PLAYER_SIZE),
        ],
    }
    
    return animations