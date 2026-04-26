import pygame
import pygame.freetype
import random, math
import os
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum
from random import randint

from global_variables import *
from other_functions import *
from ui_elements import *

from game_state import *
from about import *
from achievements import *
from menu import *
from settings import *

from camera import *
from player import *
from collectible import *
from collectibles_detailed import *
from ghost import *
from ghosts_detailed import *
from room import *
from rooms_detailed import *

from cabinet_vacuum import*

# Note: run main.py file to open game, play_level is the game after menu

def spawn_key_in_random_room(rooms, camera_group, key_surface):
    possible_rooms = ["library", "game_room", "living_room", "dining_room", "main_great_hall"]
    room_name = random.choice(possible_rooms)
    room = rooms[room_name]
    key_item = Collectible(random_position(room.size, margin=120), key_surface, camera_group)
    key_item.is_key = True
    key_item.room_name = room_name
    room.collectibles.append(key_item)
    return key_item, room_name

# Play Level screen (START Game State)
def play_level(screen):
    global current_direction, current_frame, frame_timer
    global walk_timer, walk_offset
    global door_sound
    
    pygame.init()
    pygame.mixer.init()
    paused = False
    clock = pygame.time.Clock()
    collected_items = 0
    floating_texts = []
    rooms = {}
    
    # Load door sound
    door_sound = pygame.mixer.Sound("Sounds/door1.mp3")
    door_sound.set_volume(random.uniform(0.3, 0.6))
    
    # Load animations from animation images
    animations = animation_images(load_scaled)
    
    # Death Screen Animantion frames
    death_frames = []
    for i in range (1, 12):
        frame = load_scaled(f"photos/grizz_death/grizz death cutscene/bear jump scare animation{i}.png",
                            screen.get_size())
        death_frames.append(frame)
        animations["death"] = death_frames
    
    # Set initial room temporarily to get viewport
    temp_room = Room(
        "photos/background_photos/Great_Hall.png",
        (1500, 1241),
        doors={},
        viewport=(1500, 700)
    )
    current_room = temp_room
    
    # Create camera
    camera_group = Camera(current_room.viewport)
    
    screen = pygame.display.set_mode(current_room.viewport)
    pygame.display.set_caption("Haunted Meadow Brook")
    
    # Load party supplies images
    ps_images = party_supplies(load_scaled)
    
    # Create collectibles with party supplies images and camera
    collectibles = collectibles_detailed(ps_images, camera_group)
    
    # Load ghost image
    ghost_img = pygame.image.load("photos\\grizzly_photos\\grizzly_ghost.png").convert_alpha()
    ghost_img = pygame.transform.scale(ghost_img, (GHOST_SIZE))
    
    # Create ghosts with ghost image and camera
    ghosts = ghosts_detailed(ghost_img, camera_group)
    
    # Create rooms with ghosts and collectibles
    rooms = rooms_detailed(ghosts, collectibles)
    
    key_surface = create_key_surface()
    vacuum_img = load_vacuum_surface()
    key_item, key_room_name = spawn_key_in_random_room(rooms, camera_group, key_surface)
    cabinet_room_name = "library"
    opened_cabinet_img = load_opened_cabinet_surface()
    cabinet = Cabinet((720, 620), create_cabinet_surface(False, False), opened_cabinet_img)
    all_room_ghosts = {room_name: room.ghosts[:] for room_name, room in rooms.items()}
    
    # Set initial current room
    current_room = rooms["main_great_hall"]
    
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
    
    while True:
        dt = clock.tick(60)
        mouse_up = False
        interact_pressed = False
        capture_pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused = not paused
                return GameState.MENU
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                interact_pressed = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                capture_pressed = True
        
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
                        
                    for room_name, room_ghosts in all_room_ghosts.items():
                        rooms[room_name].ghosts = room_ghosts[:]
                        # Reset ghosts for the retry so captured or capturing ghosts are restored.
                        for ghost in rooms[room_name].ghosts:
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
            for ghost in current_room.ghosts[:]:
                ghost.update(dt, player)
                if ghost.captured:
                    current_room.ghosts.remove(ghost)
                    ghost.kill()
                    floating_texts.append(
                        FloatingText(
                            "Ghost captured!",
                            screen_pos_from_world(player.rect.midtop, camera_group),
                            color=(160, 220, 255)
                        )
                    )
                
            # Clamp player to room bounds
            player.rect.clamp_ip(current_room.bg_rect)
            player.update()
            
            if interact_pressed and current_room == rooms[cabinet_room_name]:
                if cabinet.rect.inflate(40, 40).colliderect(player.rect):
                    if player.has_vacuum:
                        pass
                    elif not player.has_key:
                        floating_texts.append(
                            FloatingText(
                                "Need a key",
                                screen_pos_from_world(cabinet.rect.midtop, camera_group),
                                color=(255, 210, 90)
                            )
                        )
                    else:
                        cabinet.open()
                        player.has_vacuum = True
                        floating_texts.append(
                            FloatingText(
                                "Cabinet unlocked",
                                screen_pos_from_world(cabinet.rect.midtop, camera_group),
                                color=(120, 255, 140)
                            )
                        )
                        floating_texts.append(
                            FloatingText(
                                "Vacuum acquired!",
                                screen_pos_from_world(player.rect.midtop, camera_group),
                                color=(160, 220, 255)
                            )
                        )

            if capture_pressed and player.has_vacuum:
                nearest_ghost = get_nearby_capturable_ghost(player, current_room.ghosts)
                if nearest_ghost is not None:
                    nearest_ghost.start_capture(player)
            
            # Check if player hits a door
            door_hit = current_room.get_door_at(player.rect)
            if door_hit:
                door_sound.play()  # play door sound
                current_room = enter_room(player, pause_button, camera_group, rooms[door_hit['target_room']], door_hit['spawn_pos'])
                #enter_room(rooms[door_hit['target_room']], door_hit['spawn_pos'])
                
            camera_group.box_target_camera(player, current_room.size)
            camera_group.custom_draw(player, current_room)
            
            if current_room == rooms[cabinet_room_name]:
                cabinet.draw(screen, camera_group.offset)
                
            if player.has_vacuum:
                draw_vacuum(screen, player, camera_group.offset, current_direction, vacuum_img)

            prompt_text = None
            near_cabinet = current_room == rooms[cabinet_room_name] and cabinet.rect.inflate(40, 40).colliderect(player.rect)
            if near_cabinet and not player.has_vacuum:
                if player.has_key:
                    prompt_text = "Press E to unlock cabinet"
                else:
                    prompt_text = "Need a key"
            elif player.has_vacuum and get_nearby_capturable_ghost(player, current_room.ghosts) is not None:
                prompt_text = "Press SPACE to capture ghost"

            if prompt_text is not None:
                draw_prompt(screen, prompt_text)

            # COLLECTIBLE COLLISION
            for item in current_room.collectibles[:]:
                if player.rect.colliderect(item.rect):
                    item.collect()
                    current_room.collectibles.remove(item)
                    if getattr(item, "is_key", False):
                        player.has_key = True
                        floating_texts.append(
                            FloatingText(
                                "Key collected!",
                                screen_pos_from_world(item.rect.center, camera_group),
                                color=(255, 225, 80)
                            )
                        )
                    else:
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