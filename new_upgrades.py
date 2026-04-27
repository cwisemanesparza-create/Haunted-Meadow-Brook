import pygame

collected_items = 0

# BUY UPGRADE LOGIC

def buy_upgrade(upgrade_name, player):
    global collected_items

    upgrade = upgrades.get(upgrade_name)
    if not upgrade:
        return

    if upgrade["purchased"]:
        return

    if collected_items >= upgrade["cost"]:
        collected_items -= upgrade["cost"]
        upgrade["purchased"] = True
        apply_upgrade(upgrade_name, player)

# UPGRADE MENU UI

def open_upgrade_menu(screen, player):
    global collected_items

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)

    while True:
        mouse_up = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    return

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.fill((30, 30, 30))

        # Header
        header = font.render(f"Upgrades (Supplies: {collected_items})", True, (255,255,255))
        screen.blit(header, (50, 20))

        # Draw upgrades
        for i, key in enumerate(upgrades):
            upgrade = upgrades[key]

            x, y = 50, 80 + i * 80
            rect = pygame.Rect(x, y, 400, 60)

            color = (100, 255, 100) if upgrade["purchased"] else (200, 200, 200)
            pygame.draw.rect(screen, color, rect)

            text = font.render(f"{key} - Cost: {upgrade['cost']}", True, (0,0,0))
            screen.blit(text, (x + 10, y + 10))

            # Click detection
            if rect.collidepoint(pygame.mouse.get_pos()) and mouse_up:
                buy_upgrade(key, player)

        pygame.display.flip()
        clock.tick(60)

#OPTIONAL: RESET SYSTEM
def reset_upgrades():
    global upgrades, collected_items

    collected_items = 0

    for key in upgrades:
        upgrades[key]["purchased"] = False