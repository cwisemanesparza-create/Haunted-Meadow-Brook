import pygame
from pygame.rect import Rect

from ui_elements import *
from global_variables import *
from game_state import *

# About screen
def about(screen, game_state):
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
    
    back_btn = UIElement((screen.get_width() // 2, screen.get_height() - 80), "Back", 28, BLACK, WHITE, game_state)
    
    # About text content
    about_text = (
        "Haunted Meadow Brook is a thrilling exploration and horror game set in the mysterious mansion of Oakland University. "
        "Explore rooms, avoid ghosts, uncover secrets, and collect achievements. "
        "Each area of the mansion holds challenges and surprises for brave players. "
        "Immerse yourself in the eerie atmosphere and enjoy the unique soundtrack."
    )
    
    # Text box settings
    text_box_rect = pygame.Rect(150, 150, screen.get_width() - 300, screen.get_height() - 250)
    text_color = WHITE
    font = pygame.font.Font(None, 58)
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

        if action == game_state:
            if game_state == GameState.START:
                screen.fill(ORANGE) # background color when return to pause screen
                return game_state
            else:
                return game_state
            
            
           