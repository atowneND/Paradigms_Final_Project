from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Protocol
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
import time
import cPickle as pickle

playersReady = 0

class PlayerCommand(LineReceiver):
    def __init__(self):
        self.queue = DeferredQueue()

    def connectionMade(self):
        self.queue.get().addCallback(self.callback) 

    def dataReceived(self, data):
        print data
        global playersReady
        playersReady += 1

    def callback(self, data):
        self.transport.write(data)
        self.queue.get().addCallback(self.callback) 


class PlayerFactory(Factory):
    def __init__(self):
        pass

    def buildProtocol(self, addr):
        return PlayerCommand()

class GameSpace():
    def __init__(self):
       # initialize gs
       self.gameOver = False

    def tick(self):
        # Update the gamespace
        while playersReady == 2:
            print 'update'

if __name__ == '__main__':
    reactor.listenTCP(40084, PlayerFactory())
    reactor.listenTCP(40092, PlayerFactory())
    gs = GameSpace()
    LC = LoopingCall(gs.tick)
    LC.start(1/60)
    reactor.run()
