import pygame
from image_loading import load_scaled
from global_variables_and_settings import MAX_VIEWPORT_WIDTH, MAX_VIEWPORT_HEIGHT

class Room:

    def __init__(self, bg_path, size, doors=None, ghosts=None, collectibles=None, viewport=None, respawn_pos=None):

        self.bg_surf = load_scaled(bg_path, size)
        self.bg_rect = self.bg_surf.get_rect(topleft=(0,0))

        self.size = size

        self.doors = doors or {}
        self.ghosts = ghosts or []
        self.collectibles = collectibles or []

        self.respawn_pos = respawn_pos

        if viewport is None:

            w = min(size[0], MAX_VIEWPORT_WIDTH)
            h = min(size[1], MAX_VIEWPORT_HEIGHT)

            viewport = (w,h)

        self.viewport = viewport

    def get_door_at(self, player_rect):

        for door_name, info in self.doors.items():

            if player_rect.colliderect(info["rect"]):
                return info

        return None