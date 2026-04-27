import pygame
import random, math

from global_variables import *
from other_functions import *
from collectible import Collectible

class Cabinet:
    def __init__(self, pos, locked_image, opened_image):
        self.locked_image = locked_image
        self.opened_image = opened_image
        self.image = self.locked_image
        self.rect = self.image.get_rect(center=pos)
        self.unlocked = False
        self.opened = False

    def open(self):
        self.unlocked = True
        self.opened = True
        self.image = self.opened_image
        self.rect = self.image.get_rect(center=self.rect.center)

    def reset(self):
        # Not used on death retry. Cabinet progress persists for the full run.
        self.image = self.opened_image if self.opened else self.locked_image

    def draw(self, surface, offset):
        surface.blit(self.image, self.rect.topleft - offset)
        
def create_key_surface():
    surface = pygame.Surface((54, 32), pygame.SRCALPHA)
    gold = (245, 196, 45)
    dark_gold = (160, 110, 20)
    pygame.draw.circle(surface, gold, (15, 16), 11)
    pygame.draw.circle(surface, (0, 0, 0, 0), (15, 16), 5)
    pygame.draw.rect(surface, gold, pygame.Rect(24, 13, 24, 6))
    pygame.draw.rect(surface, dark_gold, pygame.Rect(38, 19, 5, 8))
    pygame.draw.rect(surface, dark_gold, pygame.Rect(46, 19, 5, 6))
    pygame.draw.circle(surface, dark_gold, (15, 16), 11, 2)
    return surface.convert_alpha()

def load_key_surface():
    try:
        image = pygame.image.load(KEY_IMAGE_PATH).convert_alpha()
        return pygame.transform.smoothscale(image, KEY_DRAW_SIZE)
    except (pygame.error, FileNotFoundError):
        return create_key_surface()

def create_vacuum_surface():
    surface = pygame.Surface((72, 38), pygame.SRCALPHA)
    blue = (42, 135, 220)
    blue_dark = (20, 66, 120)
    gray = (160, 170, 180)
    dark = (40, 45, 55)
    pygame.draw.rect(surface, gray, pygame.Rect(2, 16, 22, 6), border_radius=3)
    pygame.draw.polygon(surface, dark, [(0, 12), (16, 16), (16, 23), (0, 27)])
    pygame.draw.rect(surface, blue, pygame.Rect(22, 7, 34, 23), border_radius=7)
    pygame.draw.rect(surface, blue_dark, pygame.Rect(28, 3, 20, 7), border_radius=3)
    pygame.draw.circle(surface, dark, (32, 31), 5)
    pygame.draw.circle(surface, dark, (51, 31), 5)
    pygame.draw.line(surface, gray, (54, 9), (68, 2), 4)
    pygame.draw.circle(surface, (225, 235, 245), (42, 18), 5)
    return surface.convert_alpha()

def load_vacuum_surface():
    path = "photos/grizzly_photos/weapon and cabinet/vacuum.png"
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.smoothscale(image, VACUUM_DRAW_SIZE)
    except (pygame.error, FileNotFoundError):
        return pygame.transform.smoothscale(create_vacuum_surface(), VACUUM_DRAW_SIZE)

def load_locked_cabinet_surface():
    try:
        image = pygame.image.load(LOCKED_CABINET_IMAGE_PATH).convert_alpha()
        return pygame.transform.smoothscale(image, CABINET_DRAW_SIZE)
    except (pygame.error, FileNotFoundError):
        return create_cabinet_surface(False, False)

def load_empty_cabinet_surface():
    try:
        image = pygame.image.load(EMPTY_CABINET_IMAGE_PATH).convert_alpha()
        return pygame.transform.smoothscale(image, CABINET_DRAW_SIZE)
    except (pygame.error, FileNotFoundError):
        return create_cabinet_surface(True, True)

def load_opened_cabinet_surface():
    return load_empty_cabinet_surface()
    
