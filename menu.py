import pygame
import pygame.freetype 
from pygame.sprite import Sprite
from pygame.rect import Rect
from enum import Enum


BLACK = (0, 0, 0)
ORANGE = (255, 140, 0)

def create_surface_with_text(text, font_size, text_rgb, bg_rgb):
    #returns surface with text
    font = pygame.freetype.SysFont("Courier", font_size, bold=True)
    surface, _ = font.render(text=text, fgcolor=text_rgb, bgcolor=bg_rgb)
    return surface.convert_alpha()

class UIElement(Sprite):
    #interface Element

    def __init__(self, center_position, text, font_size, bg_rgb, text_rgb action=None):
        super().__init__()
    
    #center_position - tuple (x, y)
    #text - string of text to write
    #font_size - int
    #bg_rgb (background colour) - tuple (r, g, b)
    #text_rgb (text colour) - tuple (r, g, b)
        self.action = action
        self.mouse_over = False

    #image
        default_image = create_surafce_with_text(
            text=text, 
            font_size=font_size,
            text_rgb=text_rgb,
            bg_rgb=bg_rgb
    )
     # create the image that shows when mouse is over the element
        highlighted_image = create_surface_with_text(
            text=text,
            font_size=int(font_size * 1.2),
            text_rgb=text_rgb,
            bg_rgb=bg_rgb
        )

    # add both images and their rects to lists
        self.images = [default_image, highlighted_image]
        self.rects = [
            default_image.get_rect(center=center_position),
            highlighted_image.get_rect(center=center_position),
        ]

    @property
    def image(self):
    return self.images[1] if self.mouse_over else self.images[0]

    @property
    def rect(self):
    return self.rects[1] if self.mouse_over else self.rects[0]        return self.rects[1] if self.mouse_over else self.rects[0]

    def update(self, mouse_pos):
    if self.rect.collidepoint(mouse_pos):
        self.mouse_over = True
    else:
        self.mouse_over = False

    def draw(self, surface):
    # draws element on surface
    surface.blit(self.image, self.rect)

    def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))

    # create a ui element
    uielement = UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Hello World",
    )

    # main loop
    while True:
        for event in pygame.event.get():
            pass
        screen.fill(ORANGE)

        uielement.update(pygame.mouse.get_pos())
        uielement.draw(screen)
        pygame.display.flip()


    # call main when the script is run
    if __name__ == "__main__":
    main()

    def update(self, mouse_pos, mouse_up):
    """ Updates the element's appearance depending on the mouse position
        and returns the button's action if clicked.
    """
    if self.rect.collidepoint(mouse_pos):
        self.mouse_over = True
        if mouse_up:
            return self.action
    else:
        self.mouse_over = False
    
    class GameState(Enum):
    QUIT = -1

    def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))

    quit_btn = UIElement(
        center_position=(400, 500),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,
    )

    # main loop
    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BLUE)

        ui_action = quit_btn.update(pygame.mouse.get_pos(), mouse_up)
        if ui_action is not None:
            return
        quit_btn.draw(screen)
        pygame.display.flip()

        class GameState(Enum):
        QUIT = -1
        TITLE = 0
        NEWGAME = 1

        def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    game_state = GameState.TITLE

    while True:
        if game_state == GameState.TITLE:
            game_state = title_screen(screen)

        if game_state == GameState.NEWGAME:
            game_state = play_level(screen)

        if game_state == GameState.QUIT:
            pygame.quit()
            return
    
    def title_screen(screen):
    start_btn = UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Start",
        action=GameState.NEWGAME,
    )
    quit_btn = UIElement(
        center_position=(400, 500),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,
    )

    buttons = [start_btn, quit_btn]

    while True:
        mouse_up = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True
        screen.fill(BLUE)

        for button in buttons:
            ui_action = button.update(pygame.mouse.get_pos(), mouse_up)
            if ui_action is not None:
                return ui_action
            button.draw(screen)

        pygame.display.flip()

        def title_screen(screen):
    start_btn = UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Start",
        action=GameState.NEWGAME,
    )
    quit_btn = UIElement(
        center_position=(400, 500),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Quit",
        action=GameState.QUIT,
    )

    buttons = RenderUpdates(start_btn, quit_btn)

    return game_loop(screen, buttons)

    def play_level(screen, player):
    return_btn = UIElement(
        center_position=(140, 570),
        font_size=20,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text="Return to main menu",
        action=GameState.TITLE,
    )

    nextlevel_btn = UIElement(
        center_position=(400, 400),
        font_size=30,
        bg_rgb=BLUE,
        text_rgb=WHITE,
        text=f"Next level ({player.current_level + 1})",
        action=GameState.NEXT_LEVEL,
    )

    buttons = RenderUpdates(return_btn, nextlevel_btn)

    return game_loop(screen, buttons)

