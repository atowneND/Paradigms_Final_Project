import pygame
import sys
from maps import Maps
from menu import Menu
from ship import Ship
from twisted.internet import reactor as reactor

class GameSpace:
    def __init__(self, queue):
        pygame.init()

        self.size = self.width, self.height = (1200, 600)
        self.black = 0, 0, 0

        self.screen = pygame.display.set_mode(self.size, 0, 32)

        self.mouse_pos = [0,0]

        self.gameStarted = False
        self.queue = queue

        self.menu = Menu(self, "main_menu.csv")
        #self.menu = Menu(self, "ship_menu.csv")
        self.menu.tick()
        self.ship = None

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
                    self.queue.put("DATA DATA DATA")
                else: 
                    p = self.menu.clickHandler(self.mouse_pos)
                    print p
                    if p == "PLAY":
                        self.menu = Menu(self, "ship_menu.csv")
                        self.menu.tick()
                    elif p == "Blueship" or p == "Cruiser":
                        self.queue.put(p) 
                        self.screen.fill(self.black)
                        self.ship = Ship(self,p.lower())
                        self.gameStarted = True

            if self.gameStarted:
                self.ship.tick()

            pygame.display.flip()
            self.mouse_pos = (0,0)

    def test_Ship(self, ship):
        # tests Ship() and Maps()
        ship.tick()
