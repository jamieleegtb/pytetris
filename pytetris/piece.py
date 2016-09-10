import pygame

class Piece(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.row = 0
        self.col = 0

    def update(self, key, time, game_board):
        pass
