from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Protocol
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
import time
import cPickle as pickle

p1Ship = ""
p2Ship = ""

class PlayerCommand(LineReceiver):
    def __init__(self, port):
        self.queue = DeferredQueue()
        self.port = port

    def connectionMade(self):
        print 'connection made on port ', self.port
        self.queue.get().addCallback(self.callback) 

    def dataReceived(self, data):
        global p1Ship, p2Ship
        if p1Ship == "" or p2Ship == "":
            if self.port == 40084:
                p1Ship = data
            elif self.port == 40092:
                p2Ship = data

    def callback(self, data):
        self.transport.write(data)
        self.queue.get().addCallback(self.callback) 


class PlayerFactory(Factory):
    def __init__(self, port):
        self.port = port

    def buildProtocol(self, addr):
        return PlayerCommand(self.port)

class GameSpace():
    def __init__(self):
       # initialize gs
       self.gameOver = False

    def tick(self):
        # Update the gamespace
        global p1Ship, p2Ship
        if p1Ship != "" and p2Ship != "":
            print 'update'

if __name__ == '__main__':
    reactor.listenTCP(40084, PlayerFactory(40084))
    reactor.listenTCP(40092, PlayerFactory(40092))
    gs = GameSpace()
    LC = LoopingCall(gs.tick)
    LC.start(1/60)
    reactor.run()
