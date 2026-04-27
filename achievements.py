import pygame
from pygame.sprite import Sprite
from pygame.rect import Rect

from ui_elements import *
from global_variables import *
from game_state import *
from main import *

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
def achievements(screen, game_state):
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
    
    back_btn = UIElement((screen.get_width() // 2, screen.get_height() - 80), "Back", 28, BLACK, WHITE, game_state)

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
        
        if action == game_state:
            if game_state == GameState.START:
                screen.fill(ORANGE) # background color when return to pause screen
                return game_state
            else:
                return game_state

        pygame.display.flip()
        clock.tick(60)