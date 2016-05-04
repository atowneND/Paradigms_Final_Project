import pygame

class Weapons(pygame.sprite.Sprite):
    def __init__(self, ship, img):
        self.gs = ship.gs
        self.ship_player = int(ship.player)
        self.ship = ship
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()

        self.rect.x = ship.rect.x
        self.rect.y = self.gs.height - self.rect.height

        self.origin = ship.weapons_room # (x, y)
        self.firing_enabled = False
        self.target = self.origin

        self.ctr = 0

    def tick(self):
        color = (255,50,0)
        self.gs.screen.blit(self.image, self.rect)
        # firing ship is the player
        if (self.ship_player==int(self.gs.player)):
            if self.rect.collidepoint(self.gs.mouse_pos):
                self.firing_enabled = True
            if (self.firing_enabled==True) and (self.target != self.origin):
                start = self.origin
                end = self.target

                if self.ctr==0:
                    self.laser = LaserBeam(self.gs,start, end, self)
                    self.ctr = 1
                self.laser.tick()

        # firing ship is opponent
        elif (self.ship_player!=int(self.gs.player)) and (self.firing_enabled == True):
            start = self.origin
            end = self.target

            if self.ctr==0:
                self.laser = LaserBeam(self.gs,start, end, self)
                self.ctr = 1
            self.laser.tick()

class LaserBeam(pygame.sprite.Sprite):
    def __init__(self, gs, start, end, weapon):
        self.gs = gs
        self.damage = 1
        self.start = start
        self.end = end
        self.dx = end[0]-start[0]
        self.dy = end[1]-start[1]
        width = 50
        self.target = (self.end[0] - width/2., self.end[1] - width/2., width, width)
        self.speed = 50
        self.nextpoint = (self.start[0] + self.dx/self.speed, self.start[1] + self.dy/self.speed)

        self.weapon = weapon

    def tick(self):
        # increment location of laser beam
        self.nextpoint = (self.start[0] + self.dx/self.speed, self.start[1] + self.dy/self.speed)
        pygame.draw.line(self.gs.screen, (255,0,0), self.start, self.nextpoint, 12)
        self.start = (self.start[0] + self.dx/(8*self.speed), self.start[1] + self.dy/(8*self.speed))
        if pygame.Rect(self.target).collidepoint(self.nextpoint):
            self.weapon.firing_enabled = False
            self.weapon.target = self.weapon.origin
            self.weapon.ctr = 0
            #self.weapon.enemy_ship.health = self.weapon.enemy_ship.health -5
