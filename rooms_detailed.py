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
from room import Room

# Rooms Detailed function
def rooms_detailed(ghosts, collectibles):
    
    # Create rooms with their own ghosts
    hallway_A = Room(
        "photos/background_photos/Hallway_Main_Floor_A_Update.png",
        (3600, 700),
        doors={
            "hallwayA_to_dining": {
                'rect': pygame.Rect(250, 100, 25, 50), 
                'target_room': "dining_room",
                'spawn_pos': (850, 750) 
            },
            "hallwayA_to_alfred": {
                'rect': pygame.Rect(1525, 100, 25, 50), 
                'target_room': "alfred_study",
                'spawn_pos': (200, 750) 
            },
            "hallwayA_to_matilda": {
                'rect': pygame.Rect(2350, 100, 25, 50), 
                'target_room': "matilda_study",
                'spawn_pos': (200, 750) 
            },
            "hallwayA_to_maingreat": {
                'rect': pygame.Rect(3550, 425, 10, 50), 
                'target_room': "main_great_hall",
                'spawn_pos': (200, 525) 
            }
        },
        ghosts=ghosts["hallwayA_ghosts"],
        collectibles=collectibles["hallwayA_collectibles"],
        viewport=(1500, 700),
    )

    dining_room = Room(
        "photos/background_photos/Dining_Room.png",
        (1000, 900),
        doors={
            "dining_to_hallwayA": {
                'rect': pygame.Rect(900, 850, 50, 60),  
                'target_room': "hallway_A",
                'spawn_pos': (250, 300)  
            }
        },
        ghosts=ghosts["dining_ghosts"],
        collectibles=collectibles["dining_collectibles"],
        viewport=(1000, 700),
        respawn_pos=(850, 750)
    )
    
    alfred_study = Room(
        "photos/background_photos/Alfreds_Study.png",
        (900, 900),
        doors={
            "alfred_to_hallwayA": {
                'rect': pygame.Rect(100, 850, 50, 60),  
                'target_room': "hallway_A",
                'spawn_pos': (1525, 300)  
            }
        },
        ghosts=ghosts["alfred_study_ghosts"],
        collectibles=collectibles["alfred_study_collectibles"],
        viewport=(900, 700),
        respawn_pos=(200, 750)
    )
    
    matilda_study = Room(
        "photos/background_photos/Matildas_Study.png",
        (900, 900),
        doors={
            "matilda_to_hallwayA": {
                'rect': pygame.Rect(100, 850, 50, 60),  
                'target_room': "hallway_A",
                'spawn_pos': (2350, 300)  
            }
        },
        ghosts=ghosts["matilda_study_ghosts"],
        collectibles=collectibles["matilda_study_collectibles"],
        viewport=(900, 700),
        respawn_pos=(200, 750)
    )
    
    main_great_hall = Room(
        "photos/background_photos/Great_Hall.png",
        (1000, 1250),
        doors={
            "maingreat_to_hallwayA": {
                'rect': pygame.Rect(50, 525, 10, 50),  
                'target_room': "hallway_A",
                'spawn_pos': (3400, 400)  
            },
            "maingreat_to_living": {
                'rect': pygame.Rect(950, 150, 10, 50),  
                'target_room': "living_room",
                'spawn_pos': (200, 300)  
            }
        },
        ghosts=ghosts["main_great_ghosts"],
        collectibles=collectibles["main_great_collectibles"],
        viewport=(1000, 700),
        respawn_pos=(250, 1150)
    )
    
    living_room = Room(
        "photos/background_photos/Living_Room.png",
        (900, 900),
        doors={
            "living_to_maingreat": {
                'rect': pygame.Rect(50, 300, 10, 50),  
                'target_room': "main_great_hall",
                'spawn_pos': (750, 250)  
            },
            "living_to_library": {
                'rect': pygame.Rect(250, 850, 50, 15),  
                'target_room': "library",
                'spawn_pos': (175, 300)  
            }
        },
        ghosts=ghosts["living_ghosts"],
        collectibles=collectibles["living_collectibles"],
        viewport=(900, 700),
        respawn_pos=(300, 550)
    )
    
    library = Room(
        "photos/background_photos/Library.png",
        (900, 900),
        doors={
            "library_to_living": {
                'rect': pygame.Rect(175, 100, 25, 50),  
                'target_room': "living_room",
                'spawn_pos': (225, 750)  
            }
        },
        ghosts=ghosts["library_ghosts"],
        collectibles=collectibles["library_collectibles"],
        viewport=(900, 700),
        respawn_pos=(175, 300)
    )
    
    # Rooms dictionary
    rooms = {
        "hallway_A": hallway_A,
        "dining_room": dining_room,
        "alfred_study": alfred_study,
        "matilda_study": matilda_study,
        "main_great_hall": main_great_hall,
        "living_room": living_room,
        "library": library
    }
    
    return rooms