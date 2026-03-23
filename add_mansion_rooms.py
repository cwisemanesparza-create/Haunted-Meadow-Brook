import pygame
import pygame.freetype
import random, math
import os
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from random import randint

# Menu Width, Height, Size
MENU_WIDTH = 1500
MENU_HEIGHT = 670
MENU_SIZE = (MENU_WIDTH, MENU_HEIGHT)

# Viewport Width, Height, Size
MAX_VIEWPORT_WIDTH = 1500
MAX_VIEWPORT_HEIGHT = 850
MAX_VIEWPORT_SIZE = (MAX_VIEWPORT_WIDTH, MAX_VIEWPORT_HEIGHT)

# Player and Ghost size
PLAYER_SIZE = (150, 190)
GHOST_SIZE = (80, 100)

# Colors
CLEAR = (0, 0, 0, 0) # transparent
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)


# Global volume values
MASTER_VOLUME = 0.8
MUSIC_VOLUME = 0.6

# Player movement
SPEED = 6
walk_offset = 0
walk_timer = 0
BOB_DELAY = 120
BOB_AMOUNT = 3
current_direction = "forward"
current_frame = 0
frame_timer = 0
FRAME_DELAY = 110

# Death Animation timers
FRAME_DELAY = 110
DEATH_FRAME_DELAY = 300

# Achievements data, change to true when unlocked 
achievements_data = [
    {
        "title": "Speed Runner",
        "description": "Finish the game in 10min.",
        "unlocked": False,
        "image_path": "photos/achievements/Ac1.png"
    },
    {
        "title": "Treasure Hunter",
        "description": "Find 10 Party supplies.",
        "unlocked": False,
        "image_path": "photos/achievements/Ac2.png"
    },
    {
        "title": "Upgrade Maniac",
        "description": "Pick 10 upgrades.",
        "unlocked": False,
        "image_path": "photos/achievements/Ac3.png"
    },
    {
        "title": "Explorer",
        "description": "Visit all rooms in the mansion.",
        "unlocked": False,
        "image_path": "photos/achievements/Ac6.png"
    },
    {
        "title": "First Capture",
        "description": "Capture your first ghost.",
        "unlocked": False,
        "image_path": "photos/achievements/Ac5.png"
    },
     {
        "title": "Party Time",
        "description": "Beat the game.",
        "unlocked": False,
        "image_path": "photos/achievements/Ac4.png"
    },
     {
        "title": "Let's get the Party Started",
        "description": "Open the game.",
        "unlocked": True,
        "image_path": "photos/achievements/Ac7.png"
    }
]

# Helper function
def create_surface_with_text(text, font_size, text_rgb, bg_rgb, padding=12):
    font = pygame.freetype.SysFont("music&text/BlackWitcher.otf", font_size, bold=True)
    text_surface, _ = font.render(text, fgcolor=text_rgb)

    width = text_surface.get_width() + padding * 2
    height = text_surface.get_height() + padding * 2

    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill(bg_rgb)
    surface.blit(text_surface, (padding, padding))
    return surface.convert_alpha()

# UI Button class
class UIElement(Sprite):
    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        super().__init__()
        self.action = action
        self.mouse_over = False

        self.images = [
            create_surface_with_text(text, font_size, text_rgb, bg_rgb),
            create_surface_with_text(text, int(font_size * 1.15), text_rgb, bg_rgb)
        ]

        self.rects = [
            self.images[0].get_rect(center=center_position),
            self.images[1].get_rect(center=center_position)
        ]

    @property
    def image(self):
        return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos, mouse_up=False):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
            if mouse_up and self.action:
                return self.action
        else:
            self.mouse_over = False
        return None

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
# Slider class
class Slider:
    def __init__(self, pos, size, label, value=0.5):
        self.x, self.y = pos
        self.width, self.height = size
        self.label = label
        self.value = value
        self.dragging = False
        self.track_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.knob_radius = self.height // 2 + 4

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.track_rect.collidepoint(event.pos):
            self.dragging = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        if event.type == pygame.MOUSEMOTION and self.dragging:
            rel_x = max(self.x, min(event.pos[0], self.x + self.width))
            self.value = (rel_x - self.x) / self.width

    def draw(self, screen):
        font = pygame.font.Font(None, 28)
        label_surf = font.render(self.label, True, WHITE)
        screen.blit(label_surf, (self.x, self.y - 30))
        pygame.draw.rect(screen, WHITE, self.track_rect, 2)
        knob_x = self.x + int(self.value * self.width)
        knob_y = self.y + self.height // 2
        pygame.draw.circle(screen, WHITE, (knob_x, knob_y), self.knob_radius)
        
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
        
# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, image, pos, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect(center = pos)
        self.direction = pygame.math.Vector2()
        self.speed = SPEED
        
        self.dead = False
        self.death_frame = 0
        self.death_frame_timer = 0
        self.death_finished = False
        
        self.spawn_protection = 1000   # milliseconds (1 second)
        self.spawn_timer = 0
        
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
    
    def update(self, *args):
        if (self.dead):
            return
        self.input()
        self.rect.center += self.direction * self.speed
    def reset(self, pos):
        self.rect.center = pos
        self.dead = False
        self.death_frame = 0
        self.death_frame_timer = 0
        self.death_finished = False
  
# Ghost AI (Wandering and Chase)
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
        
class Collectible(pygame.sprite.Sprite):
    def __init__(self, pos, image, group):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.collected = False

        # Create a glow effect
        glow_radius = max(self.rect.width, self.rect.height)
        glow_surf = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (255, 255, 0, 60), (glow_radius, glow_radius), glow_radius)
        glow_surf = pygame.transform.smoothscale(glow_surf, (glow_radius, glow_radius))
        self.glow = glow_surf
        self.glow_rect = self.glow.get_rect(center=self.rect.center)

    def collect(self):
        self.collected = True
        self.kill()     

    def draw(self, surface, offset):
        # Draw glow first
        self.glow_rect.center = self.rect.center - offset
        surface.blit(self.glow, self.glow_rect)
        # Draw actual collectible image
        surface.blit(self.image, self.rect.topleft - offset)
        
class FloatingText:
    def __init__(self, text, pos, color=(255, 255, 0), lifespan=60, rise_speed=1.5, font_size=24):
        self.text = text
        self.pos = pygame.math.Vector2(pos)
        self.color = color
        self.lifespan = lifespan  # frames before disappearing
        self.rise_speed = rise_speed
        self.font = pygame.font.Font(None, font_size)

    def update(self):
        """Move the text upward and decrease lifespan."""
        self.pos.y -= self.rise_speed
        self.lifespan -= 1
        return self.lifespan > 0  # True if still alive

    def draw(self, surface):
        text_surf = self.font.render(self.text, True, self.color)
        rect = text_surf.get_rect(center=(self.pos.x, self.pos.y))
        surface.blit(text_surf, rect)

# Game states
class GameState(Enum):
    MENU = 0
    START = 1
    SETTINGS = 2
    ACHIEVEMENTS = 3
    ABOUT = 4
    QUIT = -1

# Settings screen
def settings(screen, width, height, game_state):
    try:
        background_img = pygame.image.load("photos/background.png").convert()
        background_img = pygame.transform.scale(background_img, screen.get_size())
    except Exception as e:
        print(f"Error loading background.png: {e}")
        background_img = pygame.Surface(screen.get_size())
        background_img.fill(ORANGE)
    
    global MASTER_VOLUME, MUSIC_VOLUME
    clock = pygame.time.Clock()

    header_font = pygame.font.Font(None, 36)
    header_surface = header_font.render("AUDIO SETTINGS", True, WHITE)
    header_rect = pygame.Rect(width/2 - 200, height/2 - 230, 400, 60)

    master_slider = Slider((width/2 - 150, height/2 - 95), (300, 8), "Master Volume", MASTER_VOLUME)
    music_slider = Slider((width/2 - 150, height/2 - 35), (300, 8), "Music Volume", MUSIC_VOLUME / MASTER_VOLUME if MASTER_VOLUME>0 else 0)

    back_btn = UIElement((width/2, height/2 + 70), "Back", 28, BLACK, WHITE, game_state)

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return GameState.QUIT
            master_slider.handle_event(event)
            music_slider.handle_event(event)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
                
        # Draw screen
        screen.blit(background_img, (0, 0))
        pygame.draw.rect(screen, BLACK, header_rect)
        screen.blit(header_surface, header_surface.get_rect(center=header_rect.center))
        master_slider.draw(screen)
        music_slider.draw(screen)
        
        action = back_btn.update(pygame.mouse.get_pos(), mouse_up)
        back_btn.draw(screen)
            
        if action == game_state:
            if game_state == GameState.START:
                screen.fill(ORANGE) # background color when return to pause screen
                return game_state
            else:
                return game_state
        
        # Update volume in real time
        MASTER_VOLUME = master_slider.value
        MUSIC_VOLUME = music_slider.value * MASTER_VOLUME
        pygame.mixer.music.set_volume(MUSIC_VOLUME)

        pygame.display.flip()
        clock.tick(60)
        
