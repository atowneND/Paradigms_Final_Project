import pygame
import csv

WHITE = (255,255,255)
GREEN = (0,255,150)
RED = (235, 12, 12)

class Maps():
    def __init__(self, gs, csvfile):
        self.gs = gs
        width = 50
        top_left_corner = (100,100)

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
                    elif room==5:
                        b.room = "engines"
                        b.img = "rooms/"+b.room+".png"
                    elif room==6:
                        b.room = "sensors"
                        b.img = "rooms/"+b.room+".png"
                    elif room==7:
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
                if b.color != GREEN:
                    b.color = GREEN
                else:
                    b.color = WHITE
            if b.img:
                b.color = RED
            size = (b.x,b.y,b.width,b.height)
            self.draw_box(size, b.color)

    def tick(self):
        self.draw_grid()

class Box():
    def __init__(self, width):
        self.x = 0
        self.y = 0
        self.width = width
        self.height = width
        self.color = (0,0,0)
