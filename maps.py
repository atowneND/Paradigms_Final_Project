import pygame
import csv

class Maps():
    def __init__(self, gs, csvfile):
        self.gs = gs
        with open(csvfile) as f:
            self.grid = [[int(x) for x in line.split()] for line in f]

    def draw_box(self,size):
        WHITE = (255,255,255)
        BLUE = (0,0,255)
        pygame.draw.rect(self.gs.screen,WHITE,size)
        pygame.draw.rect(self.gs.screen,BLUE,size,4)

    def draw_grid(self):
        width = 50
        top_left_corner = (100,100)
        num_rows = len(self.grid) # down, number of rows

        for j in xrange(num_rows):
            for i in xrange(len(self.grid[j])):
                if self.grid[j][i]==1:
                    x = (top_left_corner[0] + width * i)
                    y = (top_left_corner[1] + width * j)
                    size = (x,y,width,width)
                    self.draw_box(size)

