from twisted.internet import reactor as reactor
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet.task import LoopingCall
from twisted.internet.error import CannotListenError

import pygame
import sys
from maps import Maps
from menu import Menu
from ship import Ship
from gamespace import GameSpace

host = "student02.cse.nd.edu"
port1 = 40084
port2 = 40092

class ClientConnection(Protocol):
    def __init__(self, port):
        self.delimiter = "\r\n\r\n"
        self.port = port

    def lineReceived(self, data):
        print "received data:", data

    def connectionMade(self):
        print "new connection made to", host, "port", self.port

    def connectionLost(self, reason):
        print "lost connection to", host, "port", self.port

class ClientConnectionFactory(ClientFactory):
    def __init__(self, port):
        self.port = port
        protocol = ClientConnection

    def buildProtocol(self, addr):
        return ClientConnection(self.port)

    def clientConnectionFailed(self, connector, reason):
        if self.port == port1:
            reactor.connectTCP(host, port2, ClientConnectionFactory(port2))
        else:
            print "Connection failed"
            reactor.stop()

class GameConnection:
    def __init__(self):
        gs = GameSpace()
        lc = LoopingCall(gs.update)
        lc.start(0.1)

        reactor.connectTCP(host, port1, ClientConnectionFactory(port1))
        reactor.run()

