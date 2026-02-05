import pygame
import pygame.freetype
from pygame.sprite import Sprite
from enum import Enum
import os

# Colors

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 140, 0)

# Helper function

def create_surface_with_text(text, font_size, text_rgb, bg_rgb, padding=12, font_path=None):
    if font_path:
        font = pygame.freetype.Font(font_path, font_size)
    else:
        font = pygame.freetype.SysFont("Courier", font_size, bold=True)
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
        default_image = create_surface_with_text(text, font_size, text_rgb, bg_rgb)
        highlighted_image = create_surface_with_text(text, int(font_size*1.15), text_rgb, bg_rgb)
        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position)
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

# Game states

class GameState(Enum):
    TITLE = 0
    START = 1
    SETTINGS = 2
    ACHIEVEMENTS = 3
    ABOUT = 4
    QUIT = -1

# Global volume values

MASTER_VOLUME = 0.8
MUSIC_VOLUME = 0.6

# Settings screen

def settings_screen(screen):
    global MASTER_VOLUME, MUSIC_VOLUME
    clock = pygame.time.Clock()

    header_font = pygame.font.Font(None, 36)
    header_surface = header_font.render("AUDIO SETTINGS", True, WHITE)
    header_rect = pygame.Rect(200, 50, 400, 60)

    master_slider = Slider((250, 180), (300, 8), "Master Volume", MASTER_VOLUME)
    music_slider = Slider((250, 260), (300, 8), "Music Volume", MUSIC_VOLUME / MASTER_VOLUME if MASTER_VOLUME>0 else 0)

    back_btn = UIElement((400, 500), "Back", 28, BLACK, WHITE, GameState.TITLE)

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

        # Update volume in real time
        MASTER_VOLUME = master_slider.value
        MUSIC_VOLUME = music_slider.value * MASTER_VOLUME
        pygame.mixer.music.set_volume(MUSIC_VOLUME)

        # Draw screen
        screen.fill(ORANGE)
        pygame.draw.rect(screen, BLACK, header_rect)
        screen.blit(header_surface, header_surface.get_rect(center=header_rect.center))
        master_slider.draw(screen)
        music_slider.draw(screen)

        action = back_btn.update(pygame.mouse.get_pos(), mouse_up)
        back_btn.draw(screen)
        if action == GameState.TITLE:
            return GameState.TITLE

        pygame.display.flip()
        clock.tick(60)

# Main menu loop

def main_menu_loop(screen):
    title_surface = create_surface_with_text(
    "HAUNTED MEADOW BROOK",
    90,
    WHITE,
    ORANGE,
    padding=20,
    font_path="BlackWitcher.otf"
    )

    title_rect = title_surface.get_rect(center=(400, 140))

    buttons = [
        UIElement((400, 300), "Start", 30, BLACK, WHITE, GameState.START),
        UIElement((400, 360), "Settings", 26, BLACK, WHITE, GameState.SETTINGS),
        UIElement((400, 420), "Achievements", 26, BLACK, WHITE, GameState.ACHIEVEMENTS),
        UIElement((400, 480), "About", 26, BLACK, WHITE, GameState.ABOUT),
        UIElement((400, 540), "Quit", 26, BLACK, WHITE, GameState.QUIT),
    ]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.fill(ORANGE)
        screen.blit(title_surface, title_rect)

        for button in buttons:
            action = button.update(pygame.mouse.get_pos(), mouse_up)
            if action == GameState.START:
                print("Start game")  # Replace with actual game loop
            elif action == GameState.SETTINGS:
                result = settings_screen(screen)
                if result == GameState.QUIT:
                    pygame.quit()
                    return GameState.QUIT
            elif action == GameState.ACHIEVEMENTS:
                print("Achievements")
            elif action == GameState.ABOUT:
                print("About screen")
            elif action == GameState.QUIT:
                pygame.quit()
                return GameState.QUIT

            button.draw(screen)

        pygame.display.flip()

# Main function

def main():
    global MASTER_VOLUME, MUSIC_VOLUME
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Haunted Meadow Brook")

    # Load background music safely
    music_file = "spooky_theme.mp3"
    if os.path.isfile(music_file):
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(-1)
    else:
        print(f"Warning: {music_file} not found. Music disabled.")

    result = main_menu_loop(screen)
    if result == GameState.QUIT:
        pygame.quit()

if __name__ == "__main__":
    main()


