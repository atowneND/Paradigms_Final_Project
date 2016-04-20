import pygame
import csv
from maps import Maps

class Ship(pygame.sprite.Sprite):
    def __init__(self, gs, ship_type):
        img = ship_type + "/ship.png"
        settings = ship_type + "/settings.csv"
        gridfile = ship_type + "/grid.dat"
        pygame.sprite.Sprite.__init__(self)
        with open(settings) as f:
            data = csv.DictReader(f)
            for s in data:
                self.settings = s

        self.gs = gs
        self.grid = Maps(self.gs, gridfile)

        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()

        # position
        self.rect.x = int(self.settings['x'])
        self.rect.y = int(self.settings['y'])

        # resize
        scale_fac = float(self.settings['scale_fac'])
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*scale_fac), int(self.size[1]*scale_fac)))

    def tick(self):
        self.gs.screen.blit(self.image, self.rect)
        self.grid.tick()