# Load Achievement Images function
def load_achievement_images():
    global achievements_data
    ach_width, ach_height = 120, 120  # match your grid size

    for ach in achievements_data:
        if "image_path" in ach:
            try:
                surf = pygame.image.load(ach["image_path"]).convert_alpha()
                surf = pygame.transform.scale(surf, (ach_width, ach_height))
                ach["surf"] = surf
            except Exception as e:
                print(f"Failed to load {ach['title']} image: {e}")
                # fallback gray placeholder
                surf = pygame.Surface((ach_width, ach_height))
                surf.fill((100, 100, 100))
                ach["surf"] = surf

# Achievements screen
def achievements(screen):
    global achievements_data
    clock = pygame.time.Clock()

    # Load background
    try:
        bg_img = pygame.image.load("photos/background.png").convert()
        bg_img = pygame.transform.scale(bg_img, screen.get_size())
    except Exception as e:
        print(f"Error loading achievements background: {e}")
        bg_img = pygame.Surface(screen.get_size())
        bg_img.fill(BLACK)

    header_font = pygame.font.Font(None, 36)
    header_surface = header_font.render("ACHIEVEMENTS", True, WHITE)
    header_rect = pygame.Rect(0, 45, screen.get_width(), 60)

    back_btn = UIElement((screen.get_width() // 2, screen.get_height() - 80), "Back", 28, BLACK, WHITE, GameState.MENU)

    font_title = pygame.font.Font(None, 22)
    font_desc = pygame.font.Font(None, 20)

    # Tooltip function
    def draw_tooltip(screen, text, pos, font):
        try:
            max_width = 250
            words = text.split(' ')
            lines = []
            line = ''
            for word in words:
                test_line = line + ' ' + word if line else word
                if font.size(test_line)[0] > max_width:
                    lines.append(line)
                    line = word
                else:
                    line = test_line
            lines.append(line)

            padding = 8
            tip_width = max(font.size(line)[0] for line in lines) + padding * 2
            tip_height = len(lines) * font.get_height() + padding * 2
            tooltip_box = pygame.Surface((tip_width, tip_height), pygame.SRCALPHA)
            tooltip_box.fill((30, 30, 30, 220))

            for i, line in enumerate(lines):
                tooltip_box.blit(font.render(line, True, WHITE), (padding, padding + i * font.get_height()))

            tip_x = min(pos[0] + 20, screen.get_width() - tip_width)
            tip_y = min(pos[1] + 20, screen.get_height() - tip_height)
            screen.blit(tooltip_box, (tip_x, tip_y))
        except Exception as e:
            print(f"Tooltip render error: {e}")

    while True:
        mouse_up = False
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        # Draw background + overlay
        screen.blit(bg_img, (0, 0))
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, WHITE, header_rect, 2)
        screen.blit(header_surface, header_surface.get_rect(center=header_rect.center))

        # Grid settings
        padding = 50
        ach_width = 120
        ach_height = 120
        columns = 3
        rows = (len(achievements_data) + columns - 1) // columns

        total_grid_width = columns * ach_width + (columns - 1) * padding
        start_x = (screen.get_width() - total_grid_width) // 2
        start_y = 120

        hovered_desc = None
        tooltip_pos = (0, 0)

        for i, ach in enumerate(achievements_data):
            col = i % columns
            row = i // columns
            x = start_x + col * (ach_width + padding)
            y = start_y + row * (ach_height + 80)

            # Safe blit
            try:
                surf = ach.get("surf")
                if not surf:
                    surf = pygame.Surface((ach_width, ach_height))
                    surf.fill((100, 100, 100))  # Placeholder grey
                screen.blit(surf, (x, y))
            except Exception as e:
                print(f"Error drawing achievement {ach.get('title')}: {e}")
                continue

            # Grey overlay if locked
            if not ach.get("unlocked", False):
                overlay = pygame.Surface((ach_width, ach_height), pygame.SRCALPHA)
                overlay.fill((50, 50, 50, 180))
                screen.blit(overlay, (x, y))

            # Title
            title_surf = font_title.render(str(ach.get("title", "Unknown")), True, WHITE)
            title_rect = title_surf.get_rect(center=(x + ach_width // 2, y + ach_height + 15))
            screen.blit(title_surf, title_rect)

            # Hover tooltip
            img_rect = pygame.Rect(x, y, ach_width, ach_height)
            if img_rect.collidepoint(mouse_pos):
                hovered_desc = str(ach.get("description", "No description"))
                tooltip_pos = mouse_pos

        if hovered_desc:
            draw_tooltip(screen, hovered_desc, tooltip_pos, font_desc)

        action = back_btn.update(mouse_pos, mouse_up)
        back_btn.draw(screen)
        if action == GameState.MENU:
            return GameState.MENU

        pygame.display.flip()
        clock.tick(60)
        
# About screen
def about(screen):
    try:
        background_img = pygame.image.load("photos/background.png").convert()
        background_img = pygame.transform.scale(background_img, screen.get_size())
    except Exception as e:
        print(f"Error loading background.png: {e}")
        background_img = pygame.Surface(screen.get_size())
        background_img.fill(ORANGE)

    clock = pygame.time.Clock()

    header_font = pygame.font.Font(None, 36)
    header_surface = header_font.render("About Haunted Meadow Brook", True, WHITE)
    header_rect = pygame.Rect(200, 50, 400, 60)

    back_btn = UIElement((400, 500), "Back", 28, BLACK, WHITE, GameState.MENU)

    # About text content
    about_text = (
        "Haunted Meadow Brook is a thrilling adventure game set in a mysterious mansion. "
        "Explore every room, avoid ghosts, uncover secrets, and collect achievements. "
        "Each area of the mansion holds challenges and surprises for brave players. "
        "Immerse yourself in the eerie atmosphere and enjoy the unique soundtrack."
    )

    # Text box settings
    text_box_rect = pygame.Rect(150, 150, screen.get_width() - 300, screen.get_height() - 250)
    text_color = WHITE
    font = pygame.font.Font(None, 50)
    padding = 10

    # Pre-render wrapped text to a surface
    def render_text_surface(text, font, color, max_width):
        words = text.split(' ')
        lines = []
        line = ''
        for word in words:
            test_line = line + ' ' + word if line else word
            if font.size(test_line)[0] > max_width - padding * 2:
                lines.append(line)
                line = word
            else:
                line = test_line
        lines.append(line)

        text_height = len(lines) * (font.get_height() + 9)
        surf = pygame.Surface((max_width, text_height), pygame.SRCALPHA)
        surf.fill(CLEAR)  # transparent

        y_offset = 0
        for line in lines:
            line_surf = font.render(line, True, color)
            surf.blit(line_surf, (padding, y_offset))
            y_offset += font.get_height() + 2
        return surf

    text_surf = render_text_surface(about_text, font, text_color, text_box_rect.width)

    scroll_y = 0
    scroll_speed = 20
    max_scroll = max(0, text_surf.get_height() - text_box_rect.height)

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            # Scroll with mouse wheel
            if event.type == pygame.MOUSEWHEEL:
                scroll_y -= event.y * scroll_speed
                scroll_y = max(0, min(scroll_y, max_scroll))

        screen.blit(background_img, (0, 0))
        pygame.draw.rect(screen, BLACK, header_rect)
        screen.blit(header_surface, header_surface.get_rect(center=header_rect.center))

        # Draw text box background
        box_surf = pygame.Surface((text_box_rect.width, text_box_rect.height), pygame.SRCALPHA)
        box_surf.fill((0, 0, 0, 180))  # semi-transparent
        screen.blit(box_surf, text_box_rect.topleft)

        # Draw the visible portion of the text surface
        screen.blit(text_surf, (text_box_rect.x, text_box_rect.y), area=pygame.Rect(0, scroll_y, text_box_rect.width, text_box_rect.height))

        action = back_btn.update(pygame.mouse.get_pos(), mouse_up)
        back_btn.draw(screen)
        if action == GameState.MENU:
            return GameState.MENU

        pygame.display.flip()
        clock.tick(60)
                
        # Draw screen
        screen.blit(background_img, (0, 0))
        pygame.draw.rect(screen, BLACK, header_rect)
        screen.blit(header_surface, header_surface.get_rect(center=header_rect.center))
        
        action = back_btn.update(pygame.mouse.get_pos(), mouse_up)
        back_btn.draw(screen)
        if action == GameState.MENU:
            return GameState.MENU

# Load Scaled function
def load_scaled(path, size):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, size)

# Main function
def main():
    global MASTER_VOLUME, MUSIC_VOLUME
    global animations, door_sound

    pygame.init()
    pygame.mixer.init()
    
    door_sound = pygame.mixer.Sound("Sounds/door1.mp3")
    door_sound.set_volume(random.uniform(0.3, 0.6))
    
    screen = pygame.display.set_mode((MENU_SIZE))
    pygame.display.set_caption("Haunted Meadow Brook")

    # Load background music safely
    music_file = ("music&text/spooky_theme.mp3")
    if os.path.isfile(music_file):
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(-1)
    else:
        print(f"Warning: {music_file} not found. Music disabled.")

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
    
    # Death Screen Animantion frames
    
    death_frames = []
    for i in range (1, 12):
        frame = load_scaled(f"photos/grizz_death/grizz death cutscene/bear jump scare animation{i}.png",
                            screen.get_size())
        death_frames.append(frame)
        animations["death"] = death_frames
    
    state = GameState.MENU

    while True:
        if state == GameState.MENU:
            state = menu(screen)
        elif state == GameState.START:
            state = play_level(screen)
        elif state == GameState.SETTINGS:
            # settings screen adjusts to current screen size
            state = settings(screen, MENU_WIDTH, MENU_HEIGHT, game_state = GameState.MENU)
        elif state == GameState.ACHIEVEMENTS:
            load_achievement_images() # <-- load images first
            state = achievements(screen)
        elif state == GameState.ABOUT:
            state = about(screen)
        elif state == GameState.QUIT:
            pygame.quit()
            return

def menu(screen):
    screen = pygame.display.set_mode(MENU_SIZE)
    
    # Load menu background
    try:
        menu_background_img = pygame.image.load("photos/screen.png").convert()
        menu_background_img = pygame.transform.scale(menu_background_img, MENU_SIZE)
    except Exception as e:
        print(f"Error loading screen.png: {e}")
        menu_background_img = pygame.Surface(MENU_SIZE)
        menu_background_img.fill(ORANGE)
    
    # Menu buttons
    buttons = [
        UIElement((MENU_WIDTH/2, 300), "Start", 30, BLACK, WHITE, GameState.START),
        UIElement((MENU_WIDTH/2, 360), "Settings", 26, BLACK, WHITE, GameState.SETTINGS),
        UIElement((MENU_WIDTH/2, 420), "Achievements", 26, BLACK, WHITE, GameState.ACHIEVEMENTS),
        UIElement((MENU_WIDTH/2, 480), "About", 26, BLACK, WHITE, GameState.ABOUT),
        UIElement((MENU_WIDTH/2, 540), "Quit", 26, BLACK, WHITE, GameState.QUIT),
    ]
    
    clock = pygame.time.Clock()
    
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        
        # Draw background every frame
        screen.blit(menu_background_img, (0, 0))
        
        # Draw buttons and check for clicks
        for button in buttons:
            action = button.update(pygame.mouse.get_pos(), mouse_up)
            button.draw(screen)
            if action:
                return action
        
        pygame.display.flip()
        clock.tick(60)


def play_level(screen):
    global current_direction, current_frame, frame_timer
    global walk_timer, walk_offset
    
    pygame.init()
    pygame.mixer.init()
    paused = False
    clock = pygame.time.Clock()
    collected_items = 0
    floating_texts = []
    rooms = {}
    
    # Set initial room temporarily to get viewport
    temp_room = Room(
        "photos/background_photos/Hallway_Main_Floor_A_Update.png",
        (3600, 700),
        doors={},
        viewport=(1500, 700)
    )
    current_room = temp_room
    
    # Create camera
    camera_group = Camera(current_room.viewport)
    
    screen = pygame.display.set_mode(current_room.viewport)
    pygame.display.set_caption("Haunted Meadow Brook")
    
    # Load ghost image
    ghost_img = pygame.image.load("photos\\grizzly_photos\\grizzly_ghost.png").convert_alpha()
    ghost_img = pygame.transform.scale(ghost_img, (GHOST_SIZE))
    
    # Load Party Supplies image

    def random_position(room_size, margin=100):
        x = random.randint(margin, room_size[0] - margin)
        y = random.randint(margin, room_size[1] - margin)
        return (x, y)

    ps1_img = load_scaled("photos/party_supplies/Ps1.png", (80,80))
    ps2_img = load_scaled("photos/party_supplies/Ps2.png", (80,80))
    ps3_img = load_scaled("photos/party_supplies/Ps3.png", (80,80))
    ps4_img = load_scaled("photos/party_supplies/Ps4.png", (80,80))
    ps5_img = load_scaled("photos/party_supplies/Ps5.png", (80,80))

    hallway_collectibles = [
        Collectible(random_position((3600,700)), ps1_img, camera_group),
        Collectible(random_position((3600,700)), ps2_img, camera_group)
    ]
    dining_collectibles = [
        Collectible(random_position((1000,900)), ps3_img, camera_group)
    ]
    alfred_collectibles = [
        Collectible(random_position((900,900)), ps4_img, camera_group)
    ]
    matilda_collectibles = [
        Collectible(random_position((900,900)), ps5_img, camera_group)
    ]
    main_great_collectibles = [
        Collectible(random_position((1000,1250)), ps5_img, camera_group)
    ]
    living_room_collectibles = [
        Collectible(random_position((900,900)), ps5_img, camera_group)
    ]
    library_collectibles = [
        Collectible(random_position((900,900)), ps5_img, camera_group)
    ]
    
    
    # Create separate ghosts for each room
    hallwayA_ghost_room = pygame.Rect(0, 0, 3600, 700)
    hallwayA_ghosts = [
        Ghost(
            start_pos=(1200, 550),
            room_rect=hallwayA_ghost_room,
            image=ghost_img,
            group=camera_group  
        ),
        Ghost(
            start_pos=(1800, 150),
            room_rect=hallwayA_ghost_room,
            image=ghost_img,
            group=camera_group  
        ),
    ]
    dining_ghost_room = pygame.Rect(0, 0, 1000, 900)  
    dining_ghosts = [
        Ghost(
            start_pos=(150, 300),
            room_rect=dining_ghost_room,
            image=ghost_img,
            group=camera_group  
        ),
    ]
    alfredstudy_ghost_room = pygame.Rect(0, 0, 900, 900)  
    alfred_study_ghosts = [
        Ghost(
            start_pos=(250, 200),
            room_rect=alfredstudy_ghost_room,
            image=ghost_img,
            group=camera_group  
        )
    ]
    matildastudy_ghost_room = pygame.Rect(0, 0, 900, 900)  
    matilda_study_ghosts = [
        Ghost(
            start_pos=(250, 200),
            room_rect=matildastudy_ghost_room,
            image=ghost_img,
            group=camera_group  
        )
    ]
    maingreat_ghost_room = pygame.Rect(0, 0, 1000, 1100)  
    main_great_ghosts = [
        Ghost(
            start_pos=(900, 1000),
            room_rect=maingreat_ghost_room,
            image=ghost_img,
            group=camera_group  
        )
    ]
    living_ghost_room = pygame.Rect(0, 0, 900, 900)  
    living_room_ghosts = [
        Ghost(
            start_pos=(800, 200),
            room_rect=living_ghost_room,
            image=ghost_img,
            group=camera_group  
        )
    ]
    library_ghost_room = pygame.Rect(0, 0, 900, 900)  
    library_ghosts = [
        Ghost(
            start_pos=(800, 800),
            room_rect=library_ghost_room,
            image=ghost_img,
            group=camera_group  
        )
    ]
    
    # Create rooms with their own ghosts
    hallway_A = Room(
        "photos/background_photos/Hallway_Main_Floor_A_Update.png",
        (3600, 700),
        doors={
            "hallwayA_to_dining": {
                'rect': pygame.Rect(250, 100, 25, 50), 
                'target_room': "dining_room",
                'spawn_pos': (850, 750) 
            },
            "hallwayA_to_alfred": {
                'rect': pygame.Rect(1525, 100, 25, 50), 
                'target_room': "alfred_study",
                'spawn_pos': (200, 750) 
            },
            "hallwayA_to_matilda": {
                'rect': pygame.Rect(2350, 100, 25, 50), 
                'target_room': "matilda_study",
                'spawn_pos': (200, 750) 
            },
            "hallwayA_to_maingreat": {
                'rect': pygame.Rect(3550, 425, 10, 50), 
                'target_room': "main_great_hall",
                'spawn_pos': (200, 525) 
            }
        },
        ghosts=hallwayA_ghosts,
        collectibles=hallway_collectibles,
        viewport=(1500, 700),
    )

    dining_room = Room(
        "photos/background_photos/Dining_Room.png",
        (1000, 900),
        doors={
            "dining_to_hallwayA": {
                'rect': pygame.Rect(900, 850, 50, 60),  
                'target_room': "hallway_A",
                'spawn_pos': (250, 300)  
            }
        },
        ghosts=dining_ghosts,
        collectibles=dining_collectibles,
        viewport=(1000, 700),
        respawn_pos=(850, 750)
    )
    
    alfred_study = Room(
        "photos/background_photos/Alfreds_Study.png",
        (900, 900),
        doors={
            "alfred_to_hallwayA": {
                'rect': pygame.Rect(100, 850, 50, 60),  
                'target_room': "hallway_A",
                'spawn_pos': (1525, 300)  
            }
        },
        ghosts=alfred_study_ghosts,
        collectibles=alfred_collectibles,
        viewport=(900, 700),
        respawn_pos=(200, 750)
    )
    
    matilda_study = Room(
        "photos/background_photos/Matildas_Study.png",
        (900, 900),
        doors={
            "matilda_to_hallwayA": {
                'rect': pygame.Rect(100, 850, 50, 60),  
                'target_room': "hallway_A",
                'spawn_pos': (2350, 300)  
            }
        },
        ghosts=matilda_study_ghosts,
        collectibles=matilda_collectibles,
        viewport=(900, 700),
        respawn_pos=(200, 750)
    )
    
    main_great_hall = Room(
        "photos/background_photos/Great_Hall.png",
        (1000, 1250),
        doors={
            "maingreat_to_hallwayA": {
                'rect': pygame.Rect(50, 525, 10, 50),  
                'target_room': "hallway_A",
                'spawn_pos': (3400, 400)  
            },
            "maingreat_to_living": {
                'rect': pygame.Rect(950, 150, 10, 50),  
                'target_room': "living_room",
                'spawn_pos': (200, 300)  
            }
        },
        ghosts=main_great_ghosts,
        collectibles=main_great_collectibles,
        viewport=(1000, 700),
        respawn_pos=(250, 1150)
    )
    
    living_room = Room(
        "photos/background_photos/Living_Room.png",
        (900, 900),
        doors={
            "living_to_maingreat": {
                'rect': pygame.Rect(50, 300, 10, 50),  
                'target_room': "main_great_hall",
                'spawn_pos': (750, 250)  
            },
            "living_to_library": {
                'rect': pygame.Rect(250, 850, 50, 15),  
                'target_room': "library",
                'spawn_pos': (175, 300)  
            }
        },
        ghosts=living_room_ghosts,
        collectibles=living_room_collectibles,
        viewport=(900, 700),
        respawn_pos=(300, 550)
    )
    
    library = Room(
        "photos/background_photos/Library.png",
        (900, 900),
        doors={
            "library_to_living": {
                'rect': pygame.Rect(175, 100, 25, 50),  
                'target_room': "living_room",
                'spawn_pos': (225, 750)  
            }
        },
        ghosts=library_ghosts,
        collectibles=library_collectibles,
        viewport=(900, 700),
        respawn_pos=(175, 300)
    )
    
    # Room dictionary
    rooms = {
        "hallway_A": hallway_A,
        "dining_room": dining_room,
        "alfred_study": alfred_study,
        "matilda_study": matilda_study,
        "main_great_hall": main_great_hall,
        "living_room": living_room,
        "library": library
    }
    
    # Set initial current room
    current_room = hallway_A
    
    # Create player
    player = Player(
        image=animations["forward"][0],
        pos=(current_room.viewport[0] // 2, current_room.viewport[1] // 2),
        group=camera_group
    )
    
    player.dead = False
    player.death_finished = False
    player.death_frame = 0
    
    #PAUSE BUTTON
    pause_button = UIElement(
        center_position=(current_room.viewport[0] - 60, 40),
        text="II",
        font_size=26,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        action="PAUSE"
    )
    
    # Buttons after Player Death
    retry_btn = UIElement((current_room.viewport[0]//2, current_room.viewport[1]//2 + 120), 
                          "Retry", 30, BLACK, WHITE, GameState.START)
    menu_btn = UIElement((current_room.viewport[0]//2, current_room.viewport[1]//2 + 190), 
                         "Main Menu", 30, BLACK, WHITE, GameState.MENU)
    
    # Define enter_room function
    def enter_room(room, spawn_pos):
        nonlocal player, current_room, pause_button, camera_group
        
        current_room = room
        player.rect.center = spawn_pos
        
        # push the player out of any door they happen to land in
        for info in room.doors.values():
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
    
    while True:
        dt = clock.tick(60)
        mouse_up = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = not paused
                return GameState.MENU
        
        if player.dead:
            player.death_frame_timer += dt
            
            if not player.death_finished:
                if player.death_frame_timer >= DEATH_FRAME_DELAY:
                    player.death_frame += 1
                    player.death_frame_timer = 0
                    
                    if player.death_frame >= len(animations["death"]):
                        player.death_frame = len(animations["death"]) - 1
                        player.death_finished = True
                        
            frame = pygame.transform.scale(animations["death"][player.death_frame], screen.get_size())
            screen.blit(frame, (0, 0))
            
            if player.death_finished:
                w, h = screen.get_size()

                retry_btn.rects[0].center = (w//2, h//2 + 120)
                retry_btn.rects[1].center = (w//2, h//2 + 120)

                menu_btn.rects[0].center = (w//2, h//2 + 190)
                menu_btn.rects[1].center = (w//2, h//2 + 190)

                action = retry_btn.update(pygame.mouse.get_pos(), mouse_up)
                retry_btn.draw(screen)

                action2 = menu_btn.update(pygame.mouse.get_pos(), mouse_up)
                menu_btn.draw(screen)

                if action == GameState.START:
                    # Reset player at the respawn position of current room
                    if current_room.respawn_pos == None:
                        player.reset((current_room.viewport[0] // 2, current_room.viewport[1] // 2))
                    else:
                        player.reset(current_room.respawn_pos)
                        
                    # Reset ghosts of current room
                    for ghost in current_room.ghosts:
                        ghost.reset()
                        
                    continue
                
                elif action2 == GameState.MENU:
                    return GameState.MENU
                
            pygame.display.update()
            continue
            
        # Update pause button
        action = pause_button.update(pygame.mouse.get_pos(), mouse_up)
        if action == "PAUSE":
            paused = not paused
            mouse_up = False
            
        # Draw pause overlay if paused
        if paused:
            overlay = pygame.Surface(current_room.viewport, pygame.SRCALPHA)
            overlay.fill(CLEAR)
            screen.blit(overlay, (0, 0))
            pause_text = create_surface_with_text("PAUSED", 48, WHITE, BLACK)
            screen.blit(
                pause_text, 
                pause_text.get_rect(center=(current_room.viewport[0]//2, current_room.viewport[1]//2))
            )
            
            # Buttons on pause screen
            pause_buttons = [
                UIElement((current_room.viewport[0]//2, current_room.viewport[1]//2 - 65), 
                          "Resume", 30, BLACK, WHITE, "RESUME"),
                UIElement((current_room.viewport[0]//2, current_room.viewport[1]//2 + 70), 
                          "Settings", 26, BLACK, WHITE, "SETTINGS"),
                UIElement((current_room.viewport[0]//2, current_room.viewport[1]//2 + 130), 
                          "Quit", 26, BLACK, WHITE, "QUIT"),
            ]
            
            for btn in pause_buttons:
                menu_action = btn.update(pygame.mouse.get_pos(), mouse_up)
                btn.draw(screen)
                
                if menu_action == "RESUME":
                    paused = False
                    mouse_up = False
                elif menu_action == "SETTINGS":
                    mouse_up = False
                    settings(screen, current_room.viewport[0], current_room.viewport[1], GameState.START)
                elif menu_action == "QUIT":
                    return GameState.MENU
            
        else:
            keys = pygame.key.get_pressed()
            moving = False

            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player.direction.x = -1
                current_direction = "left"
                moving = True
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player.direction.x = 1
                current_direction = "right"
                moving = True
            else:
                player.direction.x = 0
                
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player.direction.y = -1
                current_direction = "back"
                moving = True
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player.direction.y = 1
                current_direction = "forward"
                moving = True
            else:
                player.direction.y = 0

            if moving:
                frame_timer += dt
                walk_timer += dt

                if frame_timer >= FRAME_DELAY:
                    current_frame = (current_frame + 1) % 4
                    frame_timer = 0

                if walk_timer >= BOB_DELAY:
                    walk_offset = -BOB_AMOUNT if walk_offset == 0 else 0
                    walk_timer = 0
            else:
                current_frame = 0
                frame_timer = 0
                walk_offset = 0

            player.image = animations[current_direction][current_frame]
            for ghost in current_room.ghosts:
                ghost.update(dt, player)
                
            # Clamp player to room bounds
            player.rect.clamp_ip(current_room.bg_rect)
            player.update()
            
            # Check if player hits a door
            door_hit = current_room.get_door_at(player.rect)
            if door_hit:
                door_sound.play()  # play door sound
                enter_room(rooms[door_hit['target_room']], door_hit['spawn_pos'])
                
            camera_group.box_target_camera(player, current_room.size)
            camera_group.custom_draw(player, current_room)
          
            # COLLECTIBLE COLLISION
            for item in current_room.collectibles[:]:
                if player.rect.colliderect(item.rect):
                    item.collect()
                    current_room.collectibles.remove(item)
                    collected_items += 1
                    floating_texts.append(FloatingText("+1", item.rect.center))
                    print("Collected:", collected_items)
                    
            # ACHIEVEMENT CHECK
            if collected_items >= 10:
                achievements_data[1]["unlocked"] = True
            
            # Update floating text
            for ft in floating_texts[:]:
                if not ft.update():  
                    floating_texts.remove(ft)
                
                # Draw floating text

            for ft in floating_texts:
                ft.draw(screen)

        pause_button.draw(screen)
        pygame.display.update()

if __name__ == "__main__":
    main()
