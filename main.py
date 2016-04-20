import pygame
import sys
from maps import Maps
from menu import Menu
from ship import Ship

class GameSpace:
    def __init__(self):
        pygame.init()

        self.size = self.width, self.height = (2048, 2048)
        self.black = 0, 0, 0

        self.screen = pygame.display.set_mode(self.size, 0, 32)

        self.mouse_pos = [0,0]

    def main(self):
        ship = "blueship"
        ship = "cruiser"
        s = Ship(self, ship)
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # http://stackoverflow.com/questions/12150957/pygame-action-when-mouse-click-on-rect
                    self.mouse_pos = pygame.mouse.get_pos()
            self.test_Ship(s)
            #self.test_main_menu()
            pygame.display.flip()
        self.test_maps()

    def test_main_menu(self):
        csvfile = "main_menu.csv"
        main_menu = Menu(self, csvfile)
        main_menu.tick()

    def test_Ship(self, ship):
        # tests Ship() and Maps()
        ship.tick()

if __name__ == "__main__":
    gs = GameSpace()
    gs.main()
