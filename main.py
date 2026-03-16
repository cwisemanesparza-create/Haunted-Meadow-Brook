import pygame

from menu_screen import menu
from play_level import play_level
from settings_screen import settings
from achievements_screen import achievements
from about_screen import about

from global_variables_and_settings import MENU_SIZE


def main():

    pygame.init()

    screen = pygame.display.set_mode(MENU_SIZE)

    state = "MENU"

    while True:

        if state == "MENU":
            state = menu(screen)

        elif state == "START":
            state = play_level(screen)

        elif state == "SETTINGS":
            state = settings(screen)

        elif state == "ACHIEVEMENTS":
            state = achievements(screen)

        elif state == "ABOUT":
            state = about(screen)


if __name__ == "__main__":
    main()