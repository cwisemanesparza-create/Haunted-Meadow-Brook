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
from collectible import Collectible

# Party Supplies function
def party_supplies(load_scaled):
    
    # Load party supplies images
    ps1_img = load_scaled("photos/party_supplies/Ps1.png", (80,80))
    ps2_img = load_scaled("photos/party_supplies/Ps2.png", (80,80))
    ps3_img = load_scaled("photos/party_supplies/Ps3.png", (80,80))
    ps4_img = load_scaled("photos/party_supplies/Ps4.png", (80,80))
    ps5_img = load_scaled("photos/party_supplies/Ps5.png", (80,80))
    
    # Party Supplies images dictionary
    ps_images = {
        "ps1_img" : ps1_img,
        "ps2_img" : ps2_img,
        "ps3_img" : ps3_img,
        "ps4_img" : ps4_img,
        "ps5_img" : ps5_img 
    }
    
    return ps_images

# Collectibles Detailed function
def collectibles_detailed(images, camera):
    
    collect_images = ["ps1_img", "ps2_img", "ps3_img", "ps4_img", "ps5_img"]
    
    # Create separate collectibles for each room with randomly selected images
    hallwayA_collectibles = [
        Collectible(random_position((3600,700)), images[random.choice(collect_images)], camera),
        Collectible(random_position((3600,700)), images[random.choice(collect_images)], camera)
    ]
    dining_collectibles = [
        Collectible(random_position((1500,900)), images[random.choice(collect_images)], camera)
    ]
    alfred_study_collectibles = [
        Collectible(random_position((1500,900)), images[random.choice(collect_images)], camera)
    ]
    matilda_study_collectibles = [
        Collectible(random_position((1500,900)), images[random.choice(collect_images)], camera)
    ]
    main_great_collectibles = [
        Collectible(random_position((1500,1241)), images[random.choice(collect_images)], camera),
        Collectible(random_position((1500,1241)), images[random.choice(collect_images)], camera)
    ]
    hallwayB_collectibles = [
        Collectible(random_position((1896,700)), images[random.choice(collect_images)], camera),
    ]
    living_collectibles = [
        Collectible(random_position((1500,900)), images[random.choice(collect_images)], camera)
    ]
    hallwayC_collectibles = [
        Collectible(random_position((700,1850)), images[random.choice(collect_images)], camera),
    ]
    library_collectibles = [
        Collectible(random_position((1500,900)), images[random.choice(collect_images)], camera)
    ]
    lower_hallway_collectibles = [
        Collectible(random_position((3600,700)), images[random.choice(collect_images)], camera),
        Collectible(random_position((3600,700)), images[random.choice(collect_images)], camera)
    ]
    game_collectibles = [
        Collectible(random_position((1500,900)), images[random.choice(collect_images)], camera),
        Collectible(random_position((1500,900)), images[random.choice(collect_images)], camera)
    ]
    lower_great_collectibles = [
        Collectible(random_position((1500,1250)), images[random.choice(collect_images)], camera),
        Collectible(random_position((1500,1250)), images[random.choice(collect_images)], camera)
    ]
    ballroom_collectibles = [
        Collectible(random_position((1500,1000)), images[random.choice(collect_images)], camera),
        Collectible(random_position((1500,1000)), images[random.choice(collect_images)], camera)
    ]
    upper_great_collectibles = [
        Collectible(random_position((1500,1250)), images[random.choice(collect_images)], camera),
        Collectible(random_position((1500,1250)), images[random.choice(collect_images)], camera)
    ]
    hallwayD_collectibles = [
        Collectible(random_position((3600,700)), images[random.choice(collect_images)], camera),
        Collectible(random_position((3600,700)), images[random.choice(collect_images)], camera)
    ]
    matilda_bed_collectibles = [
        Collectible(random_position((1500,1000)), images[random.choice(collect_images)], camera)
    ]
    alfred_bed_collectibles = [
        Collectible(random_position((1500,1000)), images[random.choice(collect_images)], camera)
    ]
    
    guest3_collectibles = [
        Collectible(random_position((1500,1000)), images[random.choice(collect_images)], camera)
    ]
    
    guest1_collectibles = [
        Collectible(random_position((1500,1000)), images[random.choice(collect_images)], camera)
    ]
    
    guest2_collectibles = [
        Collectible(random_position((1500,1000)), images[random.choice(collect_images)], camera)
    ]
    
    hallwayE_collectibles = [
        Collectible(random_position((1896,700)), images[random.choice(collect_images)], camera),
        Collectible(random_position((1896,700)), images[random.choice(collect_images)], camera)
    ]
    
    guest4_collectibles = [
        Collectible(random_position((1500,1000)), images[random.choice(collect_images)], camera)
    ]
    
    frances_collectibles = [
        Collectible(random_position((1500,1000)), images[random.choice(collect_images)], camera)
    ]
    
    hallwayF1_collectibles = [
        Collectible(random_position((1909,700)), images[random.choice(collect_images)], camera)
    ]
    
    hallwayF2_collectibles = [
        Collectible(random_position((1000,1201)), images[random.choice(collect_images)], camera)
    ]
    
    guest5_collectibles = [
        Collectible(random_position((1500,1000)), images[random.choice(collect_images)], camera)
    ]
    
    hallwayF3_collectibles = [
        Collectible(random_position((1896,700)), images[random.choice(collect_images)], camera)
    ]
    
    dan_collectibles = [
        Collectible(random_position((1500,1000)), images[random.choice(collect_images)], camera)
    ]
    
    # Collectibles dictionary
    collectibles = {
        "hallwayA_collectibles": hallwayA_collectibles,
        "dining_collectibles": dining_collectibles,
        "alfred_study_collectibles": alfred_study_collectibles,
        "matilda_study_collectibles": matilda_study_collectibles,
        "main_great_collectibles": main_great_collectibles,
        "hallwayB_collectibles": hallwayB_collectibles,
        "living_collectibles": living_collectibles,
        "hallwayC_collectibles": hallwayC_collectibles,
        "library_collectibles": library_collectibles,
        "lower_hallway_collectibles": lower_hallway_collectibles,
        "game_collectibles": game_collectibles,
        "lower_great_collectibles": lower_great_collectibles,
        "ballroom_collectibles": ballroom_collectibles,
        "upper_great_collectibles": upper_great_collectibles,
        "hallwayD_collectibles": hallwayD_collectibles,
        "matilda_bed_collectibles": matilda_bed_collectibles,
        "alfred_bed_collectibles": alfred_bed_collectibles,
        "guest3_collectibles": guest3_collectibles,
        "guest1_collectibles": guest1_collectibles,
        "guest2_collectibles": guest2_collectibles,
        "hallwayE_collectibles": hallwayE_collectibles,
        "guest4_collectibles": guest4_collectibles,
        "frances_collectibles": frances_collectibles,
        "hallwayF1_collectibles": hallwayF1_collectibles,
        "hallwayF2_collectibles": hallwayF2_collectibles,
        "guest5_collectibles": guest5_collectibles,
        "hallwayF3_collectibles": hallwayF3_collectibles,
        "dan_collectibles": dan_collectibles
    }

    return collectibles
    
    
