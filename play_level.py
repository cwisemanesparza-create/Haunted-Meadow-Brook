import pygame
import pygame.freetype
import random, math
import os
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from random import randint

from global_variables import *
from load_scaled import *
from ui_elements import *

from game_state import *
from about import *
from achievements import *
from menu import *
from settings import *

from camera import *
from ghost import *
from player import *
from room import *
from collectible import *

# Start (play_level) screen
def play_level(screen):
    global current_direction, current_frame, frame_timer
    global walk_timer, walk_offset
    global door_sound, animation
    
    pygame.init()
    pygame.mixer.init()
    paused = False
    clock = pygame.time.Clock()
    collected_items = 0
    floating_texts = []
    rooms = {}
    
    door_sound = pygame.mixer.Sound("Sounds/door1.mp3")
    door_sound.set_volume(random.uniform(0.3, 0.6))
    
    animations = {
        "forward": [
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_forward.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_forward_left_foot.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_forward.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_forward_right_foot.png", PLAYER_SIZE),
        ],
        "back": [
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_back.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_back_left_foot.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_back.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_back_right_foot.png", PLAYER_SIZE),
        ],
        "left": [
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_left.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_left_left_foot.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_left.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_left_right_foot.png", PLAYER_SIZE),
        ],
        "right": [
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_right.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_right_left_foot.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_right.png", PLAYER_SIZE),
            load_scaled("photos/grizzly_photos/8-bit_grizz_face_right_right_foot.png", PLAYER_SIZE),
        ],
    }
    
    # Death Screen Animantion frames
    death_frames = []
    for i in range (1, 12):
        frame = load_scaled(f"photos/grizz_death/grizz death cutscene/bear jump scare animation{i}.png",
                            screen.get_size())
        death_frames.append(frame)
        animations["death"] = death_frames
    
    # Set initial room temporarily to get viewport
    temp_room = Room(
        "photos/background_photos/Hallway_Main_Floor_A_Update.png",
        (3600, 700),
        doors={},
        viewport=(1500, 700)
    )
    current_room = temp_room
    
    # Create camera
    camera_group = Camera(current_room.viewport)
    
    screen = pygame.display.set_mode(current_room.viewport)
    pygame.display.set_caption("Haunted Meadow Brook")
    
    # Load ghost image
    ghost_img = pygame.image.load("photos\\grizzly_photos\\grizzly_ghost.png").convert_alpha()
    ghost_img = pygame.transform.scale(ghost_img, (GHOST_SIZE))
    
    # Load Party Supplies image

    def random_position(room_size, margin=100):
        x = random.randint(margin, room_size[0] - margin)
        y = random.randint(margin, room_size[1] - margin)
        return (x, y)

    ps1_img = load_scaled("photos/party_supplies/Ps1.png", (80,80))
    ps2_img = load_scaled("photos/party_supplies/Ps2.png", (80,80))
    ps3_img = load_scaled("photos/party_supplies/Ps3.png", (80,80))
    ps4_img = load_scaled("photos/party_supplies/Ps4.png", (80,80))
    ps5_img = load_scaled("photos/party_supplies/Ps5.png", (80,80))

    hallway_collectibles = [
        Collectible(random_position((3600,700)), ps1_img, camera_group),
        Collectible(random_position((3600,700)), ps2_img, camera_group)
    ]
    dining_collectibles = [
        Collectible(random_position((1000,900)), ps3_img, camera_group)
    ]
    alfred_collectibles = [
        Collectible(random_position((900,900)), ps4_img, camera_group)
    ]
    matilda_collectibles = [
        Collectible(random_position((900,900)), ps5_img, camera_group)
    ]
    main_great_collectibles = [
        Collectible(random_position((1000,1250)), ps5_img, camera_group)
    ]
    living_room_collectibles = [
        Collectible(random_position((900,900)), ps5_img, camera_group)
    ]
    library_collectibles = [
        Collectible(random_position((900,900)), ps5_img, camera_group)
    ]
    
    
    # Create separate ghosts for each room
    hallwayA_ghost_room = pygame.Rect(0, 0, 3600, 700)
    hallwayA_ghosts = [
        Ghost(
            start_pos=(1200, 550),
            room_rect=hallwayA_ghost_room,
            image=ghost_img,
            group=camera_group  
        ),
        Ghost(
            start_pos=(1800, 150),
            room_rect=hallwayA_ghost_room,
            image=ghost_img,
            group=camera_group  
        ),
    ]
    dining_ghost_room = pygame.Rect(0, 0, 1000, 900)  
    dining_ghosts = [
        Ghost(
            start_pos=(150, 300),
            room_rect=dining_ghost_room,
            image=ghost_img,
            group=camera_group  
        ),
    ]
    alfredstudy_ghost_room = pygame.Rect(0, 0, 900, 900)  
    alfred_study_ghosts = [
        Ghost(
            start_pos=(250, 200),
            room_rect=alfredstudy_ghost_room,
            image=ghost_img,
            group=camera_group  
        )
    ]
    matildastudy_ghost_room = pygame.Rect(0, 0, 900, 900)  
    matilda_study_ghosts = [
        Ghost(
            start_pos=(250, 200),
            room_rect=matildastudy_ghost_room,
            image=ghost_img,
            group=camera_group  
        )
    ]
    maingreat_ghost_room = pygame.Rect(0, 0, 1000, 1100)  
    main_great_ghosts = [
        Ghost(
            start_pos=(900, 1000),
            room_rect=maingreat_ghost_room,
            image=ghost_img,
            group=camera_group  
        )
    ]
    living_ghost_room = pygame.Rect(0, 0, 900, 900)  
    living_room_ghosts = [
        Ghost(
            start_pos=(800, 200),
            room_rect=living_ghost_room,
            image=ghost_img,
            group=camera_group  
        )
    ]
    library_ghost_room = pygame.Rect(0, 0, 900, 900)  
    library_ghosts = [
        Ghost(
            start_pos=(800, 800),
            room_rect=library_ghost_room,
            image=ghost_img,
            group=camera_group  
        )
    ]
    
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
        ghosts=hallwayA_ghosts,
        collectibles=hallway_collectibles,
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
        ghosts=dining_ghosts,
        collectibles=dining_collectibles,
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
        ghosts=alfred_study_ghosts,
        collectibles=alfred_collectibles,
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
        ghosts=matilda_study_ghosts,
        collectibles=matilda_collectibles,
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
        ghosts=main_great_ghosts,
        collectibles=main_great_collectibles,
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
        ghosts=living_room_ghosts,
        collectibles=living_room_collectibles,
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
        ghosts=library_ghosts,
        collectibles=library_collectibles,
        viewport=(900, 700),
        respawn_pos=(175, 300)
    )
    
    # Room dictionary
    rooms = {
        "hallway_A": hallway_A,
        "dining_room": dining_room,
        "alfred_study": alfred_study,
        "matilda_study": matilda_study,
        "main_great_hall": main_great_hall,
        "living_room": living_room,
        "library": library
    }
    
    # Set initial current room
    current_room = hallway_A
    
    # Create player
    player = Player(
        image=animations["forward"][0],
        pos=(current_room.viewport[0] // 2, current_room.viewport[1] // 2),
        group=camera_group
    )
    
    player.dead = False
    player.death_finished = False
    player.death_frame = 0
    
    #PAUSE BUTTON
    pause_button = UIElement(
        center_position=(current_room.viewport[0] - 60, 40),
        text="II",
        font_size=26,
        bg_rgb=BLACK,
        text_rgb=WHITE,
        action="PAUSE"
    )
    
    # Buttons after Player Death
    retry_btn = UIElement((current_room.viewport[0]//2, current_room.viewport[1]//2 + 120), 
                          "Retry", 30, BLACK, WHITE, GameState.START)
    menu_btn = UIElement((current_room.viewport[0]//2, current_room.viewport[1]//2 + 190), 
                         "Main Menu", 30, BLACK, WHITE, GameState.MENU)
    
    # Define enter_room function
    def enter_room(room, spawn_pos):
        nonlocal player, current_room, pause_button, camera_group
        
        current_room = room
        player.rect.center = spawn_pos
        
        # push the player out of any door they happen to land in
        for info in room.doors.values():
            if player.rect.colliderect(info['rect']):
                player.rect.bottom = info['rect'].top - 1   # for example
        
        viewport_width, viewport_height = current_room.viewport
        screen = pygame.display.set_mode((viewport_width, viewport_height))
        pause_button.rects[0].center = (viewport_width - 60, 40)
        pause_button.rects[1].center = (viewport_width - 60, 40)
        
        camera_group.set_viewport(viewport_width, viewport_height)
        
        # Clamp camera to the new room, centred on the player
        camera_group.camera_rect.x = max(0, min(player.rect.centerx - viewport_width // 2, current_room.size[0] - viewport_width))
        camera_group.camera_rect.y = max(0, min(player.rect.centery - viewport_height // 2, current_room.size[1] - viewport_height))
        camera_group.offset.x = camera_group.camera_rect.x - camera_group.camera_borders["left"]
        camera_group.offset.y = camera_group.camera_rect.y - camera_group.camera_borders["top"]
    
    while True:
        dt = clock.tick(60)
        mouse_up = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = not paused
                return GameState.MENU
        
        if player.dead:
            player.death_frame_timer += dt
            
            if not player.death_finished:
                if player.death_frame_timer >= DEATH_FRAME_DELAY:
                    player.death_frame += 1
                    player.death_frame_timer = 0
                    
                    if player.death_frame >= len(animations["death"]):
                        player.death_frame = len(animations["death"]) - 1
                        player.death_finished = True
                        
            frame = pygame.transform.scale(animations["death"][player.death_frame], screen.get_size())
            screen.blit(frame, (0, 0))
            
            if player.death_finished:
                w, h = screen.get_size()

                retry_btn.rects[0].center = (w//2, h//2 + 120)
                retry_btn.rects[1].center = (w//2, h//2 + 120)

                menu_btn.rects[0].center = (w//2, h//2 + 190)
                menu_btn.rects[1].center = (w//2, h//2 + 190)

                action = retry_btn.update(pygame.mouse.get_pos(), mouse_up)
                retry_btn.draw(screen)

                action2 = menu_btn.update(pygame.mouse.get_pos(), mouse_up)
                menu_btn.draw(screen)

                if action == GameState.START:
                    # Reset player at the respawn position of current room
                    if current_room.respawn_pos == None:
                        player.reset((current_room.viewport[0] // 2, current_room.viewport[1] // 2))
                    else:
                        player.reset(current_room.respawn_pos)
                        
                    # Reset ghosts of current room
                    for ghost in current_room.ghosts:
                        ghost.reset()
                        
                    continue
                
                elif action2 == GameState.MENU:
                    return GameState.MENU
                
            pygame.display.update()
            continue
            
        # Update pause button
        action = pause_button.update(pygame.mouse.get_pos(), mouse_up)
        if action == "PAUSE":
            paused = not paused
            mouse_up = False
            
        # Draw pause overlay if paused
        if paused:
            overlay = pygame.Surface(current_room.viewport, pygame.SRCALPHA)
            overlay.fill(CLEAR)
            screen.blit(overlay, (0, 0))
            pause_text = create_surface_with_text("PAUSED", 48, WHITE, BLACK)
            screen.blit(
                pause_text, 
                pause_text.get_rect(center=(current_room.viewport[0]//2, current_room.viewport[1]//2))
            )
            
            # Buttons on pause screen
            pause_buttons = [
                UIElement((current_room.viewport[0]//2, current_room.viewport[1]//2 - 65), 
                          "Resume", 30, BLACK, WHITE, "RESUME"),
                UIElement((current_room.viewport[0]//2, current_room.viewport[1]//2 + 70), 
                          "Settings", 26, BLACK, WHITE, "SETTINGS"),
                UIElement((current_room.viewport[0]//2, current_room.viewport[1]//2 + 130), 
                          "Quit", 26, BLACK, WHITE, "QUIT"),
            ]
            
            for btn in pause_buttons:
                menu_action = btn.update(pygame.mouse.get_pos(), mouse_up)
                btn.draw(screen)
                
                if menu_action == "RESUME":
                    paused = False
                    mouse_up = False
                elif menu_action == "SETTINGS":
                    mouse_up = False
                    settings(screen, current_room.viewport[0], current_room.viewport[1], GameState.START)
                elif menu_action == "QUIT":
                    return GameState.MENU
            
        else:
            keys = pygame.key.get_pressed()
            moving = False

            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player.direction.x = -1
                current_direction = "left"
                moving = True
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player.direction.x = 1
                current_direction = "right"
                moving = True
            else:
                player.direction.x = 0
                
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player.direction.y = -1
                current_direction = "back"
                moving = True
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player.direction.y = 1
                current_direction = "forward"
                moving = True
            else:
                player.direction.y = 0

            if moving:
                frame_timer += dt
                walk_timer += dt

                if frame_timer >= FRAME_DELAY:
                    current_frame = (current_frame + 1) % 4
                    frame_timer = 0

                if walk_timer >= BOB_DELAY:
                    walk_offset = -BOB_AMOUNT if walk_offset == 0 else 0
                    walk_timer = 0
            else:
                current_frame = 0
                frame_timer = 0
                walk_offset = 0

            player.image = animations[current_direction][current_frame]
            for ghost in current_room.ghosts:
                ghost.update(dt, player)
                
            # Clamp player to room bounds
            player.rect.clamp_ip(current_room.bg_rect)
            player.update()
            
            # Check if player hits a door
            door_hit = current_room.get_door_at(player.rect)
            if door_hit:
                door_sound.play()  # play door sound
                enter_room(rooms[door_hit['target_room']], door_hit['spawn_pos'])
                
            camera_group.box_target_camera(player, current_room.size)
            camera_group.custom_draw(player, current_room)
          
            # COLLECTIBLE COLLISION
            for item in current_room.collectibles[:]:
                if player.rect.colliderect(item.rect):
                    item.collect()
                    current_room.collectibles.remove(item)
                    collected_items += 1
                    floating_texts.append(FloatingText("+1", item.rect.center))
                    print("Collected:", collected_items)
                    
            # ACHIEVEMENT CHECK
            if collected_items >= 10:
                achievements_data[1]["unlocked"] = True
            
            # Update floating text
            for ft in floating_texts[:]:
                if not ft.update():  
                    floating_texts.remove(ft)
                
                # Draw floating text

            for ft in floating_texts:
                ft.draw(screen)

        pause_button.draw(screen)
        pygame.display.update()