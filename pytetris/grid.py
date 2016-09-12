import pygame

from .cell import Cell

class Grid:
    def __init__(self, top_left, grid_dimensions, cell_dimensions, background_color, show_grid_marks):
        self.offset_x, self.offset_y = top_left
        self.column_count, self.row_count = grid_dimensions
        self.cell_width, self.cell_height = cell_dimensions
        self.background_color = background_color
        self.show_grid_marks = show_grid_marks
        self.cells = []
        self.current_shape = None
        self.__build_cells()

    def __build_cells(self):
        for row in range(self.row_count):
            self.cells.append([])
            for col in range(self.column_count):
                self.cells[row].append(Cell(
                    row=row,
                    column=col,
                    x_coordinate=col*self.cell_height + self.offset_x,
                    y_coordinate=row*self.cell_width + self.offset_y,
                ))

    def update_and_validate(self):
        is_valid = True
        for piece in self.current_shape.pieces:
            if piece.row <= 0:
                piece.row = 0
                is_valid = False
            self.cells[piece.row][piece.col].active = True
            self.cells[piece.row][piece.col].image = piece.image
        return is_valid

    def clear_and_count_rows(self):
        row_count = 0
        for row in range(self.row_count):
            flag_row = True
            for col in range(self.column_count):
                if self.cells[row][col].active:
                    flag_row = True
                    continue
                if not self.cells[row][col].active:
                    flag_row = False
                    break
            if flag_row:
                self.shift_row(row)
                row_count += 1
        return row_count

    def shift_row(self, row_number):
        for row in range(row_number, 0, -1):
            for col in range(self.column_count):
                self.cells[row][col].active = self.cells[row-1][col].active
                self.cells[row][col].image = self.cells[row-1][col].image

    def __reset_cells(self):
        for row in range(self.row_count):
            for col in range(self.column_count):
                self.cells[row][col].active = False
                self.cells[row][col].clear()

    def clear_shape(self):
        self.shape = None

    def toggle_grid_marks(self):
        self.show_grid_marks = not self.show_grid_marks

    def draw(self, screen):
        border_topx, border_topy = self.cells[0][0].rect.topleft
        border_btmx, border_btmy = self.cells[self.row_count-1][self.column_count-1].rect.bottomright
        pygame.draw.rect(screen, self.background_color, ((border_topx,border_topy),(border_btmx+1,border_btmy)), 1)

        for item in self.cells:
            for cell in item:
                if self.show_grid_marks:
                    screen.blit(cell.image, cell.rect.topleft)
                if cell.active:
                    screen.blit(cell.image, cell.rect.topleft)
        for piece in self.current_shape.pieces:
            piece_position = self.cells[piece.row][piece.col].rect.topleft
            screen.blit(piece.image, piece_position)
