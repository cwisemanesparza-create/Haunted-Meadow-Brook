import pygame
import pygame.freetype
import random
import os
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum

# Menu Width, Height, Size
WIDTH = 1500
HEIGHT = 670
SCREEN_SIZE = (WIDTH, HEIGHT)

# Player and Ghost size
PLAYER_SIZE = (150, 190)
GHOST_SIZE = (80, 100)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)

# Global volume values
MASTER_VOLUME = 0.8
MUSIC_VOLUME = 0.6

# Player movement
SPEED = 3
walk_offset = 0
walk_timer = 0
BOB_DELAY = 120
BOB_AMOUNT = 3
current_direction = "forward"
current_frame = 0
frame_timer = 0
FRAME_DELAY = 110

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

# Ghost AI (Wandering Only)
class Ghost(pygame.sprite.Sprite):
    def __init__(self, start_pos, room_rect,image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=start_pos)

        self.room_rect = room_rect
        self.speed = 2

        self.direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
        self.timer = random.randint(400, 1200)

    def update(self, dt):
        self.timer -= dt

        if self.timer <= 0:
            self.direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
            self.timer = random.randint(400, 1200)

        dx, dy = self.direction
        next_rect = self.rect.move(dx * self.speed, dy * self.speed)

        # Keep ghost inside its room
        if self.room_rect.contains(next_rect):
            self.rect = next_rect
        else:
            self.timer = 0

# Game states
class GameState(Enum):
    MENU = 0
    START = 1
    SETTINGS = 2
    ACHIEVEMENTS = 3
    ABOUT = 4
    QUIT = -1

# Settings screen
def settings(screen):
    global MASTER_VOLUME, MUSIC_VOLUME
    clock = pygame.time.Clock()

    header_font = pygame.font.Font(None, 36)
    header_surface = header_font.render("AUDIO SETTINGS", True, WHITE)
    header_rect = pygame.Rect(200, 50, 400, 60)

    master_slider = Slider((250, 180), (300, 8), "Master Volume", MASTER_VOLUME)
    music_slider = Slider((250, 260), (300, 8), "Music Volume", MUSIC_VOLUME / MASTER_VOLUME if MASTER_VOLUME>0 else 0)

    back_btn = UIElement((400, 500), "Back", 28, BLACK, WHITE, GameState.MENU)

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
        screen.fill(ORANGE)
        pygame.draw.rect(screen, BLACK, header_rect)
        screen.blit(header_surface, header_surface.get_rect(center=header_rect.center))
        master_slider.draw(screen)
        music_slider.draw(screen)
        
        action = back_btn.update(pygame.mouse.get_pos(), mouse_up)
        back_btn.draw(screen)
        if action == GameState.MENU:
            return GameState.MENU
        
        # Update volume in real time
        MASTER_VOLUME = master_slider.value
        MUSIC_VOLUME = music_slider.value * MASTER_VOLUME
        pygame.mixer.music.set_volume(MUSIC_VOLUME)

        pygame.display.flip()

# Achievements screen
def achievements(screen):

    header_font = pygame.font.Font(None, 36)
    header_surface = header_font.render("ACHIEVEMENTS", True, WHITE)
    header_rect = pygame.Rect(200, 50, 400, 60)

    back_btn = UIElement((400, 500), "Back", 28, BLACK, WHITE, GameState.MENU)

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
                
        # Draw screen
        screen.fill(ORANGE)
        pygame.draw.rect(screen, BLACK, header_rect)
        screen.blit(header_surface, header_surface.get_rect(center=header_rect.center))
        
        action = back_btn.update(pygame.mouse.get_pos(), mouse_up)
        back_btn.draw(screen)
        if action == GameState.MENU:
            return GameState.MENU

        pygame.display.flip()
        
# About screen
def about(screen):
    clock = pygame.time.Clock()

    header_font = pygame.font.Font(None, 36)
    header_surface = header_font.render("About Haunted Meadow Brook", True, WHITE)
    header_rect = pygame.Rect(200, 50, 400, 60)
    
    back_btn = UIElement((400, 500), "Back", 28, BLACK, WHITE, GameState.MENU)

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
                
        # Draw screen
        screen.fill(ORANGE)
        pygame.draw.rect(screen, BLACK, header_rect)
        screen.blit(header_surface, header_surface.get_rect(center=header_rect.center))
        
        action = back_btn.update(pygame.mouse.get_pos(), mouse_up)
        back_btn.draw(screen)
        if action == GameState.MENU:
            return GameState.MENU

        pygame.display.flip()

