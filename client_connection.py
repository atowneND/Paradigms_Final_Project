from twisted.internet import reactor as reactor
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet.task import LoopingCall
from twisted.internet.error import CannotListenError
from twisted.internet.defer import DeferredQueue

import pickle

import pygame
import sys
from maps import Maps
from menu import Menu
from ship import Ship
from gamespace import GameSpace

host = "student02.cse.nd.edu"

gs_queue = DeferredQueue()
gameOver = False
class ClientConnection(Protocol):
    def __init__(self, port, gs):
        self.delimiter = "\r\n"
        self.port = port
        self.gs = gs

    def dataReceived(self, data):
        print "received data:", data
        strings = data.split()
        # Let the users know what the other ship is
        if strings[0] == "START":
            self.gs.otherShip = Ship(self.gs, strings[1].lower(), strings[2])
            self.gs.myShip.weapon.enemy_ship = self.gs.otherShip
            self.gs.otherShip.weapon.enemy_ship = self.gs.myShip
            self.gs.otherShip.tick()
        # Share coordinates of fired shots
        elif strings[0] == "FIRE":
            self.gs.otherShip.weapon.target = (float(strings[2]), float(strings[3]))
            self.gs.otherShip.weapon.firing_enabled = True
            print "firing on coordinates", strings[2], strings[3]
        # End the game
        elif strings[0] == "END" and not gameOver:
            self.gs.gameOver = int(strings[1])
            global gameOver
            gameOver = True

    def connectionMade(self):
        print "now connected to", host, "port", self.port
        self.gs.queue.get().addCallback(self.sendData)

    def sendData(self, data):
        self.transport.write(data + self.delimiter)
        self.gs.queue.get().addCallback(self.sendData)

    def connectionLost(self, reason):
        print "lost connection to", host, "port", self.port
        reactor.stop()

class ClientConnectionFactory(ClientFactory):
    def __init__(self, port, gs):
        self.port = port
        protocol = ClientConnection
        self.gs = gs

    def buildProtocol(self, addr):
        return ClientConnection(self.port, self.gs)

class GameConnection:
    def __init__(self, port):
        gs = GameSpace(gs_queue, port)
        lc = LoopingCall(gs.update)
        lc.start(1/60)
        reactor.connectTCP(host, port, ClientConnectionFactory(port, gs))
        reactor.run()
