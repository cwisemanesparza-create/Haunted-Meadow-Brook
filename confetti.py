import pygame
import random

# Initialize
pygame.init()
WIDTH, HEIGHT = 1500, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

background_img = pygame.image.load(f"photos/win_screen_photos/bear_celebration_1.png",).convert()
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

class Confetti():
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, 0)
        self.size = random.randint(5, 10)
        self.speed = random.randint(3, 6)
        self.color = random.choice(colors)

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-20, -1)
            self.x = random.randint(0, WIDTH)

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
