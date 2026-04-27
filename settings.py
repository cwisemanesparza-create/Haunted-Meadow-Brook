import pygame
from pygame.rect import Rect

from ui_elements import *
from global_variables import *
from game_state import *

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