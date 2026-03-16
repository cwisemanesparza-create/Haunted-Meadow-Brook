import pygame

from ui_button import UIElement
from global_variables_and_settings import *


def achievements_screen(screen):

    clock = pygame.time.Clock()

    font_title = pygame.font.Font(None, 60)
    font_text = pygame.font.Font(None, 32)

    back_button = UIElement(
        center_position=(750, 560),
        text="BACK",
        font_size=40,
        bg_rgb=(50,50,50),
        text_rgb=WHITE,
        action="MENU"
    )

    achievements = [
        "First Escape",
        "Collected 5 Items",
        "Avoided a Ghost",
        "Finished the Game"
    ]

    while True:

        mouse_pos = pygame.mouse.get_pos()
        mouse_up = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_up = True

        screen.fill((20,20,20))

        title = font_title.render("Achievements", True, WHITE)
        screen.blit(title, (620,120))

        y = 250

        for achievement in achievements:

            text = font_text.render(achievement, True, WHITE)
            screen.blit(text, (620,y))
            y += 50

        action = back_button.update(mouse_pos, mouse_up)

        back_button.draw(screen)

        if action:
            return action

        pygame.display.flip()
        clock.tick(60)