def create_cabinet_surface(unlocked=False, opened=False):
    surface = pygame.Surface(CABINET_DRAW_SIZE, pygame.SRCALPHA)
    wood = (92, 55, 32)
    wood_light = (125, 78, 45)
    wood_dark = (45, 28, 20)
    pygame.draw.rect(surface, wood_dark, pygame.Rect(0, 0, 92, 122), border_radius=4)
    pygame.draw.rect(surface, wood, pygame.Rect(6, 6, 80, 110), border_radius=3)

    if opened:
        pygame.draw.rect(surface, (28, 25, 28), pygame.Rect(14, 14, 64, 94), border_radius=2)
        pygame.draw.rect(surface, wood_light, pygame.Rect(52, 10, 28, 102), border_radius=2)
        pygame.draw.circle(surface, (190, 190, 190), (58, 61), 3)
    else:
        pygame.draw.line(surface, wood_dark, (46, 8), (46, 114), 3)
        pygame.draw.circle(surface, (190, 190, 190), (38, 61), 3)
        pygame.draw.circle(surface, (190, 190, 190), (54, 61), 3)

    lock_color = (95, 210, 110) if unlocked else (225, 185, 45)
    pygame.draw.rect(surface, lock_color, pygame.Rect(36, 78, 20, 18), border_radius=3)
    pygame.draw.arc(surface, lock_color, pygame.Rect(39, 66, 14, 18), math.pi, 0, 3)
    return surface.convert_alpha()

def draw_vacuum(screen, player, offset, direction, vacuum_img):
    player_screen_x = player.rect.x - offset.x
    player_screen_y = player.rect.y - offset.y
    offset_x, offset_y = VACUUM_OFFSETS.get(direction, VACUUM_OFFSETS["forward"])

    if direction == "left":
        image = pygame.transform.flip(vacuum_img, True, False)
    else:
        image = vacuum_img

    pos = (player_screen_x + offset_x, player_screen_y + offset_y)
    screen.blit(image, pos)
    
def draw_prompt(screen, text):
    font = pygame.font.Font(None, 32)
    text_surface = font.render(text, True, (244, 232, 198))
    padding_x = 24
    padding_y = 12
    prompt_width = text_surface.get_width() + padding_x * 2
    prompt_height = text_surface.get_height() + padding_y * 2

    shadow_surface = pygame.Surface((prompt_width, prompt_height), pygame.SRCALPHA)
    shadow_surface.fill((8, 5, 4, 130))
    shadow_rect = shadow_surface.get_rect(center=(screen.get_width() // 2 + 4, screen.get_height() - 60))
    screen.blit(shadow_surface, shadow_rect)

    prompt_surface = pygame.Surface((prompt_width, prompt_height), pygame.SRCALPHA)
    prompt_surface.fill((31, 18, 14, 215))
    outer_rect = prompt_surface.get_rect()
    inner_rect = outer_rect.inflate(-8, -8)
    pygame.draw.rect(prompt_surface, (126, 78, 36, 230), outer_rect, 2, border_radius=6)
    pygame.draw.rect(prompt_surface, (196, 151, 72, 210), inner_rect, 1, border_radius=4)
    pygame.draw.line(prompt_surface, (88, 48, 28, 210), (12, prompt_height - 7), (prompt_width - 12, prompt_height - 7), 2)
    prompt_surface.blit(text_surface, (padding_x, padding_y))
    rect = prompt_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() - 64))
    screen.blit(prompt_surface, rect)
    
def get_nearby_capturable_ghost(player, ghosts, capture_radius=250):
    player_pos = pygame.math.Vector2(player.rect.center)
    nearby_ghosts = [
        ghost for ghost in ghosts
        if not ghost.capture_started
        and not ghost.captured
        and pygame.math.Vector2(ghost.rect.center).distance_to(player_pos) <= capture_radius
    ]
    if not nearby_ghosts:
        return None

    return min(
        nearby_ghosts,
        key=lambda ghost: pygame.math.Vector2(ghost.rect.center).distance_to(player_pos)
    )

def screen_pos_from_world(world_pos, camera_group):
    return pygame.math.Vector2(world_pos) - camera_group.offset