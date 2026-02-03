import pygame
pygame.init()
pygame.display.set_caption("Haunted Meadow Brook") #title of game

#set width and height of window
width = 1000
height = 750
win = pygame.display.set_mode((width, height))

#load grizzly mascot player
player = pygame.image.load("photos\\grizzly_photos\\grizzly_mascot_pixel.png")
player_rect = player.get_rect(center = (0, 0)) #player starts at (x, y)
player = pygame.transform.scale(player, (150, 200)) #player scale to size (x, y)
vel = 10 #set velocity of player movement

#run game
run = True
while run:
    pygame.time.delay(100)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
    #left, right, up, down movement based on keys pressed
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_rect.x -= vel
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_rect.x += vel
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_rect.y -= vel 
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_rect.y += vel
        
    #keep player inside edges of window
    if player_rect.right > width:
        player_rect.right = width
    if player_rect.left < 0:
        player_rect.left = 0
    if player_rect.bottom > height:
        player_rect.bottom = height
    if player_rect.top < 0:
        player_rect.top = 0
    
    win.fill((0,0,0))  
    win.blit(player, player_rect)     
    pygame.display.update()

pygame.quit()