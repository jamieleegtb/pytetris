import pygame

from .util import draw_label
from .util import label_dimensions
from .util import load_image

class ShapeViewer:
    DEFAULT_BACKGROUND_IMAGE = None

    @staticmethod
    def load_default_image():
        if ShapeViewer.DEFAULT_BACKGROUND_IMAGE is None:
            ShapeViewer.DEFAULT_BACKGROUND_IMAGE = load_image('queue_bg_color.png', False)
        return ShapeViewer.DEFAULT_BACKGROUND_IMAGE

    def __init__(self, title, offset, dimensions, cell_dimensions):
        self.shape = None
        self.title = title
        self.offset_x, self.offset_y = offset
        self.surface = pygame.Surface(dimensions)
        self.cell_width, self.cell_height = cell_dimensions
        self.font_width, self.font_height = label_dimensions(self.title)
        self.image = self.load_default_image()

    def get_width(self):
        self.surface.get_width()

    def draw(self, screen):
        x_coordinate = self.offset_x + ((self.surface.get_width()/2) - (self.font_width/2))
        y_coordinate = self.offset_y - self.font_height
        draw_label(screen, self.title, (x_coordinate,y_coordinate))
        screen.blit(
            self.surface,
           (self.offset_x, self.offset_y)
        )

    def draw_shape(self):
        col_index = []
        row_index = []
        shape_rows = 0
        shape_columns = 0
        for piece in self.shape.pieces:
            if piece.row not in row_index:
                row_index.append(piece.row)
                shape_rows += 1
            if piece.col not in col_index:
                col_index.append(piece.col)
                shape_columns += 1
        x_offset = (self.surface.get_width()/2) - ((shape_columns * self.cell_width)/2)
        y_offset = (self.surface.get_height()/2) - ((shape_rows * self.cell_height)/2)
        self.surface.blit(self.image, (0,0))
        for piece in self.shape.pieces:
            if self.shape.shape == 2 and self.shape.shape_rotation == 1:
                x = x_offset
            else:
                x = x_offset + ((piece.col - 6) * self.cell_width)
            y = y_offset + (piece.row * self.cell_height)
            self.surface.blit(piece.image, (x, y))

