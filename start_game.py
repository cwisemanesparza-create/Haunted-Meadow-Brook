import pygame
pygame.init()

win = pygame.display.set_mode((1000, 750))

pygame.display.set_caption("Haunted Meadow Brook")

player_image = pygame.image.load("photos\\grizzly_photos\\grizzly_mascot_pixel.png")

player_rect = player_image.get_rect(center = (350, 350))

x = 50
y = 50
width = 40
height = 60
vel = 10

run = True

while run:
    pygame.time.delay(100)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_rect.x -= vel
        
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_rect.x += vel
        
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_rect.y -= vel
        
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_rect.y += vel
    
    win.fill((0,0,0))  
    win.blit(player_image, player_rect)     
    pygame.display.update()

pygame.quit()