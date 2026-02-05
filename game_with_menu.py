import pygame
import pygame.freetype
from pygame.sprite import Sprite
from enum import Enum
from pygame.rect import Rect
from pygame.sprite import RenderUpdates

#set width and height of window
width = 800
height = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 140, 0)

#load grizzly mascot player photo
player = pygame.image.load("photos\\grizzly_photos\\grizzly_mascot_pixel.png")
player_rect = player.get_rect(center = (0, 0)) #player starts at (x, y)
player = pygame.transform.scale(player, (200, 250)) #player scale to size (x, y)
vel = 10 #set velocity of player movement

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
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Haunted Meadow Brook")
    action = GameState.MENU
    
    # Title text
    title_surface = create_surface_with_text(
        "HAUNTED MEADOW BROOK",
        48,
        WHITE,
        ORANGE,
        padding=20
    )
    title_rect = title_surface.get_rect(center=(400, 140))
    
    # Draw title (top half)
    screen.blit(title_surface, title_rect)

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
        UIElement((400, 300), "Start", 30, BLACK, WHITE, action=GameState.START),
        UIElement((400, 360), "Settings", 26, BLACK, WHITE, GameState.SETTINGS),
        UIElement((400, 420), "Achievements", 26, BLACK, WHITE, GameState.ACHIEVEMENTS),
        UIElement((400, 480), "About", 26, BLACK, WHITE, GameState.ABOUT),
        UIElement((400, 540), "Quit", 26, BLACK, WHITE, action=GameState.QUIT),
    ]
    
    # Title text
    title_surface = create_surface_with_text(
        "HAUNTED MEADOW BROOK",
        48,
        WHITE,
        ORANGE,
        padding=20
    )
    title_rect = title_surface.get_rect(center=(400, 140))
    
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
    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=ORANGE,
        text_rgb=WHITE,
        text="Return to main menu",
        action=GameState.MENU,
    )

    #run game
    run = True
    while run:
        pygame.time.delay(100)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        #left, right, up, down movement based on keys pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player_rect.x -= vel
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player_rect.x += vel
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player_rect.y -= vel 
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player_rect.y += vel
            
        #keep player inside edges of window
        if player_rect.right > width:
            player_rect.right = width
        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.bottom > height:
            player_rect.bottom = height
        if player_rect.top < 0:
            player_rect.top = 0
        
        screen.fill(ORANGE)    
        screen.blit(player, player_rect)  
        pygame.display.update()

if __name__ == "__main__":
    main()