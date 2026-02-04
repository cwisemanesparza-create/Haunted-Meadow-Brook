import pygame
import pygame.freetype
from pygame.sprite import Sprite
from enum import Enum

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 140, 0)

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text, fgcolor=text_rgb, bgcolor=bg_rgb)
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
            font_size=int(font_size * 1.2),
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
    TITLE = 0
    START = 1
    SETTINGS = 2
    ACHIEVEMENTS = 3
    ABOUT = 4
    QUIT = -1

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Haunted Meadow Brook")

    buttons = [
        UIElement((400, 260), "Start", 32, BLUE, WHITE, GameState.START),
        UIElement((400, 320), "Settings", 28, BLUE, WHITE, GameState.SETTINGS),
        UIElement((400, 380), "Achievements", 28, BLUE, WHITE, GameState.ACHIEVEMENTS),
        UIElement((400, 440), "About", 28, BLUE, WHITE, GameState.ABOUT),
        UIElement((400, 500), "Quit", 28, BLUE, WHITE, GameState.QUIT),
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

        for button in buttons:
            action = button.update(pygame.mouse.get_pos(), mouse_up)

            if action == GameState.START:
                print("Start game")
            elif action == GameState.SETTINGS:
                print("Open settings menu")
            elif action == GameState.ACHIEVEMENTS:
                print("Open achievements")
            elif action == GameState.ABOUT:
                print("Open about screen")
            elif action == GameState.QUIT:
                pygame.quit()
                return

            button.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    main()