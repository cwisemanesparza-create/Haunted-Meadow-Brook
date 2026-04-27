import pygame
import pygame.freetype
import random, math
import os
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from random import randint

from game_state import *
from global_variables import *
from other_functions import *
from play_level import *

# Main function (run this file to open game)
def main():
    global MASTER_VOLUME, MUSIC_VOLUME

    pygame.init()
    pygame.mixer.init()
    
    screen = pygame.display.set_mode((MENU_SIZE))
    pygame.display.set_caption("Haunted Meadow Brook")

    # Load background music safely
    music_file = ("music&text/spooky_theme.mp3")
    if os.path.isfile(music_file):
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.set_volume(MUSIC_VOLUME)
        pygame.mixer.music.play(-1)
    else:
        print(f"Warning: {music_file} not found. Music disabled.")
    
    state = GameState.MENU

    while True:
        if state == GameState.MENU:
            state = menu(screen, game_state = GameState.MENU)
        elif state == GameState.START:
            state = play_level(screen)
        elif state == GameState.SETTINGS:
            # settings screen adjusts to current screen size
            state = settings(screen, MENU_WIDTH, MENU_HEIGHT, game_state = GameState.MENU)
        elif state == GameState.ACHIEVEMENTS:
            load_achievement_images() # <-- load images first
            state = achievements(screen, game_state = GameState.MENU)
        elif state == GameState.ABOUT:
            state = about(screen, game_state = GameState.MENU)
        elif state == GameState.QUIT:
            pygame.quit()
            return
        
if __name__ == "__main__":
    main()