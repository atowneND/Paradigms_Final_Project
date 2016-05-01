from twisted.internet import reactor as reactor
from twisted.internet.protocol import ClientFactory, Protocol
from twisted.internet.task import LoopingCall

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
    def __init__(self):
        self.delimiter = "\r\n\r\n"

    def lineReceived(self, data):
        print "received data:", data

    def connectionMade(self):
        print "new connection made to", host, "port", port

    def connectionLost(self, reason):
        print "lost connection to", host, "port", port

class ClientConnectionFactory(ClientFactory):
    protocol = ClientConnection

    def buildProtocol(self, addr):
        return ClientConnection()

class GameConnection:
    def __init__(self):
        gs = GameSpace()
        lc = LoopingCall(gs.update)
        lc.start(0.1)

        try:
            reactor.connectTCP(host, port1, ClientConnectionFactory())
        except socket.error:
            reactor.connectTCP(host, port2, ClientConnectionFactory())
        except:
            print "Unable to connect"
            exit()
        reactor.run()

