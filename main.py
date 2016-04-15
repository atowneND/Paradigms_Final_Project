import pygame
import sys
from maps import Maps
from menu import Menu

class GameSpace:
    def __init__(self):
        pygame.init()

        self.size = self.width, self.height = (640, 1024)
        self.black = 0, 0, 0

        self.screen = pygame.display.set_mode(self.size, 0, 32)

    def main(self):
        print "rendering map"
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.test_maps()
            self.test_main_menu()
            pygame.display.flip()
        self.test_maps()

    def test_main_menu(self):
        csvfile = "main_menu.csv"
        main_menu = Menu(self, csvfile)
        main_menu.tick()

    def test_maps(self):
        csvfile = "grid.dat"
        m = Maps(self, csvfile)
        m.draw_grid()

if __name__ == "__main__":
    gs = GameSpace()
    gs.main()
