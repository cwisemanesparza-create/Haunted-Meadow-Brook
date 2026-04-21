import pygame
import random, math
from pygame.sprite import Sprite
from pygame.rect import Rect

from global_variables import *
from collectible import *

# Camera class
class Camera(pygame.sprite.Group):
    def __init__(self, viewport_size):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.keyboard_speed = SPEED 
        self.set_viewport(*viewport_size)
        
    def set_viewport(self, width, height):
        self.viewport_width = width
        self.viewport_height = height
        self.half_w = width // 2
        self.half_h = height // 2
        
        # box setup
        self.camera_borders = {"left": 0, "right": width/2, "top": 0, "bottom": height/2}
        l = self.camera_borders["left"]
        t = self.camera_borders["top"]
        w = width - (self.camera_borders["left"] + self.camera_borders["right"])
        h = height - (self.camera_borders["top"] + self.camera_borders["bottom"])
        self.camera_rect = pygame.Rect(l, t, w, h)
        
        # zoom 
        self.zoom_scale = 1
        self.internal_surf_size = (width, height)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center = (self.half_w,self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h
        
        # camera offset 
        self.offset = pygame.math.Vector2()
        
    def box_target_camera(self, target, room_size):
        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
            
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
            
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
            
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders["left"]
        self.offset.y = self.camera_rect.top - self.camera_borders["top"]

        # Clamp to room bounds using current viewport dimensions
        self.offset.x = max(0, min(self.offset.x, room_size[0] - self.viewport_width))
        self.offset.y = max(0, min(self.offset.y, room_size[1] - self.viewport_height))
        
    def keyboard_control(self, room_size):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: 
            self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_d]: 
            self.camera_rect.x += self.keyboard_speed
        if keys[pygame.K_w]: 
            self.camera_rect.y -= self.keyboard_speed
        if keys[pygame.K_s]: 
            self.camera_rect.y += self.keyboard_speed

        self.offset.x = self.camera_rect.left - self.camera_borders["left"]
        self.offset.y = self.camera_rect.top - self.camera_borders["top"]
        
        # Clamp to room bounds using viewport size
        self.offset.x = max(0, min(self.offset.x, room_size[0] - self.viewport_width))
        self.offset.y = max(0, min(self.offset.y, room_size[1] - self.viewport_height))
        
    def custom_draw(self, player, room):
        self.box_target_camera(player, room.size)
        self.keyboard_control(room.size)
        
        self.offset.x = max(0, min(self.offset.x, room.size[0] - self.viewport_width))
        self.offset.y = max(0, min(self.offset.y, room.size[1] - self.viewport_height))
        
        # Clear internal_surf (no fill with black)
        self.internal_surf.fill((0, 0, 0, 0))  # Transparent fill instead
        
        # Draw room background to internal_surf
        self.internal_surf.blit(room.bg_surf, (0, 0), (self.offset.x, self.offset.y, self.viewport_width, self.viewport_height))
        
        # Draw player, ghosts, and collectibles to internal_surf
        all_sprites = [player] + room.ghosts + room.collectibles
        for sprite in sorted(all_sprites, key=lambda s: s.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            if isinstance(sprite, Collectible):
                self.internal_surf.blit(sprite.image, offset_pos)
                sprite.draw(self.internal_surf, self.offset)
            else:
                self.internal_surf.blit(sprite.image, offset_pos)

        scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center=(self.half_w, self.half_h))

        self.display_surface.blit(scaled_surf, (0, 0), scaled_rect)
        
        
