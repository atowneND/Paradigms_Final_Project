import pygame

class Weapons(pygame.sprite.Sprite):
    def __init__(self, ship, img):
        self.gs = ship.gs
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()

        self.rect.x = ship.rect.x
        self.rect.y = self.gs.height - self.rect.height

    def tick(self):
        self.gs.screen.blit(self.image, self.rect)
