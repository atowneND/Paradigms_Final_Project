import pygame
import csv, math
from maps import Maps
from weapons import Weapons

class Ship(pygame.sprite.Sprite):
    def __init__(self, gs, ship_type, player):
        img = ship_type + "/ship" + player + ".png"
        settings = ship_type + "/settings" + player + ".csv"
        gridfile = ship_type + "/grid" + player + ".dat"
        self.player = player

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

        self.grid = Maps(self, grid_pos, gridfile)

        # resize
        scale_fac = float(self.settings['scale_fac'])
        self.size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(self.size[0]*scale_fac), int(self.size[1]*scale_fac)))

        ship_rect = self.image.get_rect()
        self.shield_rect = None
        if int(self.player) == 1:
            self.shield_rect = ship_rect.move(self.rect.x+30, self.rect.y)
        else:
            self.shield_rect = ship_rect.move(self.rect.x-30, self.rect.y)

        # shields
        self.shields = 3
        self.currentShield = 3
        # health
        self.health = 20
        # weapons
        weapon_name = "ion2.png"
        weapon_dir = "weapons/"+weapon_name
        self.weapon = Weapons(self, weapon_dir)
        # crew?

    def tick(self):
        self.gs.screen.blit(self.image, self.rect)
        # Health Icons
        for i in range(0, self.health):
            healthRect = pygame.Rect(self.rect.x + i*20, self.rect.y - 40, 15, 15)
            pygame.draw.rect(self.gs.screen, (0, 255, 0), healthRect, 0)

        # Shield Icons
        for i in range(0, self.shields):
            width = 0
            if i >= self.currentShield:
                width = 2
            shieldCircle = pygame.draw.circle(self.gs.screen, (0, 0, 255), (self.rect.x + i*30 + 10, self.rect.y - 10), 10, width)

        # Shield
        if self.currentShield != 0:
            angle1 = angle2 = 0
            if int(self.player) == 1:
                angle1 = math.pi*1.5
                angle2 = math.pi*2.5
            else:
                angle1 = math.pi*0.5
                angle2 = math.pi*1.5
            pygame.draw.arc(self.gs.screen, (0,0,255), self.shield_rect, angle1, angle2, self.currentShield)

        self.grid.tick()
        self.weapon.tick()

