import pygame
import pygame.freetype
import random, math
import os
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from random import randint

from other_functions import *
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
    
# Enter Room function
def enter_room(player, pause_button, camera_group, target_room, spawn_pos):
    
    current_room = target_room
    player.rect.center = spawn_pos
    
    # push the player out of any door they happen to land in
    for info in target_room.doors.values():
        if player.rect.colliderect(info['rect']):
            player.rect.bottom = info['rect'].top - 1   # for example
    
    viewport_width, viewport_height = current_room.viewport
    screen = pygame.display.set_mode((viewport_width, viewport_height))
    pause_button.rects[0].center = (viewport_width - 60, 40)
    pause_button.rects[1].center = (viewport_width - 60, 40)
    
    camera_group.set_viewport(viewport_width, viewport_height)
    
    # Clamp camera to the new room, centred on the player
    camera_group.camera_rect.x = max(0, min(player.rect.centerx - viewport_width // 2, current_room.size[0] - viewport_width))
    camera_group.camera_rect.y = max(0, min(player.rect.centery - viewport_height // 2, current_room.size[1] - viewport_height))
    camera_group.offset.x = camera_group.camera_rect.x - camera_group.camera_borders["left"]
    camera_group.offset.y = camera_group.camera_rect.y - camera_group.camera_borders["top"]
    
    return current_room
    
    