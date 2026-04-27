import pygame

upgrades = {
    "speed": {
        "id": "speed",
        "name": "Extra Speed",
        "description": "Move faster.",
        "cost": 4,
        "purchased": False,
    },
    "slow_aura": {
        "id": "slow_aura",
        "name": "Slow Aura",
        "description": "Slows nearby ghosts.",
        "cost": 3,
        "purchased": False,
    },
    "shield": {
        "id": "shield",
        "name": "Shield",
        "description": "Extra hit before death, but slower movement.",
        "cost": 5,
        "purchased": False,
    },
    "dash": {
        "id": "dash",
        "name": "Dash",
        "description": "Press SHIFT to dash quickly.",
        "cost": 6,
        "purchased": False,
    },
}


def open_upgrade_menu(screen, player, collected_items):

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)

    while True:
        mouse_up = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return collected_items
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    return collected_items
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                mouse_up = True

        screen.fill((30, 30, 30))

        # Header
        header = font.render(
            f"Upgrades (Party Supplies: {collected_items})",
            True,
            (255, 255, 255),
        )
        screen.blit(header, (50, 20))

        # Draw upgrades
        for i, upgrade_name in enumerate(upgrades):
            upgrade = upgrades[upgrade_name]

            x, y = 50, 80 + i * 80
            color = (100, 255, 100) if upgrade["purchased"] else (200, 200, 200)

            rect = pygame.Rect(x, y, 400, 60)
            pygame.draw.rect(screen, color, rect)

            text = font.render(
                f"{upgrade['name']} - Cost: {upgrade['cost']}",
                True,
                (0, 0, 0),
            )
            screen.blit(text, (x + 10, y + 10))

            # Buy on click
            if rect.collidepoint(pygame.mouse.get_pos()) and mouse_up:
                collected_items = buy_upgrade(upgrade_name, player, collected_items)

        pygame.display.flip()
        clock.tick(60)

def buy_upgrade(upgrade_name, player, collected_items):

    upgrade = upgrades[upgrade_name]

    if upgrade["purchased"]:
        return collected_items

    if collected_items >= upgrade["cost"]:
        #collected_items -= upgrade["cost"]
        upgrade["purchased"] = True

        # Apply effect
        if upgrade_name == "speed":
            player.speed += 0.5
        elif upgrade_name == "slow_aura":
            player.slow_aura = True
        elif upgrade_name == "shield":
            player.extra_hits += 1
            player.speed -= 1
        elif upgrade_name == "dash":
            player.can_dash = True
            
    return collected_items