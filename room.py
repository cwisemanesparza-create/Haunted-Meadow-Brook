import pygame
import pygame.freetype
import random, math
import os
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from random import randint

from load_scaled import *
from global_variables import *

# Room class
class Room:
    def __init__(self, bg_path, size, doors=None, ghosts=None, collectibles=None, viewport=None, respawn_pos=None):
        self.bg_surf = load_scaled(bg_path, size)
        self.bg_rect = self.bg_surf.get_rect(topleft=(0, 0))
        self.size = size
        self.doors = doors or {}  # {door_name: {'rect': pygame.Rect, 'target_room': str, 'spawn_pos': (x, y)}}
        self.ghosts = ghosts or []
        self.collectibles = collectibles or []
        self.respawn_pos = respawn_pos # (x, y)
        
        # if the caller supplied a viewport, otherwise clamp to the maximum allowed
        if viewport is None:
            w = min(size[0], MAX_VIEWPORT_WIDTH)
            h = min(size[1], MAX_VIEWPORT_HEIGHT)
            viewport = (w, h)
        self.viewport = viewport         

    def get_door_at(self, player_rect):
        for door_name, info in self.doors.items():
            if player_rect.colliderect(info['rect']):
                return info  
        return None