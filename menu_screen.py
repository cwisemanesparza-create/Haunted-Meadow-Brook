from ui_button import UIElement
from global_variables_and_settings import *

def menu(screen):

    buttons = [
        UIElement((MENU_WIDTH/2, 300), "Start", 30, BLACK, WHITE, "START"),
        UIElement((MENU_WIDTH/2, 360), "Settings", 26, BLACK, WHITE, "SETTINGS"),
    ]

    while True:

        for button in buttons:
            action = button.update(pygame.mouse.get_pos())

            if action:
                return action