import pygame
import csv
from maps import Maps

class Ship(pygame.sprite.Sprite):
    def __init__(self, gs, ship_type, player):
        img = ship_type + "/ship" + player + ".png"
        settings = ship_type + "/settings" + player + ".csv"
        gridfile = ship_type + "/grid" + player + ".dat"
        pygame.sprite.Sprite.__init__(self)
        with open(settings) as f:
            data = csv.DictReader(f)
            for s in data:
                self.settings = s

        self.gs = gs

        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()

        # position
        self.rect.x = int(self.settings['x'])
        self.rect.y = int(self.settings['y'])

        grid_pos = (0,0)
        if ship_type == "cruiser":
            grid_pos = (self.rect.x+70, self.rect.y+50)
        else:
            grid_pos = (self.rect.x+100, self.rect.y+50)

        self.grid = Maps(self.gs, grid_pos, gridfile)
        
        # resize
        scale_fac = float(self.settings['scale_fac'])
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*scale_fac), int(self.size[1]*scale_fac)))

        # shields
        # weapons
        # health
        # crew?

    def tick(self):
        self.gs.screen.blit(self.image, self.rect)
        self.grid.tick()

