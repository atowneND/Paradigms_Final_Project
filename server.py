from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet.protocol import Protocol
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall
from twisted.internet import reactor
import time
import cPickle as pickle

playersConnected = 0

class PlayerCommand(LineReceiver):
    def __init__(self):
        self.queue = DeferredQueue()

    def connectionMade(self):
       playersConnected += 1
       self.queue.get().addCallback(self.callback) 

    #def dataReceived(self, data):
        # handle received data

    def callback(self, data):
        self.transport.write(data)
        self.queue.get().addCallback(self.callback) 


class PlayerFactory(Factory):
    def __init__(self):
        pass

    def buildProtocol(self, addr):
        return PlayerCommand(addr)

class GameSpace():
    def __init__(self):
       # initialize gs
       self.gameOver = False

    def tick(self):
        # Update the gamespace
        print 'update'

if __name__ == '__main__':
    reactor.listenTCP(40084, PlayerFactory())
    reactor.listenTCP(40092, PlayerFactory())
    while playersConnected != 2:
        time.sleep(2)
        print "Waiting for players to join..."
    gs = GameSpace()
    LC = LoopingCall(gs.tick)
    LC.start(1/60)
    reactor.run()
