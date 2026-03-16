from menu_screen import menu_screen
from play_level import play_level
from settings_screen import settings_screen

class Game:

    def __init__(self, screen):
        self.screen = screen
        self.state = "MENU"

    def run(self):

        while True:

            if self.state == "MENU":
                self.state = menu_screen(self.screen)

            elif self.state == "PLAY":
                self.state = play_level(self.screen)

            elif self.state == "SETTINGS":
                self.state = settings_screen(self.screen)