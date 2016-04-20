import pygame
from maps import Maps

class Ship(pygame.sprite.Sprite):
    def __init__(self, gs, img, grid):
        pygame.sprite.Sprite.__init__(self)

        self.gs = gs
        self.grid = grid

        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()

        # position
        self.rect.x = 30
        self.rect.y = 50

        # resize
        scale_fac = 0.6
        scale_fac = 1.5
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*scale_fac), int(self.size[1]*scale_fac)))

    def tick(self):
        self.gs.screen.blit(self.image, self.rect)
        self.grid.tick()

