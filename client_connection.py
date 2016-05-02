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

class ClientConnection(Protocol):
    def __init__(self, port, gs):
        self.delimiter = "\r\n"
        self.port = port
        self.gs = gs

    def dataReceived(self, data):
        print "received data:", data
        strings = data.split()
        if strings[0] == "START":
            self.gs.otherShip = Ship(self.gs, strings[1].lower(), strings[2])
            self.gs.otherShip.tick()

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
        lc = LoopingCall(gs.update, gs_queue)
        lc.start(1/60)
        reactor.connectTCP(host, port, ClientConnectionFactory(port, gs))
        reactor.run()
