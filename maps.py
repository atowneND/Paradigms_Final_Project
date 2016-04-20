import pygame
import csv

class Maps():
    def __init__(self, gs, csvfile):
        self.gs = gs
        with open(csvfile) as f:
            self.grid = [[int(x) for x in line.split()] for line in f]

    def draw_box(self,size,color):
        BLUE = (22,25,196)
        pygame.draw.rect(self.gs.screen,color,size)
        pygame.draw.rect(self.gs.screen,BLUE,size,4)

    def draw_grid(self):
        width = 50
        top_left_corner = (100,100)

        WHITE = (255,255,255)
        GREEN = (0,255,150)
        RED = (235, 12, 12)
        color = WHITE

        num_rows = len(self.grid) # down, number of rows
        for j in xrange(num_rows):
            for i in xrange(len(self.grid[j])):
                if self.grid[j][i]==1:
                    x = (top_left_corner[0] + width * i)
                    y = (top_left_corner[1] + width * j)
                    if pygame.Rect(x,y,width,width).collidepoint(self.gs.mouse_pos):
                        color = GREEN
                    else:
                        color = WHITE
                    size = (x,y,width,width)
                    self.draw_box(size, color)

    def tick(self):
        self.draw_grid()

