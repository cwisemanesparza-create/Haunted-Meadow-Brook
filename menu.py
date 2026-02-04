import pygame
import pygame.freetype
from pygame.sprite import Sprite
from enum import Enum

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 140, 0)

def create_surface_with_text(text, font_size, text_rgb, bg_rgb, padding=12):
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    text_surface, _ = font.render(text, fgcolor=text_rgb)

    width = text_surface.get_width() + padding * 2
    height = text_surface.get_height() + padding * 2

    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    surface.fill(bg_rgb)
    surface.blit(text_surface, (padding, padding))

    return surface.convert_alpha()

class UIElement(Sprite):
    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb, action=None):
        super().__init__()

        self.action = action
        self.mouse_over = False

        default_image = create_surface_with_text(
            text=text,
            font_size=font_size,
            text_rgb=text_rgb,
            bg_rgb=bg_rgb
        )

        highlighted_image = create_surface_with_text(
            text=text,
            font_size=int(font_size * 1.15),
            text_rgb=text_rgb,
            bg_rgb=bg_rgb
        )

        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
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

class GameState(Enum):
    START = 1
    SETTINGS = 2
    ACHIEVEMENTS = 3
    ABOUT = 4
    QUIT = -1

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Haunted Meadow Brook")

    # Title text
    title_surface = create_surface_with_text(
        "HAUNTED MEADOW BROOK",
        48,
        WHITE,
        ORANGE,
        padding=20
    )
    title_rect = title_surface.get_rect(center=(400, 140))

    # Buttons (bottom half)
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
                return
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.fill(ORANGE)

        # Draw title (top half)
        screen.blit(title_surface, title_rect)

        # Draw buttons (bottom half)
        for button in buttons:
            action = button.update(pygame.mouse.get_pos(), mouse_up)

            if action == GameState.START:
                print("Start game")
            elif action == GameState.SETTINGS:
                 result = settings_screen(screen)
            if result == GameState.QUIT:
                pygame.quit()
                return
            elif action == GameState.ACHIEVEMENTS:
                print("Achievements")
            elif action == GameState.ABOUT:
                print("About screen")
            elif action == GameState.QUIT:
                pygame.quit()
                return

            button.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()

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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.track_rect.collidepoint(event.pos):
                self.dragging = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        if event.type == pygame.MOUSEMOTION and self.dragging:
            rel_x = max(self.x, min(event.pos[0], self.x + self.width))
            self.value = (rel_x - self.x) / self.width

    def draw(self, screen):
        # label
        font = pygame.font.Font(None, 28)
        label_surf = font.render(self.label, True, WHITE)
        screen.blit(label_surf, (self.x, self.y - 30))

        # track
        pygame.draw.rect(screen, WHITE, self.track_rect, 2)

        # knob
        knob_x = self.x + int(self.value * self.width)
        knob_y = self.y + self.height // 2
        pygame.draw.circle(screen, WHITE, (knob_x, knob_y), self.knob_radius)

        def settings_screen(screen):
    clock = pygame.time.Clock()

    # Audio table header
    header_font = pygame.font.Font(None, 36)
    header_surface = header_font.render("AUDIO SETTINGS", True, WHITE)
    header_rect = pygame.Rect(200, 50, 400, 60)

    # Sliders
    master_slider = Slider((250, 180), (300, 8), "Master Volume", 0.8)
    music_slider = Slider((250, 260), (300, 8), "Music Volume", 0.6)

    back_btn = UIElement(
        center_position=(400, 500),
        text="Back",
        font_size=28,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        action=GameState.TITLE,
    )

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return GameState.QUIT

            master_slider.handle_event(event)
            music_slider.handle_event(event)

            if event.type == pygame.MOUSEBUTTONUP:
                action = back_btn.update(pygame.mouse.get_pos(), True)
                if action == GameState.TITLE:
                    return GameState.TITLE

        screen.fill(ORANGE)

        # Draw audio table
        pygame.draw.rect(screen, BLACK, header_rect)
        screen.blit(header_surface, header_surface.get_rect(center=header_rect.center))

        # Draw sliders
        master_slider.draw(screen)
        music_slider.draw(screen)

        back_btn.update(pygame.mouse.get_pos())
        back_btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)

