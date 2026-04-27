import pygame

# Menu Width, Height, Size
MENU_WIDTH = 1500
MENU_HEIGHT = 670
MENU_SIZE = (MENU_WIDTH, MENU_HEIGHT)

# Viewport Width, Height, Size
MAX_VIEWPORT_WIDTH = 1500
MAX_VIEWPORT_HEIGHT = 850
MAX_VIEWPORT_SIZE = (MAX_VIEWPORT_WIDTH, MAX_VIEWPORT_HEIGHT)

# Player and Ghost size
PLAYER_SIZE = (150, 190)
GHOST_SIZE = (80, 100)

# Colors
CLEAR = (0, 0, 0, 0) # transparent
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)

# Global volume values
MASTER_VOLUME = 0.8
MUSIC_VOLUME = 0.6

# Global player movement
SPEED = 6
BOB_DELAY = 120
BOB_AMOUNT = 3
FRAME_DELAY = 110

# Death Animation timers
FRAME_DELAY = 110
DEATH_FRAME_DELAY = 300

# Vacuum draw size and offsets
VACUUM_DRAW_SIZE = (64, 29)
VACUUM_OFFSETS = {
    "right": (82, 88),
    "left": (4, 88),
    "forward": (43, 118),
    "back": (45, 80),
}

# Key and Cabinet image path
KEY_IMAGE_PATH = "photos/background_photos/cabinet variations and key/Key.png"
LOCKED_CABINET_IMAGE_PATH = "photos/background_photos/cabinet variations and key/LOCKED cabinet with vacuum.png"
EMPTY_CABINET_IMAGE_PATH = "photos/background_photos/cabinet variations and key/cabinet (NO VACUUM).png"

# Key and Cabinet draw size
KEY_DRAW_SIZE = (54, 32)
CABINET_DRAW_SIZE = (92, 122)