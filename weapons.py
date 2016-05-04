import pygame

class Weapons(pygame.sprite.Sprite):
    def __init__(self, ship, img):
        self.gs = ship.gs
        self.ship_player = int(ship.player)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()

        self.rect.x = ship.rect.x
        self.rect.y = self.gs.height - self.rect.height

        self.origin = ship.weapons_room # (x, y)
        self.firing_enabled = False
        self.target = self.origin

        self.duration = 400
        self.ctr = 0

    def tick(self):
        color = (255,50,0)
        self.gs.screen.blit(self.image, self.rect)
        if (self.ship_player==int(self.gs.player)):
            if self.rect.collidepoint(self.gs.mouse_pos):
                self.firing_enabled = True
            if (self.firing_enabled==True) and (self.target != self.origin):
                start = self.origin
                end = self.target
                width = 4
                pygame.draw.line(self.gs.screen, color, start, end, width)
                self.ctr += 1
                if self.ctr > self.duration:
                    self.firing_enabled = False
                    self.ctr = 0
                    self.target = self.origin
        elif (self.ship_player!=int(self.gs.player)) and (self.firing_enabled == True):
            start = self.origin
            end = self.target
            width = 4
            pygame.draw.line(self.gs.screen, color, start, end, width)
            self.ctr += 1
            if self.ctr > self.duration:
                self.firing_enabled = False
                self.ctr = 0
                self.target = self.origin
