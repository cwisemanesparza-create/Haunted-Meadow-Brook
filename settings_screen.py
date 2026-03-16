import pygame

from ui_slider import Slider
from ui_button import UIElement
from global_variables_and_settings import *


def settings_screen(screen):

    clock = pygame.time.Clock()

    master_slider = Slider((600, 300), (300, 20), "Master Volume", MASTER_VOLUME)
    music_slider = Slider((600, 380), (300, 20), "Music Volume", MUSIC_VOLUME)

    back_button = UIElement(
        center_position=(750, 520),
        text="BACK",
        font_size=40,
        bg_rgb=(50,50,50),
        text_rgb=WHITE,
        action="MENU"
    )

    while True:

        mouse_pos = pygame.mouse.get_pos()
        mouse_up = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_up = True

            master_slider.handle_event(event)
            music_slider.handle_event(event)

        screen.fill((30,30,30))

        master_slider.draw(screen)
        music_slider.draw(screen)

        action = back_button.update(mouse_pos, mouse_up)

        back_button.draw(screen)

        if action:
            return action

        pygame.display.flip()
        clock.tick(60)