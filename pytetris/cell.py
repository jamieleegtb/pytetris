from pygame.sprite import Sprite

from .util import load_image

class Cell(Sprite):
    DEFAULT_IMAGE = None

    @staticmethod
    def load_default_image():
        if Cell.DEFAULT_IMAGE is None:
            Cell.DEFAULT_IMAGE = load_image("cell1.png")
        return Cell.DEFAULT_IMAGE

    def __init__(self, **kwargs):
        Sprite.__init__(self)
        self.image = self.load_default_image()
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)
        self.active = kwargs.get("active", False)
        self.row = kwargs.get("row", 0)
        self.column = kwargs.get("column", 0)
        self.x_coordinate = kwargs.get("x_coordinate", 0)
        self.y_coordinate = kwargs.get("y_coordinate", 0)

    def clear(self):
        self.image = self.load_default_image()

    @property
    def x_coordinate(self):
        return self.x

    @x_coordinate.setter
    def x_coordinate(self, value):
        self.x = value
        self.rect.topleft = (self.x, self.rect[1])

    @property
    def y_coordinate(self):
        return self.x

    @y_coordinate.setter
    def y_coordinate(self, value):
        self.y = value
        self.rect.topleft = (self.rect[0], self.y)

