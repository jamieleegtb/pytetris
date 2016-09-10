import pygame

class Cell(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)
        self.active = False
        self.row = 0
        self.col = 0
        self.x = 0
        self.y = 0
