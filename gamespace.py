import pygame
import sys
from maps import Maps
from menu import Menu
from ship import Ship
from twisted.internet import reactor as reactor

class GameSpace:
    def __init__(self, queue):
        pygame.init()

        self.size = self.width, self.height = (800, 800)
        self.black = 0, 0, 0

        self.screen = pygame.display.set_mode(self.size, 0, 32)

        self.mouse_pos = [0,0]

        self.gameStarted = False

        ship = "cruiser"
        self.ship = Ship(self, ship)
        queue.put(ship + "\r\n")

        self.menu = Menu(self, "main_menu.csv")
        self.menu.tick()

    def update(self, queue):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                reactor.stop()
                pygame.quit()
                try:
                    sys.exit()
                except BaseException:
                    pass
                break
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # http://stackoverflow.com/questions/12150957/pygame-action-when-mouse-click-on-rect
                self.mouse_pos = pygame.mouse.get_pos()
                if self.gameStarted:
                    print "players playing"
                else: 
                    p = self.menu.clickHandler(self.mouse_pos)
                    print p

            if self.gameStarted:
                self.test_Ship(self.ship)
            pygame.display.flip()
            self.mouse_pos = (0,0)

    def test_Ship(self, ship):
        # tests Ship() and Maps()
        ship.tick()
