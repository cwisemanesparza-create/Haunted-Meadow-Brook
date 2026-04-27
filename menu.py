import pygame
import pygame.freetype
import random, math
import os
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from random import randint

from ui_elements import *
from global_variables import *
from game_state import *
from main import *

# Menu screen
def menu(screen, game_state):
    screen = pygame.display.set_mode(MENU_SIZE)
    
    # Load menu background
    try:
        menu_background_img = pygame.image.load("photos/screen.png").convert()
        menu_background_img = pygame.transform.scale(menu_background_img, MENU_SIZE)
    except Exception as e:
        print(f"Error loading screen.png: {e}")
        menu_background_img = pygame.Surface(MENU_SIZE)
        menu_background_img.fill(ORANGE)
    
    # Menu buttons
    buttons = [
        UIElement((MENU_WIDTH/2, 300), "Start", 30, BLACK, WHITE, GameState.START),
        UIElement((MENU_WIDTH/2, 360), "Settings", 26, BLACK, WHITE, GameState.SETTINGS),
        UIElement((MENU_WIDTH/2, 420), "Achievements", 26, BLACK, WHITE, GameState.ACHIEVEMENTS),
        UIElement((MENU_WIDTH/2, 480), "About", 26, BLACK, WHITE, GameState.ABOUT),
        UIElement((MENU_WIDTH/2, 540), "Quit", 26, BLACK, WHITE, GameState.QUIT),
    ]
    
    clock = pygame.time.Clock()
    
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        
        # Draw background every frame
        screen.blit(menu_background_img, (0, 0))
        
        # Draw buttons and check for clicks
        for button in buttons:
            action = button.update(pygame.mouse.get_pos(), mouse_up)
            button.draw(screen)
            if action:
                if game_state == GameState.START:
                    if action == GameState.START:
                        screen.fill(ORANGE) # background color when return to pause screen
                        return game_state
                    else:
                        return action
                else:
                    return action
        
        pygame.display.flip()
        clock.tick(60)