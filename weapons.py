import pygame

class Weapons(pygame.sprite.Sprite):
    def __init__(self, gs, img):
        self.gs = gs
        self.image = pygame.image.load(img)
