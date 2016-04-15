import pygame
import csv

class Menu():
    def __init__(self, gs, csvfile):
        self.gs = gs
        self.menu_words = []
        with open(csvfile) as f:
            data = csv.DictReader(f)
            for row in data:
                color = (int(row['R']), int(row['G']), int(row['B']))
                position = (int(row['X']), int(row['Y']))
                self.menu_words.append([row['word'],{'color':color, 'position':position}])
        self.myfont = pygame.font.SysFont("monospace",50)

    def tick(self):
        for i in self.menu_words:
            label = self.myfont.render(i[0], 1, i[1]["color"])
            self.gs.screen.blit(label, i[1]["position"])
