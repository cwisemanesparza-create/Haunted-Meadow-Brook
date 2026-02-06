import pygame
import pygame.freetype
from pygame.sprite import Sprite
from enum import Enum

WIDTH = 900
HEIGHT = 700

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)

vel = 3

walk_offset = 0
walk_timer = 0
BOB_DELAY = 120
BOB_AMOUNT = 2

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

class GameState(Enum):
    MENU = 0
    START = 1
    SETTINGS = 2
    ACHIEVEMENTS = 3
    ABOUT = 4
    QUIT = -1

def main():
    global grizz_forward, grizz_back, grizz_left, grizz_right
    global player_image, player_rect

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Haunted Meadow Brook")

    grizz_forward = pygame.image.load(
        "photos/grizzly_photos/8-bit_grizz_face_forward.png"
    ).convert_alpha()

    grizz_back = pygame.image.load(
        "photos/grizzly_photos/8-bit_grizz_face_back.png"
    ).convert_alpha()

    grizz_left = pygame.image.load(
        "photos/grizzly_photos/8-bit_grizz_face_left.png"
    ).convert_alpha()

    grizz_right = pygame.image.load(
        "photos/grizzly_photos/8-bit_grizz_face_right.png"
    ).convert_alpha()

    SPRITE_SIZE = (96, 120)
    grizz_forward = pygame.transform.scale(grizz_forward, SPRITE_SIZE)
    grizz_back = pygame.transform.scale(grizz_back, SPRITE_SIZE)
    grizz_left = pygame.transform.scale(grizz_left, SPRITE_SIZE)
    grizz_right = pygame.transform.scale(grizz_right, SPRITE_SIZE)

    player_image = grizz_forward
    player_rect = player_image.get_rect(center=(500, 400))

    action = GameState.MENU

    while True:
        if action == GameState.MENU:
            action = menu(screen)
        elif action == GameState.START:
            action = play_level(screen)
        elif action == GameState.QUIT:
            pygame.quit()
            return

def menu(screen):
    buttons = [
        UIElement((WIDTH/2, 300), "Start", 30, BLACK, WHITE, GameState.START),
        UIElement((WIDTH/2, 360), "Settings", 26, BLACK, WHITE),
        UIElement((WIDTH/2, 420), "Achievements", 26, BLACK, WHITE),
        UIElement((WIDTH/2, 480), "About", 26, BLACK, WHITE),
        UIElement((WIDTH/2, 540), "Quit", 26, BLACK, WHITE, GameState.QUIT),
    ]

    title_surface = create_surface_with_text(
        "HAUNTED MEADOW BROOK", 48, WHITE, ORANGE, padding=20
    )
    title_rect = title_surface.get_rect(center=(WIDTH/2, 140))

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.fill(ORANGE)
        screen.blit(title_surface, title_rect)

        for button in buttons:
            action = button.update(pygame.mouse.get_pos(), mouse_up)
            button.draw(screen)
            if action:
                return action

        pygame.display.flip()

def play_level(screen):
    global player_image, player_rect, walk_timer, walk_offset

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.MENU

        keys = pygame.key.get_pressed()
        moving = False

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player_rect.x -= vel
            player_image = grizz_left
            moving = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player_rect.x += vel
            player_image = grizz_right
            moving = True
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player_rect.y -= vel
            player_image = grizz_back
            moving = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player_rect.y += vel
            player_image = grizz_forward
            moving = True

        walk_timer += clock.get_time()

        if moving:
            if walk_timer >= BOB_DELAY:
                walk_offset = -BOB_AMOUNT if walk_offset == 0 else 0
                walk_timer = 0
        else:
            walk_offset = 0

        player_rect.clamp_ip(screen.get_rect())

        screen.fill(ORANGE)
        screen.blit(player_image, (player_rect.x, player_rect.y + walk_offset))
        pygame.display.flip()

if __name__ == "__main__":
    main()
