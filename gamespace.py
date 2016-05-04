import pygame
import sys
from maps import Maps
from menu import Menu
from ship import Ship
from twisted.internet import reactor as reactor

class GameSpace:
    def __init__(self, queue, port):
        pygame.init()

        self.size = self.width, self.height = (1400, 600)
        self.black = 0, 0, 0

        self.screen = pygame.display.set_mode(self.size, 0, 32)

        self.mouse_pos = [0,0]

        self.gameStarted = False
        self.gameOver = 0
        self.cease = False
        self.queue = queue

        self.player = 0
        if port == 40084:
            self.player = 1
        else:
            self.player = 2

        self.menu = Menu(self, "main_menu.csv")
        self.menu.tick()
        self.myShip = None
        self.otherShip = None

    def update(self):
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
                    pass
                    #self.queue.put("DATA DATA DATA")
                else:
                    # Check if any options have been selected in the menus
                    p = self.menu.clickHandler(self.mouse_pos)
                    print p
                    if p == "PLAY":
                        self.menu = Menu(self, "ship_menu.csv")
                        self.menu.tick()
                    elif p == "Blueship" or p == "Cruiser":
                        self.queue.put(p)
                        self.screen.fill(self.black)
                        self.myShip = Ship(self,p.lower(),str(self.player))
                        self.gameStarted = True
        
        # If game over, broadcast winner and show end screen
        if self.gameOver and not self.cease:
            self.queue.put("END " + str(self.gameOver))
            self.gameStarted = False
            self.cease = True
            self.screen.fill(self.black)
            myfont = pygame.font.SysFont("monospace",50)
            label = myfont.render("Player " + str(self.gameOver) + " WINS!", 1, (255,0,0))
            self.screen.blit(label, (650, 300))

        # should everything from here forward be unindented by one block? so multiple events can occur on one tick?
        if self.gameStarted:
            self.screen.fill(self.black)
            self.myShip.tick()
            if self.otherShip != None:
                self.otherShip.tick()

        pygame.display.flip()
        self.mouse_pos = (0,0)
