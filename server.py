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
queueToP1 = DeferredQueue()
queueToP2 = DeferredQueue()

class PlayerCommand(LineReceiver):
    def __init__(self, port):
        self.port = port
        self.player = 0
        if self.port == 40084:
            self.player = 1
        else:
            self.player = 2

    def connectionMade(self):
        print p1Ship, p2Ship
        print 'connection made on port', self.port
        if self.player == 1:
            queueToP1.get().addCallback(self.callback)
        else:
            queueToP2.get().addCallback(self.callback)
    
    def connectionLost(self, reason):
        print 'lost connection on port', self.port 
        queueToP1.put("RESTART " + str(self.player))
        queueToP2.put("RESTART " + str(self.player))
        global p1Ship, p2Ship
        p1Ship = p2Ship = ""

    def lineReceived(self, line):
        print "Player", self.player, "sent data:", line
        global p1Ship, p2Ship
        if p1Ship == "" or p2Ship == "":
            if self.player == 1:
                p1Ship = line
            else:
                p2Ship = line
            # Send ship data if both players ready
            if p1Ship != "" and p2Ship != "":
                queueToP1.put("START " + p2Ship + " 2")
                queueToP2.put("START " + p1Ship + " 1")
        else:
            if self.player == 1:
                queueToP2.put(line)
            else:
                queueToP1.put(line)


    def callback(self, data):
        self.transport.write(data)

        strings = data.strip()
        if strings[0] == "RESTART":
            if strings[1] == "1" and str(self.player) == "1":
                queueToP2.get().addCallback(self.callback)
                print str(self.player), "callback to p2"
            elif strings[1] == "2" and str(self.player) == "2":
                queueToP1.get().addCallback(self.callback)
                print str(self.player), "callback to p1"
        else:
            if self.player == 1:
                queueToP1.get().addCallback(self.callback)
                print str(self.player), "callback to p1"
            else:
                queueToP2.get().addCallback(self.callback)
                print str(self.player), "callback to p2"


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
            return

if __name__ == '__main__':
    reactor.listenTCP(40084, PlayerFactory(40084))
    reactor.listenTCP(40092, PlayerFactory(40092))
    reactor.run()
