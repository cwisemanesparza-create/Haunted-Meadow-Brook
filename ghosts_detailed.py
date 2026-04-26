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
        
    ]
    
    dining_ghost_room = pygame.Rect(0, 0, 1500, 900)  
    dining_ghosts = [
        Ghost(
            start_pos=(750, 200),
            room_rect=dining_ghost_room,
            image=ghost_img,
            group=camera 
        )
    ]
    
    alfredstudy_ghost_room = pygame.Rect(0, 0, 1500, 900)  
    alfred_study_ghosts = [
        Ghost(
            start_pos=(1200, 450),
            room_rect=alfredstudy_ghost_room,
            image=ghost_img,
            group=camera 
        )
    ]
    
    matildastudy_ghost_room = pygame.Rect(0, 0, 1500, 900)  
    matilda_study_ghosts = [
        Ghost(
            start_pos=(750, 300),
            room_rect=matildastudy_ghost_room,
            image=ghost_img,
            group=camera
        )
    ]
    
    maingreat_ghost_room = pygame.Rect(0, 0, 1500, 900)  
    main_great_ghosts = [
        
    ]
    
    hallwayB_ghost_room = pygame.Rect(0, 0, 1896, 700)  
    hallwayB_ghosts = [
        
    ]
    
    living_ghost_room = pygame.Rect(0, 0, 1500, 900)  
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
        
    ]
    
    library_ghost_room = pygame.Rect(0, 0, 1500, 900)  
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
        
    ]
    
    game_ghost_room = pygame.Rect(0, 0, 1500, 900)  
    game_ghosts = [
        Ghost(
            start_pos=(250, 200),
            room_rect=game_ghost_room,
            image=ghost_img,
            group=camera 
        )
    ]
    
    lowergreat_ghost_room = pygame.Rect(0, 0, 1500, 900)  
    lower_great_ghosts = [
        Ghost(
            start_pos=(850, 100),
            room_rect=lowergreat_ghost_room,
            image=ghost_img,
            group=camera 
        )
    ]
    
    ball_ghost_room = pygame.Rect(0, 0, 1500, 1000)  
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
    
    uppergreat_ghost_room = pygame.Rect(0, 0, 1500, 900)  
    upper_great_ghosts = [
        
    ]
    
    hallwayD_ghost_room = pygame.Rect(0, 0, 3600, 700)  
    hallwayD_ghosts = [
        
    ]
    
    matilda_bed_ghost_room = pygame.Rect(0, 0, 1500, 1000)  
    matilda_bed_ghosts = [
    
    ]
    
    alfred_bed_ghost_room = pygame.Rect(0, 0, 1500, 1000)  
    alfred_bed_ghosts = [
    
    ]
    
    guest3_ghost_room = pygame.Rect(0, 0, 1500, 1000) 
    guest3_ghosts = [
        
    ]
    
    guest1_ghost_room = pygame.Rect(0, 0, 1500, 1000) 
    guest1_ghosts = [
        
    ]
    
    guest2_ghost_room = pygame.Rect(0, 0, 1500, 1000) 
    guest2_ghosts = [
        
    ]
    
    hallwayE_ghost_room = pygame.Rect(0, 0, 1896, 700) 
    hallwayE_ghosts = [
        
    ]
    
    guest4_ghost_room = pygame.Rect(0, 0, 1500, 1000) 
    guest4_ghosts = [
        
    ]
    
    frances_ghost_room = pygame.Rect(0, 0, 1500, 1000) 
    frances_ghosts = [
        
    ]
    
    hallwayF1_ghost_room = pygame.Rect(0, 0, 1909, 700) 
    hallwayF1_ghosts = [
        
    ]
    
    hallwayF2_ghost_room = pygame.Rect(0, 0, 1500, 1802) 
    hallwayF2_ghosts = [
        
    ]
    
    guest5_ghost_room = pygame.Rect(0, 0, 1500, 1000) 
    guest5_ghosts = [
        
    ]
    
    hallwayF3_ghost_room = pygame.Rect(0, 0, 1896, 700) 
    hallwayF3_ghosts = [
        
    ]
    
    dan_ghost_room = pygame.Rect(0, 0, 1500, 1000) 
    dan_ghosts = [
        
    ]
    
    
    
    
    # Ghosts dictionary
    ghosts = {
        "hallwayA_ghosts": hallwayA_ghosts,
        "dining_ghosts": dining_ghosts,
        "alfred_study_ghosts": alfred_study_ghosts,
        "matilda_study_ghosts": matilda_study_ghosts,
        "main_great_ghosts": main_great_ghosts,
        "hallwayB_ghosts": hallwayB_ghosts,
        "living_ghosts": living_ghosts,
        "hallwayC_ghosts": hallwayC_ghosts,
        "library_ghosts": library_ghosts,
        "lower_hallway_ghosts": lower_hallway_ghosts,
        "game_ghosts": game_ghosts,
        "lower_great_ghosts": lower_great_ghosts,
        "ballroom_ghosts": ballroom_ghosts,
        "upper_great_ghosts": upper_great_ghosts,
        "hallwayD_ghosts": hallwayD_ghosts,
        "matilda_bed_ghosts": matilda_bed_ghosts,
        "alfred_bed_ghosts": alfred_bed_ghosts,
        "guest3_ghosts": guest3_ghosts,
        "guest1_ghosts": guest1_ghosts,
        "guest2_ghosts": guest2_ghosts,
        "hallwayE_ghosts": hallwayE_ghosts,
        "guest4_ghosts": guest4_ghosts,
        "frances_ghosts": frances_ghosts,
        "hallwayF1_ghosts": hallwayF1_ghosts,
        "hallwayF2_ghosts": hallwayF2_ghosts,
        "guest5_ghosts": guest5_ghosts,
        "hallwayF3_ghosts": hallwayF3_ghosts,
        "dan_ghosts": dan_ghosts
    }
    
    return ghosts
    
    
