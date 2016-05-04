import pygame
import csv

WHITE = (255,255,255)
GREEN = (0,255,150)
RED = (235, 12, 12)

class Maps():
    # reformat inputs?
    def __init__(self, ship, pos, csvfile):
        self.gs = ship.gs
        self.ship = ship
        width = 50
        top_left_corner = pos

        with open(csvfile) as f:
            self.layout = [[int(x) for x in line.split()] for line in f]
        nboxes = sum([sum(x) for x in self.layout])
        self.grid = []

        s = 0
        for j in xrange(len(self.layout)):
            for i in xrange(len(self.layout[j])):
                room = self.layout[j][i]
                if room >= 1:
                    b = Box(width)
                    b.x = (top_left_corner[0] + width*i)
                    b.y = (top_left_corner[1] + width*j)
                    b.color = WHITE
                    b.img = ""
                    if room==1:
                        b.room = "empty"
                    elif room==2:
                        b.room = "bridge"
                        b.img = "rooms/"+b.room+".png"
                    elif room==3:
                        b.room = "shields"
                        b.img = "rooms/"+b.room+".png"
                    elif room==4:
                        b.room = "weapons"
                        b.img = "rooms/"+b.room+".png"
                        self.ship.weapons_room = (b.x + b.width/2., b.y + b.height/2.)
                    elif room==5:
                        b.room = "engines"
                        b.img = "rooms/"+b.room+".png"
                    elif room==6:
                        b.room = "sensors"
                        b.img = "rooms/"+b.room+".png"
                    elif room==9:
                        b.room = "medbay"
                        b.img = "rooms/"+b.room+".png"
                    elif room==8:
                        b.room = "oxygen"
                        b.img = "rooms/"+b.room+".png"
                    elif room==9:
                        b.room = "other"
                    self.grid.append(b)

    def draw_box(self,size,color):
        BLUE = (22,25,196)
        pygame.draw.rect(self.gs.screen,color,size)
        pygame.draw.rect(self.gs.screen,BLUE,size,4)

    def draw_grid(self):
        for b in self.grid:
            if pygame.Rect(b.x, b.y, b.width, b.height).collidepoint(self.gs.mouse_pos):
                target = (b.x + b.width/2., b.y + b.width/2.)
                if b.color != GREEN:
                    b.color = GREEN
                else:
                    b.color = WHITE
                if self.gs.myShip.weapon.firing_enabled == True:
                    self.gs.queue.put("FIRE " + b.room + " " + str(target[0]) + " " + str(target[1]))
                    self.gs.myShip.weapon.target = target
                    print "new target: my ship firing on ",target
                elif self.gs.otherShip.weapon.firing_enabled == True:
                    self.gs.queue.put("FIRE " + b.room + " " + str(target[0]) + " " + str(target[1]))
                    self.gs.otherShip.weapon.target = target
                    print "new target: other ship firing on",target
            size = (b.x,b.y,b.width,b.height)
            self.draw_box(size, b.color)
            if b.img:
                if 'image' not in dir(b):
                    b.image = RoomFunction(self.gs,b)
                    b.image.tick()
                else:
                    b.image.tick()

    def tick(self):
        self.draw_grid()

class RoomFunction(pygame.sprite.Sprite):
    def __init__(self, gs, box):
        self.gs = gs
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(box.img)
        self.rect = self.image.get_rect()

        # position
        self.rect.centerx = box.x + 0.5*box.width
        self.rect.centery = box.y + 0.5*box.height

    def tick(self):
        self.gs.screen.blit(self.image, self.rect)

class Box():
    def __init__(self, width):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = width
        self.color = (0,0,0)
