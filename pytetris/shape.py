from random import choice, randint
from .piece import Piece
from .util import load_image

class Shape:
    SHAPE_REGISTRY = {
        "z-reverse": {"id": 1, "filename": "gem_purple.png"},
        "pipe": {"id": 2, "filename": "gem_blue.png"},
        "join": {"id": 3, "filename": "gem_teal.png"},
        "square": {"id": 4, "filename": "gem_pink.png"},
        "z-normal": {"id": 5, "filename": "gem_white.png"},
        "l-normal": {"id": 6, "filename": "gem_green.png"},
        "l-reverse": {"id": 7, "filename": "gem_yellow.png"},
    }
    SHAPE_IMAGES_LOADED = False

    @classmethod
    def load_images(cls):
        for shape_recipe in cls.SHAPE_REGISTRY.values():
            shape_recipe["image"] = load_image(shape_recipe["filename"])
        cls.SHAPE_IMAGES_LOADED = True

    @classmethod
    def random(cls, grid):
        if not cls.SHAPE_IMAGES_LOADED:
            cls.load_images()
        shape_recipe = cls.SHAPE_REGISTRY[choice(cls.SHAPE_REGISTRY.keys())]
        return cls(grid, shape_recipe["id"], shape_recipe["image"])

    def __init__(self, grid, shape, image):
        self.pieces = []
        self.grid = grid
        self.shape = shape
        self.shape_rotation = 1
        self.last_move = 0
        self.active = True
        self.can_move = True
        self.fill_pieces(image)
        self.make_shape()

    def make_shape(self):
        if self.shape == 1:
            self.pieces[0].row = 0
            self.pieces[0].col = 7#     0
            self.pieces[1].row = 1#     00
            self.pieces[1].col = 7#      0
            self.pieces[2].row = 1
            self.pieces[2].col = 8
            self.pieces[3].row = 2
            self.pieces[3].col = 8
        if self.shape == 2:
            self.pieces[0].row = 0
            self.pieces[0].col = 7#     0
            self.pieces[1].row = 1#     0
            self.pieces[1].col = 7#     0
            self.pieces[2].row = 2#     0
            self.pieces[2].col = 7
            self.pieces[3].row = 3
            self.pieces[3].col = 7
        if self.shape == 3:
            self.pieces[0].row = 1
            self.pieces[0].col = 6#    000
            self.pieces[1].row = 1#     0
            self.pieces[1].col = 7
            self.pieces[2].row = 1
            self.pieces[2].col = 8
            self.pieces[3].row = 2
            self.pieces[3].col = 7
        if self.shape == 4:
            self.pieces[0].row = 0
            self.pieces[0].col = 6#     00
            self.pieces[1].row = 0#     00
            self.pieces[1].col = 7
            self.pieces[2].row = 1
            self.pieces[2].col = 6
            self.pieces[3].row = 1
            self.pieces[3].col = 7
        if self.shape == 5:
            self.pieces[0].row = 0
            self.pieces[0].col = 7#     0
            self.pieces[1].row = 1#    00
            self.pieces[1].col = 7#    0
            self.pieces[2].row = 1
            self.pieces[2].col = 6
            self.pieces[3].row = 2
            self.pieces[3].col = 6
        if self.shape == 6:
            self.pieces[0].row = 1
            self.pieces[0].col = 6#    000
            self.pieces[1].row = 1#    0
            self.pieces[1].col = 7
            self.pieces[2].row = 1
            self.pieces[2].col = 8
            self.pieces[3].row = 2
            self.pieces[3].col = 6
        if self.shape == 7:
            self.pieces[0].row = 1
            self.pieces[0].col = 6#    000
            self.pieces[1].row = 1#      0
            self.pieces[1].col = 7
            self.pieces[2].row = 1
            self.pieces[2].col = 8
            self.pieces[3].row = 2
            self.pieces[3].col = 8

    def fill_pieces(self, image):
        self.pieces.append(Piece(image))
        self.pieces.append(Piece(image))
        self.pieces.append(Piece(image))
        self.pieces.append(Piece(image))

    def update(self, time):
        pass

    def rotate_random(self):
        for _ in range(randint(0,4)):
            self.rotate()

    def rotate(self):
        if self.shape == 1:
            self.rotate_shape_1()
            return
        if self.shape == 2:
            self.rotate_shape_2()
            return
        if self.shape == 3:
            self.rotate_shape_3()
            return
        if self.shape == 4:
            return
        if self.shape == 5:
            self.rotate_shape_5()
            return
        if self.shape == 6:
            self.rotate_shape_6()
        if self.shape == 7:
            self.rotate_shape_7()

    def set_row_offset(self):
        flag_offset = False
        for piece in self.pieces:
            if piece.row > 0:
                flag_offset = True
            else:
                flag_offset = False
                return
        if flag_offset:
            for piece in self.pieces:
                piece.row -= 1

    def set_col_offset(self):
        col_index = []
        piece_cols = 0
        for piece in self.pieces:
            if piece.col not in col_index:
                col_index.append(piece.col)
                piece_cols += 1
        if 6 not in col_index and self.shape != 2:
            for piece in self.pieces:
                piece.col -= 1
        return piece_cols

    def move_left(self):
        flag = False
        for piece in self.pieces:
            if piece.col > 0:
                if self.grid.cells[piece.row][piece.col-1].active:
                    flag = True
            if piece.col == 0:
                flag = True
        if flag:
            return
        else:
            for piece in self.pieces:
                piece.col -= 1

    def move_right(self):
        flag = False
        for piece in self.pieces:
            if piece.col != self.grid.column_count - 1:
                if self.grid.cells[piece.row][piece.col+1].active:
                    flag = True
            if piece.col == self.grid.column_count -1:
                flag = True
        if flag:
            return
        else:
            for piece in self.pieces:
                piece.col += 1

    def move_down(self):
        flag = False
        for piece in self.pieces:
            if piece.row < self.grid.row_count - 1:
                if self.grid.cells[piece.row+1][piece.col].active:
                    flag = True
                    self.active = False
            if piece.row == self.grid.row_count - 1 or piece.row < 0:
                flag = True
                self.active = False
        if flag:
            return
        else:
            for piece in self.pieces:
                piece.row += 1

    def rotate_shape_1(self):
        flag_rotate = False
        p0r = self.pieces[0].row
        p0c = self.pieces[0].col
        p1r = self.pieces[2].row
        p1c = self.pieces[2].col
        p3r = self.pieces[3].row
        p3c = self.pieces[3].col
        if self.shape_rotation == 1:
            self.pieces[0].row += 1
            self.pieces[0].col += 1
            self.pieces[2].row += 1
            self.pieces[2].col -= 1
            self.pieces[3].col -= 2
        if self.shape_rotation == 2:
            self.pieces[0].row -= 1
            self.pieces[0].col -= 1
            self.pieces[2].row -= 1
            self.pieces[2].col += 1
            self.pieces[3].col += 2
        for piece in self.pieces:
            if piece.col < 0 or piece.col > self.grid.column_count - 1:
                flag_rotate = True
                break
            if piece.row > self.grid.row_count - 1 or piece.row < 0:
                flag_rotate = True
                break
        if flag_rotate == False:
            for piece in self.pieces:
                if self.grid.cells[piece.row][piece.col].active:
                    flag_rotate = True
                    break
        if flag_rotate:
            self.pieces[0].row = p0r
            self.pieces[0].col = p0c
            self.pieces[2].row = p1r
            self.pieces[2].col = p1c
            self.pieces[3].row = p3r
            self.pieces[3].col = p3c
        else:
            if self.shape_rotation == 1:
                self.shape_rotation = 2
                return
            if self.shape_rotation == 2:
                self.shape_rotation = 1

    def rotate_shape_2(self):
        flag_rotate = False
        p0r = self.pieces[0].row
        p0c = self.pieces[0].col
        p2r = self.pieces[2].row
        p2c = self.pieces[2].col
        p3r = self.pieces[3].row
        p3c = self.pieces[3].col
        if self.shape_rotation == 1:
            self.pieces[0].row += 1
            self.pieces[0].col -= 1
            self.pieces[2].row -= 1
            self.pieces[2].col += 1
            self.pieces[3].row -= 2
            self.pieces[3].col += 2
        if self.shape_rotation == 2:
            self.pieces[0].row -= 1
            self.pieces[0].col += 1
            self.pieces[2].row += 1
            self.pieces[2].col -= 1
            self.pieces[3].row += 2
            self.pieces[3].col -= 2
        for piece in self.pieces:
            if piece.col < 0 or piece.col > self.grid.column_count - 1:
                flag_rotate = True
                break
            if piece.row > self.grid.row_count - 1 or piece.row < 0:
                flag_rotate = True
                break
        if flag_rotate == False:
            for piece in self.pieces:
                if self.grid.cells[piece.row][piece.col].active:
                    flag_rotate = True
                    break
        if flag_rotate:
            self.pieces[0].row = p0r
            self.pieces[0].col = p0c
            self.pieces[2].row = p2r
            self.pieces[2].col = p2c
            self.pieces[3].row = p3r
            self.pieces[3].col = p3c
        else:
            if self.shape_rotation == 1:
                self.shape_rotation = 2
                return
            if self.shape_rotation == 2:
                self.shape_rotation = 1

    def rotate_shape_3(self):
        flag_rotate = False
        p0r = self.pieces[0].row
        p0c = self.pieces[0].col
        p2r = self.pieces[2].row
        p2c = self.pieces[2].col
        p3r = self.pieces[3].row
        p3c = self.pieces[3].col
        if self.shape_rotation == 1:
            self.pieces[0].row -= 1
            self.pieces[0].col += 1
            self.pieces[2].row += 1
            self.pieces[2].col -= 1
            self.pieces[3].row -= 1
            self.pieces[3].col -= 1
        if self.shape_rotation == 2:
            self.pieces[0].row += 1
            self.pieces[0].col += 1
            self.pieces[2].row -= 1
            self.pieces[2].col -= 1
            self.pieces[3].row -= 1
            self.pieces[3].col += 1
        if self.shape_rotation == 3:
            self.pieces[0].row += 1
            self.pieces[0].col -= 1
            self.pieces[2].row -= 1
            self.pieces[2].col += 1
            self.pieces[3].row += 1
            self.pieces[3].col += 1
        if self.shape_rotation == 4:
            self.pieces[0].row -= 1
            self.pieces[0].col -= 1
            self.pieces[2].row += 1
            self.pieces[2].col += 1
            self.pieces[3].row += 1
            self.pieces[3].col -= 1
        for piece in self.pieces:
            if piece.col < 0 or piece.col > self.grid.column_count - 1:
                flag_rotate = True
                break
            if piece.row > self.grid.row_count - 1 or piece.row < 0:
                flag_rotate = True
                break
        if flag_rotate == False:
            for piece in self.pieces:
                if self.grid.cells[piece.row][piece.col].active:
                    flag_rotate = True
                    break
        if flag_rotate:
            self.pieces[0].row = p0r
            self.pieces[0].col = p0c
            self.pieces[2].row = p2r
            self.pieces[2].col = p2c
            self.pieces[3].row = p3r
            self.pieces[3].col = p3c
        else:
            if self.shape_rotation == 1:
                self.shape_rotation = 2
                return
            if self.shape_rotation == 2:
                self.shape_rotation = 3
                return
            if self.shape_rotation == 3:
                self.shape_rotation = 4
                return
            if self.shape_rotation == 4:
                self.shape_rotation = 1

    def rotate_shape_4(self):
        pass

    def rotate_shape_5(self):
        flag_rotate = False
        p0r = self.pieces[0].row
        p0c = self.pieces[0].col
        p2r = self.pieces[2].row
        p2c = self.pieces[2].col
        p3r = self.pieces[3].row
        p3c = self.pieces[3].col
        if self.shape_rotation == 1:
            self.pieces[0].row += 1
            self.pieces[0].col += 1
            self.pieces[2].row -= 1
            self.pieces[2].col += 1
            self.pieces[3].row -= 2
        if self.shape_rotation == 2:
            self.pieces[0].row -= 1
            self.pieces[0].col -= 1
            self.pieces[2].row += 1
            self.pieces[2].col -= 1
            self.pieces[3].row += 2
        for piece in self.pieces:
            if piece.col < 0 or piece.col > self.grid.column_count - 1:
                flag_rotate = True
                break
            if piece.row > self.grid.row_count - 1 or piece.row < 0:
                flag_rotate = True
                break
        if flag_rotate == False:
            for piece in self.pieces:
                if self.grid.cells[piece.row][piece.col].active:
                    flag_rotate = True
                    break
        if flag_rotate:
            self.pieces[0].row = p0r
            self.pieces[0].col = p0c
            self.pieces[2].row = p2r
            self.pieces[2].col = p2c
            self.pieces[3].row = p3r
            self.pieces[3].col = p3c
        else:
            if self.shape_rotation == 1:
                self.shape_rotation = 2
                return
            if self.shape_rotation == 2:
                self.shape_rotation = 1

    def rotate_shape_6(self):
        flag_rotate = False
        p0r = self.pieces[0].row
        p0c = self.pieces[0].col
        p2r = self.pieces[2].row
        p2c = self.pieces[2].col
        p3r = self.pieces[3].row
        p3c = self.pieces[3].col
        if self.shape_rotation == 1:
            self.pieces[0].row -= 1
            self.pieces[0].col += 1
            self.pieces[2].row += 1
            self.pieces[2].col -= 1
            self.pieces[3].row -= 2
        if self.shape_rotation == 2:
            self.pieces[0].row += 1
            self.pieces[0].col += 1
            self.pieces[2].row -= 1
            self.pieces[2].col -= 1
            self.pieces[3].col += 2
        if self.shape_rotation == 3:
            self.pieces[0].row += 1
            self.pieces[0].col -= 1
            self.pieces[2].row -= 1
            self.pieces[2].col += 1
            self.pieces[3].row += 2
        if self.shape_rotation == 4:
            self.pieces[0].row -= 1
            self.pieces[0].col -= 1
            self.pieces[2].row += 1
            self.pieces[2].col += 1
            self.pieces[3].col -= 2

        for piece in self.pieces:
            if piece.col < 0 or piece.col > self.grid.column_count - 1:
                flag_rotate = True
                break
            if piece.row > self.grid.row_count - 1 or piece.row < 0:
                flag_rotate = True
                break
        if flag_rotate == False:
            for piece in self.pieces:
                if self.grid.cells[piece.row][piece.col].active:
                    flag_rotate = True
                    break
        if flag_rotate:
            self.pieces[0].row = p0r
            self.pieces[0].col = p0c
            self.pieces[2].row = p2r
            self.pieces[2].col = p2c
            self.pieces[3].row = p3r
            self.pieces[3].col = p3c
        else:
            if self.shape_rotation == 1:
                self.shape_rotation = 2
                return
            if self.shape_rotation == 2:
                self.shape_rotation = 3
                return
            if self.shape_rotation == 3:
                self.shape_rotation = 4
                return
            if self.shape_rotation == 4:
                self.shape_rotation = 1

    def rotate_shape_7(self):
        flag_rotate = False
        p0r = self.pieces[0].row
        p0c = self.pieces[0].col
        p2r = self.pieces[2].row
        p2c = self.pieces[2].col
        p3r = self.pieces[3].row
        p3c = self.pieces[3].col
        if self.shape_rotation == 1:
            self.pieces[0].row -= 1
            self.pieces[0].col += 1
            self.pieces[2].row += 1
            self.pieces[2].col -= 1
            self.pieces[3].col -= 2
        if self.shape_rotation == 2:
            self.pieces[0].row += 1
            self.pieces[0].col += 1
            self.pieces[2].row -= 1
            self.pieces[2].col -= 1
            self.pieces[3].row -= 2
        if self.shape_rotation == 3:
            self.pieces[0].row += 1
            self.pieces[0].col -= 1
            self.pieces[2].row -= 1
            self.pieces[2].col += 1
            self.pieces[3].col += 2
        if self.shape_rotation == 4:
            self.pieces[0].row -= 1
            self.pieces[0].col -= 1
            self.pieces[2].row += 1
            self.pieces[2].col += 1
            self.pieces[3].row += 2
        for piece in self.pieces:
            if piece.col < 0 or piece.col > self.grid.column_count - 1:
                flag_rotate = True
                break
            if piece.row > self.grid.row_count - 1 or piece.row < 0:
                flag_rotate = True
                break

        if flag_rotate == False:
            for piece in self.pieces:
                if self.grid.cells[piece.row][piece.col].active:
                    flag_rotate = True
                    break

        if flag_rotate:
            self.pieces[0].row = p0r
            self.pieces[0].col = p0c
            self.pieces[2].row = p2r
            self.pieces[2].col = p2c
            self.pieces[3].row = p3r
            self.pieces[3].col = p3c
        else:
            if self.shape_rotation == 1:
                self.shape_rotation = 2
                return
            if self.shape_rotation == 2:
                self.shape_rotation = 3
                return
            if self.shape_rotation == 3:
                self.shape_rotation = 4
                return
            if self.shape_rotation == 4:
                self.shape_rotation = 1
