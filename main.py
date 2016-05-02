import pygame
import sys
from maps import Maps
from menu import Menu
from ship import Ship
from client_connection import GameConnection

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print 'USAGE: python main.py <40084|40092>'
    else:
        port = int(sys.argv[1])
        GameConnection(port)
