import pygame
from enum import Enum

from ui_elements import *
from global_variables import *

# Game State class
class GameState(Enum):
    MENU = 0
    START = 1
    SETTINGS = 2
    ACHIEVEMENTS = 3
    ABOUT = 4
    PAUSED = 5
    QUIT = -1
