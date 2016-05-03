import pygame

class Weapons(pygame.sprite.Sprite):
    def __init__(self, ship, img):
        self.gs = ship.gs
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()

        self.rect.x = ship.rect.x
        self.rect.y = self.gs.height - self.rect.height

        self.origin = ship.weapons_room # (x, y)

    def tick(self):
        color = (22,25,196)
        self.gs.screen.blit(self.image, self.rect)
        if self.rect.collidepoint(self.gs.mouse_pos):
            print "FIRE"
            self.fire = True
