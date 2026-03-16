import pygame

from ui_button import UIElement
from global_variables_and_settings import *


def about_screen(screen):

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

    while True:

        mouse_pos = pygame.mouse.get_pos()
        mouse_up = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_up = True

        screen.fill((25,25,25))

        title = font_title.render("Haunted Meadow Brook", True, WHITE)
        screen.blit(title, (520,120))

        text_lines = [
            "A top-down exploration horror game",
            "",
            "Created for a college Python project",
            "",
            "Explore rooms",
            "Collect objects",
            "Avoid ghosts",
        ]

        y = 220

        for line in text_lines:

            text = font_text.render(line, True, WHITE)
            screen.blit(text, (550,y))
            y += 40

        action = back_button.update(mouse_pos, mouse_up)

        back_button.draw(screen)

        if action:
            return action

        pygame.display.flip()
        clock.tick(60)