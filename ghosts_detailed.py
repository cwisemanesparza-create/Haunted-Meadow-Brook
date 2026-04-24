import pygame
import pygame.freetype
import random, math
import os
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from random import randint

from other_functions import *
from global_variables import *
from ghost import Ghost

# Ghosts Detailed function
def ghosts_detailed(ghost_img, camera):
    
    # Create separate ghosts for each room
    hallwayA_ghost_room = pygame.Rect(0, 0, 3600, 700)
    hallwayA_ghosts = [
        Ghost(
            start_pos=(1500, 550),
            room_rect=hallwayA_ghost_room,
            image=ghost_img,
            group=camera
        ),
        Ghost(
            start_pos=(1800, 150),
            room_rect=hallwayA_ghost_room,
            image=ghost_img,
            group=camera 
        ),
    ]
    dining_ghost_room = pygame.Rect(0, 0, 1000, 900)  
    dining_ghosts = [
        Ghost(
            start_pos=(150, 300),
            room_rect=dining_ghost_room,
            image=ghost_img,
            group=camera 
        ),
    ]
    alfredstudy_ghost_room = pygame.Rect(0, 0, 900, 900)  
    alfred_study_ghosts = [
        Ghost(
            start_pos=(250, 200),
            room_rect=alfredstudy_ghost_room,
            image=ghost_img,
            group=camera 
        )
    ]
    matildastudy_ghost_room = pygame.Rect(0, 0, 900, 900)  
    matilda_study_ghosts = [
        Ghost(
            start_pos=(250, 200),
            room_rect=matildastudy_ghost_room,
            image=ghost_img,
            group=camera
        )
    ]
    
    maingreat_ghost_room = pygame.Rect(0, 0, 1000, 900)  
    main_great_ghosts = [
        Ghost(
            start_pos=(900,800),
            room_rect=maingreat_ghost_room,
            image=ghost_img,
            group=camera 
        )
    ]
    
    living_ghost_room = pygame.Rect(0, 0, 900, 900)  
    living_ghosts = [
        Ghost(
            start_pos=(800, 200),
            room_rect=living_ghost_room,
            image=ghost_img,
            group=camera  
        )
    ]
    hallwayC_ghost_room = pygame.Rect(0, 0, 700, 1850)  
    hallwayC_ghosts = [
        Ghost(
            start_pos=(150, 950),
            room_rect=hallwayC_ghost_room,
            image=ghost_img,
            group=camera  
        )
    ]
    library_ghost_room = pygame.Rect(0, 0, 900, 900)  
    library_ghosts = [
        Ghost(
            start_pos=(800, 800),
            room_rect=library_ghost_room,
            image=ghost_img,
            group=camera  
        )
    ]
    
    lowerhallway_ghost_room = pygame.Rect(0, 0, 3600, 700)
    lower_hallway_ghosts = [
        Ghost(
            start_pos=(2000, 150),
            room_rect=lowerhallway_ghost_room,
            image=ghost_img,
            group=camera
        ),
        Ghost(
            start_pos=(2600, 150),
            room_rect=lowerhallway_ghost_room,
            image=ghost_img,
            group=camera 
        ),
    ]
    game_ghost_room = pygame.Rect(0, 0, 916, 905)  
    game_ghosts = [
        Ghost(
            start_pos=(250, 200),
            room_rect=game_ghost_room,
            image=ghost_img,
            group=camera 
        )
    ]
    lowergreat_ghost_room = pygame.Rect(0, 0, 1000, 900)  
    lower_great_ghosts = [
        Ghost(
            start_pos=(850, 100),
            room_rect=lowergreat_ghost_room,
            image=ghost_img,
            group=camera 
        )
    ]
    ball_ghost_room = pygame.Rect(0, 0, 1280, 1000)  
    ballroom_ghosts = [
        Ghost(
            start_pos=(1000, 800),
            room_rect=ball_ghost_room,
            image=ghost_img,
            group=camera 
        ),
        Ghost(
            start_pos=(200, 800),
            room_rect=ball_ghost_room,
            image=ghost_img,
            group=camera 
        )
    ]
    
    # Ghosts dictionary
    ghosts = {
        "hallwayA_ghosts": hallwayA_ghosts,
        "dining_ghosts": dining_ghosts,
        "alfred_study_ghosts": alfred_study_ghosts,
        "matilda_study_ghosts": matilda_study_ghosts,
        "main_great_ghosts": main_great_ghosts,
        "living_ghosts": living_ghosts,
        "hallwayC_ghosts": hallwayC_ghosts,
        "library_ghosts": library_ghosts,
        "lower_hallway_ghosts": lower_hallway_ghosts,
        "game_ghosts": game_ghosts,
        "lower_great_ghosts": lower_great_ghosts,
        "ballroom_ghosts": ballroom_ghosts
    }
    
    return ghosts
    
    
