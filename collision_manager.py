import pygame
class CollisionManager:

    def check_collectibles(self, player, collectibles):

        hits = pygame.sprite.spritecollide(player, collectibles, True)

        return len(hits)

    def check_ghosts(self, player, ghosts):

        if pygame.sprite.spritecollideany(player, ghosts):
            player.dead = True