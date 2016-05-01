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
port1 = 40084
port2 = 40092

x = 0
gs_queue = DeferredQueue()

class ClientConnection(Protocol):
    def __init__(self, port, gs):
        self.delimiter = "\r\n\r\n"
        self.port = port
        self.gs = gs

    def lineReceived(self, data):
        print "received data:", data

    def connectionMade(self):
        print "now connected to", host, "port", self.port
        def sendData(data):
            self.transport.write(data)
            gs_queue.get().addCallback(sendData)
        gs_queue.get().addCallback(sendData)

    def connectionLost(self, reason):
        print "lost connection to", host, "port", self.port

class ClientConnectionFactory(ClientFactory):
    def __init__(self, port, gs):
        self.port = port
        protocol = ClientConnection
        self.gs = gs

    def buildProtocol(self, addr):
        return ClientConnection(self.port, self.gs)

    def clientConnectionFailed(self, connector, reason):
        if self.port == port1:
            reactor.connectTCP(host, port2, ClientConnectionFactory(port2, self.gs))
        else:
            print "Connection failed"

class GameConnection:
    def __init__(self):
        gs = GameSpace(gs_queue)
        lc = LoopingCall(gs.update, gs_queue)
        lc.start(0.1)

        reactor.connectTCP(host, port1, ClientConnectionFactory(port1, gs))
        reactor.run()