def load_scaled(path, size):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, size)

# Main function
def main():
    global animations, player_image, player_rect
    global MASTER_VOLUME, MUSIC_VOLUME

    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_SIZE))
    pygame.display.set_caption("Haunted Meadow Brook")

    SPRITE_SIZE = (150, 190)

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

    player_image = animations["forward"][0]
    player_rect = player_image.get_rect(center=(500, 400))

    state = GameState.MENU

    while True:
        if state == GameState.MENU:
            state = menu(screen)
        elif state == GameState.START:
            state = play_level(screen)
        elif state == GameState.SETTINGS:
            state = settings(screen)
        elif state == GameState.ACHIEVEMENTS:
            state = achievements(screen)
        elif state == GameState.ABOUT:
            state = about(screen)
        elif state == GameState.QUIT:
            pygame.quit()
            return


def menu(screen):
    buttons = [
        UIElement((WIDTH/2, 280), "Start", 30, BLACK, WHITE, GameState.START),
        UIElement((WIDTH/2, 340), "Settings", 26, BLACK, WHITE, GameState.SETTINGS),
        UIElement((WIDTH/2, 400), "Achievements", 26, BLACK, WHITE, GameState.ACHIEVEMENTS),
        UIElement((WIDTH/2, 460), "About", 26, BLACK, WHITE, GameState.ABOUT),
        UIElement((WIDTH/2, 520), "Quit", 26, BLACK, WHITE, GameState.QUIT),
    ]
    
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        menu_background = pygame.Surface(SCREEN_SIZE)
        menu_background_img = pygame.image.load("photos\\screen.png")
        
        screen.fill(ORANGE)
        screen.blit(menu_background_img, (0, 0))

        for button in buttons:
            action = button.update(pygame.mouse.get_pos(), mouse_up)
            button.draw(screen)
            if action:
                return action

        pygame.display.flip()


def play_level(screen):
    global player_image, player_rect
    global current_direction, current_frame, frame_timer
    global walk_timer, walk_offset
    
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_SIZE))
    pygame.display.set_caption("Haunted Meadow Brook")

    #PAUSE BUTTON
    pause_button = UIElement (
        center_position=(WIDTH - 60, 40),
        text="II",
        font_size=26,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        action="PAUSE"
    )

    paused = False
    clock = pygame.time.Clock()

    # Load ghost
    ghost_img = pygame.image.load("photos\\grizzly_photos\\grizzly_ghost.png").convert_alpha()
    ghost_img = pygame.transform.scale(ghost_img, (80, 100))
    ghost_room = pygame.Rect(100, 100, 700, 500)
    ghost = Ghost(start_pos=ghost_room.center, room_rect=ghost_room, image=ghost_img)

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

        # Update pause button
        action = pause_button.update(pygame.mouse.get_pos(), mouse_up)
        if action == "PAUSE":
            paused = not paused

        # Draw pause overlay if paused
        if paused:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))  # dark transparent overlay
            screen.blit(overlay, (0, 0))
            pause_text = create_surface_with_text("PAUSED", 48, WHITE, (0, 0, 0, 0))
            screen.blit(pause_text, pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))

        else:
            keys = pygame.key.get_pressed()
            moving = False

            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player_rect.x -= SPEED
                current_direction = "left"
                moving = True
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player_rect.x += SPEED
                current_direction = "right"
                moving = True
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player_rect.y -= SPEED
                current_direction = "back"
                moving = True
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player_rect.y += SPEED
                current_direction = "forward"
                moving = True

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

            player_image = animations[current_direction][current_frame]
            player_rect.clamp_ip(screen.get_rect())
            ghost.update(dt)

            # Draw everything
            screen.fill(ORANGE)
            screen.blit(player_image, (player_rect.x, player_rect.y + walk_offset))
            screen.blit(ghost.image, ghost.rect)

        pause_button.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    main()
