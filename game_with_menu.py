import pygame
import pygame.freetype
from pygame.sprite import Sprite
from enum import Enum
from pygame.rect import Rect
import random

# -------------------------------
# GHOST AI (WANDERING ONLY)
# -------------------------------

#ghost_img = pygame.image.load("photos\\grizzly_photos\\grizzly_ghost.png").convert_alpha()
#ghost_img = pygame.transform.scale(ghost_img, (120, 140))  # adjust size if needed

class Ghost(pygame.sprite.Sprite):
    def __init__(self, start_pos, room_rect,image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=start_pos)

        self.room_rect = room_rect
        self.speed = 4

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


#set width and height of screen
WIDTH = 900
HEIGHT = 700

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 140, 0)

#load grizzly mascot player photo
player = pygame.image.load("photos\\grizzly_photos\\grizzly_mascot_pixel.png")
player_rect = player.get_rect(center = (500, 400)) #player starts at (x, y)
player = pygame.transform.scale(player, (200, 250)) #player scale to size (x, y)
vel = 15 #set velocity of player movement

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
    MENU = 0
    START = 1
    SETTINGS = 2
    ACHIEVEMENTS = 3
    ABOUT = 4
    QUIT = -1

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Haunted Meadow Brook")
    action = GameState.MENU

    while True:
        if action == GameState.MENU:
            action = menu(screen)
        
        if action == GameState.START:
            action = play_level(screen)     
        
        if action == GameState.SETTINGS:
            #action = settings()
            print("Settings menu")
        
        if action == GameState.ACHIEVEMENTS:
            #action = achievements()
            print("Achievements")
        
        if action == GameState.ABOUT:
            #action = about()
            print("About screen")
        
        if action == GameState.QUIT:
            pygame.quit()
            return

def menu(screen):

    # Buttons (bottom half)
    buttons = [
        UIElement((WIDTH/2, 300), "Start", 30, BLACK, WHITE, GameState.START),
        UIElement((WIDTH/2, 360), "Settings", 26, BLACK, WHITE, GameState.SETTINGS),
        UIElement((WIDTH/2, 420), "Achievements", 26, BLACK, WHITE, GameState.ACHIEVEMENTS),
        UIElement((WIDTH/2, 480), "About", 26, BLACK, WHITE, GameState.ABOUT),
        UIElement((WIDTH/2, 540), "Quit", 26, BLACK, WHITE, GameState.QUIT),
    ]
    
    # Title text
    title_surface = create_surface_with_text(
        "HAUNTED MEADOW BROOK",
        48,
        WHITE,
        ORANGE,
        padding=20
    )
    title_rect = title_surface.get_rect(center=(WIDTH/2, 140))
    
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

            if action == GameState.MENU:
                action = menu(screen)
            elif action == GameState.START:
                action = play_level(screen)     
            elif action == GameState.SETTINGS:
                #action = settings()
                print("Settings menu")
            elif action == GameState.ACHIEVEMENTS:
                #action = achievements()
                print("Achievements")
            elif action == GameState.ABOUT:
                #action = about()
                print("About screen")
            elif action == GameState.QUIT:
                pygame.quit()
                return
        
            button.draw(screen)
        pygame.display.flip()


def play_level(screen):
    clock = pygame.time.Clock()# Load ghost image AFTER display is initialized
    ghost_img = pygame.image.load(
        "photos\\grizzly_photos\\grizzly_ghost.png"
    ).convert_alpha()
    ghost_img = pygame.transform.scale(ghost_img, (120, 140))

    

    # Define the room the ghost can wander in
    ghost_room = pygame.Rect(150, 120, 600, 450)

    # Create the ghost
    ghost = Ghost(
    start_pos=ghost_room.center,
    room_rect=ghost_room,
    image=ghost_img
    )

    run = True
    while run:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # ---------------- PLAYER MOVEMENT ----------------
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player_rect.x -= vel
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player_rect.x += vel
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player_rect.y -= vel
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player_rect.y += vel

        # Keep player inside screen
        if player_rect.right > WIDTH + 150:
            player_rect.right = WIDTH + 150
        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.bottom > HEIGHT + 225:
            player_rect.bottom = HEIGHT + 225
        if player_rect.top < 0:
            player_rect.top = 0

        # ---------------- GHOST UPDATE ----------------
        ghost.update(dt)

        # ---------------- DRAW ----------------
        screen.fill(ORANGE)

        # Debug: draw ghost room boundary
        pygame.draw.rect(screen, BLACK, ghost_room, 3)

        screen.blit(player, player_rect)
        screen.blit(ghost.image, ghost.rect)

        pygame.display.update()

if __name__ == "__main__":
    main()