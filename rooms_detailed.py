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
                'spawn_pos': (1300, 750) 
            },
            "hallwayA_to_alfred": {
                'rect': pygame.Rect(1525, 100, 25, 50), 
                'target_room': "alfred_study",
                'spawn_pos': (300, 750) 
            },
            "hallwayA_to_matilda": {
                'rect': pygame.Rect(2350, 100, 25, 50), 
                'target_room': "matilda_study",
                'spawn_pos': (300, 750) 
            },
            "hallwayA_to_maingreat": {
                'rect': pygame.Rect(3550, 425, 10, 50), 
                'target_room': "main_great_hall",
                'spawn_pos': (200, 525) 
            },
            "hallwayA_to_lower": {
                'rect': pygame.Rect(650, 100, 50, 25), 
                'target_room': "lower_hallway",
                'spawn_pos': (725, 300) 
            },
            "hallwayA_to_hallwayD": {
                'rect': pygame.Rect(900, 50, 100, 75), 
                'target_room': "hallway_D",
                'spawn_pos': (700, 300) 
            }
            
        },
        ghosts=ghosts["hallwayA_ghosts"],
        collectibles=collectibles["hallwayA_collectibles"],
        viewport=(1500, 700),
    )

    dining_room = Room(
        "photos/background_photos/Dining_Room.png",
        (1500, 900),
        doors={
            "dining_to_hallwayA": {
                'rect': pygame.Rect(1250, 850, 50, 60),  
                'target_room': "hallway_A",
                'spawn_pos': (250, 300)  
            }
        },
        ghosts=ghosts["dining_ghosts"],
        collectibles=collectibles["dining_collectibles"],
        viewport=(1500, 700),
        respawn_pos=(1300, 750)
    )
    
    alfred_study = Room(
        "photos/background_photos/Alfreds_Study.png",
        (1500, 900),
        doors={
            "alfred_to_hallwayA": {
                'rect': pygame.Rect(200, 850, 50, 60),  
                'target_room': "hallway_A",
                'spawn_pos': (1525, 300)  
            }
        },
        ghosts=ghosts["alfred_study_ghosts"],
        collectibles=collectibles["alfred_study_collectibles"],
        viewport=(1500, 700),
        respawn_pos=(300, 750)
    )
    
    matilda_study = Room(
        "photos/background_photos/Matildas_Study.png",
        (1500, 900),
        doors={
            "matilda_to_hallwayA": {
                'rect': pygame.Rect(200, 850, 50, 60),  
                'target_room': "hallway_A",
                'spawn_pos': (2350, 300)  
            }
        },
        ghosts=ghosts["matilda_study_ghosts"],
        collectibles=collectibles["matilda_study_collectibles"],
        viewport=(1500, 700),
        respawn_pos=(300, 750)
    )
    
    main_great_hall = Room(
        "photos/background_photos/Great_Hall.png",
        (1500, 1241),
        doors={
            "maingreat_to_hallwayA": {
                'rect': pygame.Rect(50, 525, 10, 50),  
                'target_room': "hallway_A",
                'spawn_pos': (3400, 400)  
            },
            "maingreat_to_hallwayB": {
                'rect': pygame.Rect(1450, 150, 10, 50),  
                'target_room': "hallway_B",
                'spawn_pos': (150, 450)  
            },
            "maingreat_to_lowergreat": {
                'rect': pygame.Rect(300, 1100, 100, 100),  
                'target_room': "lower_great_hall",
                'spawn_pos': (750, 1160)   
            },
            "maingreat_to_uppergreat": {
                'rect': pygame.Rect(1100, 1100, 100, 100),  
                'target_room': "upper_great_hall",
                'spawn_pos': (750, 1160)   
            }
        },
        ghosts=ghosts["main_great_ghosts"],
        collectibles=collectibles["main_great_collectibles"],
        viewport=(1500, 700),
        respawn_pos=(750, 1150)
    )
    
    hallway_B = Room(
        "photos/background_photos/Hallway_Main_Floor_B.png",
        (1896, 700),
        doors={
            "hallwayB_to_maingreat": {
                'rect': pygame.Rect(50, 425, 10, 50),  
                'target_room': "main_great_hall",
                'spawn_pos': (1350, 200)  
            },
            "hallwayC_to_living": {
                'rect': pygame.Rect(1846, 425, 10, 50),  
                'target_room': "living_room",
                'spawn_pos': (200, 300)  
            }
            
        },
        ghosts=ghosts["hallwayB_ghosts"],
        collectibles=collectibles["hallwayB_collectibles"],
        viewport=(1500, 700),
        respawn_pos=(150, 450)
    )
    
    living_room = Room(
        "photos/background_photos/Living_Room.png",
        (1500, 900),
        doors={
            "living_to_hallwayB": {
                'rect': pygame.Rect(50, 300, 10, 50),  
                'target_room': "hallway_B",
                'spawn_pos': (1746, 450)  
            },
            "living_to_hallwayC": {
                'rect': pygame.Rect(300, 850, 100, 15),  
                'target_room': "hallway_C",
                'spawn_pos': (350, 300)  
            }
        },
        ghosts=ghosts["living_ghosts"],
        collectibles=collectibles["living_collectibles"],
        viewport=(1500, 700),
        respawn_pos=(350, 300)
    )
    
    hallway_C = Room(
        "photos/background_photos/Hallway_Main_Floor_C_Update.png",
        (700, 1850),
        doors={
            "hallwayC_to_living": {
                'rect': pygame.Rect(340, 100, 25, 50),  
                'target_room': "living_room",
                'spawn_pos': (350, 750)  
            },
            "hallwayC_to_library": {
                'rect': pygame.Rect(340, 1800, 50, 15),  
                'target_room': "library",
                'spawn_pos': (275, 300)  
            }
            
        },
        ghosts=ghosts["hallwayC_ghosts"],
        collectibles=collectibles["hallwayC_collectibles"],
        viewport=(700, 700),
        respawn_pos=(350, 300)
    )
    
    library = Room(
        "photos/background_photos/Library.png",
        (1500, 900),
        doors={
            "library_to_hallwayC": {
                'rect': pygame.Rect(250, 100, 35, 50),  
                'target_room': "hallway_C",
                'spawn_pos': (350, 1700)  
            }
        },
        ghosts=ghosts["library_ghosts"],
        collectibles=collectibles["library_collectibles"],
        viewport=(1500, 700),
        respawn_pos=(275, 300)
    )
    
    lower_hallway = Room(
        "photos/background_photos/lower_floor_hallway.png",
        (3600, 700),
        doors={
            "lowerhallway_to_hallwayA": {
                'rect': pygame.Rect(700, 100, 25, 50),  
                'target_room': "hallway_A",
                'spawn_pos': (700, 300)  
            },
            "lowerhallway_to_game": {
                'rect': pygame.Rect(250, 100, 25, 50),  
                'target_room': "game_room",
                'spawn_pos': (1050, 750)  
            },
            "lowerhallway_to_lowergreat": {
                'rect': pygame.Rect(3550, 425, 10, 50), 
                'target_room': "lower_great_hall",
                'spawn_pos': (200, 525) 
            },
            "lowerhallway_to_ballroom": {
                'rect': pygame.Rect(1450, 650, 25, 10),  
                'target_room': "ballroom",
                'spawn_pos': (735, 300)  
            }
            
        },
        ghosts=ghosts["lower_hallway_ghosts"],
        collectibles=collectibles["lower_hallway_collectibles"],
        viewport=(1500, 700)
    )
    
    game_room = Room(
        "photos/background_photos/game_room.png",
        (1500, 900),
        doors={
            "game_to_lowerhallway": {
                'rect': pygame.Rect(950, 850, 50, 60),  
                'target_room': "lower_hallway",
                'spawn_pos': (250, 300)  
            }
        },
        ghosts=ghosts["game_ghosts"],
        collectibles=collectibles["game_collectibles"],
        viewport=(1500, 700),
        respawn_pos=(1050, 750)
    )
    
    lower_great_hall = Room(
        "photos/background_photos/Lower_Great_Hall.png",
        (1500, 1250),
        doors={
            "lowergreat_to_lowerhallway": {
                'rect': pygame.Rect(50, 525, 10, 50),  
                'target_room': "lower_hallway",
                'spawn_pos': (3400, 400)  
            },
            "lowergreat_to_maingreat": {
                'rect': pygame.Rect(300, 1110, 100, 100),  
                'target_room': "main_great_hall",
                'spawn_pos': (750, 1150)   
            }
        },
        ghosts=ghosts["lower_great_ghosts"],
        collectibles=collectibles["lower_great_collectibles"],
        viewport=(1500, 700),
        respawn_pos=(750, 1160)
    )
    
    ballroom = Room(
        "photos/background_photos/lower_floor_ballroom.png",
        (1500, 1000),
        doors={
            "ballroom_to_lowerhallway": {
                'rect': pygame.Rect(715, 100, 25, 50),  
                'target_room': "lower_hallway",
                'spawn_pos': (1400, 450)  
            }
        },
        ghosts=ghosts["ballroom_ghosts"],
        collectibles=collectibles["ballroom_collectibles"],
        viewport=(1280, 700),
        respawn_pos=(735, 300)
    )
    
    upper_great_hall = Room(
        "photos/background_photos/Upper_Great_Hall.png",
        (1500, 1250),
        doors={
            "uppergreat_to_maingreat": {
                'rect': pygame.Rect(1050, 1110, 100, 100),  
                'target_room': "main_great_hall",
                'spawn_pos': (750, 1150)   
            },
            "uppergreat_to_hallwayD": {
                'rect': pygame.Rect(50, 525, 10, 50),  
                'target_room': "hallway_D",
                'spawn_pos': (3400, 400)  
            },
            "uppergreat_to_hallwayE": {
                'rect': pygame.Rect(1450, 100, 10, 50),  
                'target_room': "hallway_E",
                'spawn_pos': (150, 450)  
            },
            "uppergreat_to_hallwayF": {
                'rect': pygame.Rect(1450, 350, 10, 50),  
                'target_room': "hallway_F",
                'spawn_pos': (150, 450)  
            }
        },
        ghosts=ghosts["upper_great_ghosts"],
        collectibles=collectibles["upper_great_collectibles"],
        viewport=(1500, 700),
        respawn_pos=(750, 1160)
    )
    
    hallway_D = Room(
        "photos/background_photos/Hallway_Upper_Floors_D.png",
        (3600, 700),
        doors={
            "hallwayD_to_matilda": {
                'rect': pygame.Rect(250, 100, 25, 50), 
                'target_room': "matilda_bedroom",
                'spawn_pos': (1300, 850) 
            },
            "hallwayD_to_hallwayA": {
                'rect': pygame.Rect(650, 100, 50, 25), 
                'target_room': "hallway_A",
                'spawn_pos': (925, 300) 
            },
            "hallwayD_to_alfred": {
                'rect': pygame.Rect(1100, 100, 25, 50), 
                'target_room': "alfred_bedroom",
                'spawn_pos': (300, 850) 
            },
            "hallwayD_to_guest3": {
                'rect': pygame.Rect(2350, 100, 25, 50), 
                'target_room': "guest_room_3",
                'spawn_pos': (300, 850) 
            },
            "hallwayD_to_guest1": {
                'rect': pygame.Rect(1100, 650, 50, 10), 
                'target_room': "guest_room_1",
                'spawn_pos': (200, 300) 
            },
            "hallwayD_to_guest2": {
                'rect': pygame.Rect(2350, 650, 50, 10), 
                'target_room': "guest_room_2",
                'spawn_pos': (200, 300) 
            },
            "hallwayD_to_uppergreat": {
                'rect': pygame.Rect(3550, 425, 10, 50), 
                'target_room': "upper_great_hall",
                'spawn_pos': (200, 525) 
            }
           
        },
        ghosts=ghosts["hallwayD_ghosts"],
        collectibles=collectibles["hallwayD_collectibles"],
        viewport=(1500, 700),
    )
    
    matilda_bedroom = Room(
        "photos/background_photos/Matildas_Room.png",
        (1500, 1000),
        doors={
            "matilda_to_hallwayD": {
                'rect': pygame.Rect(1250, 950, 50, 60),  
                'target_room': "hallway_D",
                'spawn_pos': (250, 300)  
            }
        },
        ghosts=ghosts["matilda_bed_ghosts"],
        collectibles=collectibles["matilda_bed_collectibles"],
        viewport=(1500, 700),
        respawn_pos=(1300, 850)
    )
    
    alfred_bedroom = Room(
        "photos/background_photos/Alfreds_Bedroom.png",
        (1500, 1000),
        doors={
            "alfred_to_hallwayD": {
                'rect': pygame.Rect(300, 950, 50, 60),  
                'target_room': "hallway_D",
                'spawn_pos': (1100, 300)  
            }
        },
        ghosts=ghosts["alfred_bed_ghosts"],
        collectibles=collectibles["alfred_bed_collectibles"],
        viewport=(1500, 700),
        respawn_pos=(300, 850)
    )
    
    guest_room_3 = Room(
        "photos/background_photos/Guest_Room_3.png",
        (1500, 1000),
        doors={
            "guest3_to_hallwayD": {
                'rect': pygame.Rect(200, 100, 50, 60),  
                'target_room': "hallway_D",
                'spawn_pos': (2350, 300)  
            }
        },
        ghosts=ghosts["guest3_ghosts"],
        collectibles=collectibles["guest3_collectibles"],
        viewport=(1500, 700),
        respawn_pos=(300, 850)
    )
    
    guest_room_1 = Room(
        "photos/background_photos/Guest_Room_1.png",
        (1500, 1000),
        doors={
            "guest1_to_hallwayD": {
                'rect': pygame.Rect(175, 100, 25, 50),  
                'target_room': "hallway_D",
                'spawn_pos': (1100, 450)  
            }
        },
        ghosts=ghosts["guest1_ghosts"],
        collectibles=collectibles["guest1_collectibles"],
        viewport=(1500, 700),
        respawn_pos=(200, 300)
    )
    
    guest_room_2 = Room(
        "photos/background_photos/Guest_Room_2.png",
        (1500, 1000),
        doors={
            "guest2_to_hallwayD": {
                'rect': pygame.Rect(175, 100, 25, 50),  
                'target_room': "hallway_D",
                'spawn_pos': (2350, 450)  
            }
        },
        ghosts=ghosts["guest2_ghosts"],
        collectibles=collectibles["guest2_collectibles"],
        viewport=(1500, 700),
        respawn_pos=(200, 300)
    )
    
    # Rooms dictionary
    rooms = {
        "hallway_A": hallway_A,
        "dining_room": dining_room,
        "alfred_study": alfred_study,
        "matilda_study": matilda_study,
        "main_great_hall": main_great_hall,
        "hallway_B": hallway_B,
        "living_room": living_room,
        "hallway_C": hallway_C,
        "library": library,
        "lower_hallway": lower_hallway,
        "game_room": game_room,
        "lower_great_hall": lower_great_hall,
        "ballroom": ballroom,
        "upper_great_hall": upper_great_hall,
        "hallway_D": hallway_D,
        "matilda_bedroom": matilda_bedroom,
        "alfred_bedroom": alfred_bedroom,
        "guest_room_3": guest_room_3,
        "guest_room_1": guest_room_1,
        "guest_room_2": guest_room_2
        
    }
    
    return rooms