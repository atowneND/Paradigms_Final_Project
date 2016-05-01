import pygame
import csv

class Menu():
    def __init__(self, gs, csvfile):
        self.gs = gs
        self.menu_words = []
        self.rects = []
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

            # Store rects of rendered font surfaces for click detection
            rect = label.get_rect()
            rect.move_ip(i[1]["position"])
            self.rects.append(rect)

    def clickHandler(self, mousePos):
        """Returns None if no menu item selected, or the string of the selected item"""
        for i in range(0,len(self.rects)):
            rect = self.rects[i]
            if rect.collidepoint(mousePos):
                return self.menu_words[i][0]

        return None
