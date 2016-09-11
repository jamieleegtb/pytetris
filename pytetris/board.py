import pygame

from .buttons import NewGameButton
from .buttons import PauseButton
from .cell import Cell
from .shape import Shape
from .util import load_image

class GameBoard:
    SIMPLE_VALUE_NAMES = [
        "background_color", "button_height", "cell_height", "cell_width",
        "columns", "coordinate_x", "coordinate_y", "display_depth", "display_flags",
        "down_key_shape_speed", "font_color", "font_size", "level", "rows",
        "rows_shifted", "score", "score_accumulator_multiplier", "score_row_exponent",
        "score_row_multiplier", "speed_change_per_level", "speed_minimum", "shape_speed",
        "show_grid", "show_grid", "slow_time", "slow_time_shape_speed", "show_grid",
        "strafe_rate", "strafe_tick_lag", "string_level", "string_next", "string_rows",
        "string_score", "window_height", "window_width",
    ]

    def __init__(self, **kwargs):
        self.__load_simple_values(kwargs)

        self.cells = []
        self.buttons = []
        self.width = self.cell_width * self.columns
        self.height = self.cell_height * self.rows
        self.current_piece = None
        self.next_piece = None
        self.queue_image = pygame.Surface(kwargs["queue_dimensions"])
        self.last_strafe = 0
        self.paused = False
        self.game_over = False
        self.original_shape_speed = self.shape_speed
        self.original_level = self.level
        self.original_score = self.score

        self.screen = pygame.display.set_mode(
                (self.window_width, self.window_height),
                self.display_flags,
                self.display_depth
        )

        self.__reset_key_flags()
        self.__load_images()

        self.font = pygame.font.SysFont("arial black", self.font_size)

        PauseButton(self, self.pause_button_image, ((self.columns+1)*self.cell_width, ((self.rows)*self.cell_height) - self.button_height))
        NewGameButton(self, self.new_button_image, ((self.columns+4)*self.cell_width, ((self.rows)*self.cell_height) - self.button_height))

    def __load_simple_values(self, options):
        for value_name in self.SIMPLE_VALUE_NAMES:
           setattr(self, value_name, options[value_name])

    def __load_images(self):
        self.game_over_image = load_image('game_over.png')
        self.board_bg_image = load_image('board_bg.png', False)
        self.queue_bg_image = load_image('queue_bg_color.png', False)
        self.side_bar_image = load_image('side_bar.png', False)
        self.pause_button_image = load_image('start_stop_btn.png', False)
        self.new_button_image = load_image('new_game_btn.png', False)

    def __initialize_grid(self):
        if self.cells == []:
            for row in range(self.rows):
                self.cells.append([])
                for col in range(self.columns):
                    self.cells[row].append(Cell(
                        row=row,
                        column=col,
                        x_coordinate=col*self.cell_height + self.coordinate_x,
                        y_coordinate=row*self.cell_width + self.coordinate_y,
                    ))
        else:
            for row in range(self.rows):
                for col in range(self.columns):
                    self.cells[row][col].active = False
                    self.cells[row][col].clear()

    def __initialize_shapes(self):
        self.current_piece = None
        self.generate_piece()

    def initialize(self):
        self.__initialize_grid()
        self.__initialize_shapes()

    def reset(self):
        self.shape_speed = self.original_shape_speed
        self.paused = False
        self.slow_time = False
        self.game_over = False
        self.rows_shifted = 0
        self.level = 1
        self.score = 0
        self.__initialize_grid()
        self.__initialize_shapes()

    def generate_piece(self):
        self.__reset_key_flags()

        self.current_piece = self.next_piece

        self.next_piece = Shape.random(self)
        self.next_piece.rotate_random()
        self.next_piece.set_row_offset()
        self.next_piece.set_col_offset()
        if self.current_piece is None:
            self.generate_piece()
        else:
            self.current_piece.last_move = pygame.time.get_ticks()
            self.__draw_next_piece()

    def __draw_next_piece(self):
        col_index = []
        row_index = []
        piece_rows = 0
        piece_columns = 0
        for piece in self.next_piece.pieces:
            if piece.row not in row_index:
                row_index.append(piece.row)
                piece_rows += 1
            if piece.col not in col_index:
                col_index.append(piece.col)
                piece_columns += 1
        x_offset = (self.queue_image.get_width()/2) - ((piece_columns * self.cell_width)/2)
        y_offset = (self.queue_image.get_height()/2) - ((piece_rows * self.cell_height)/2)
        self.queue_image.blit(self.queue_bg_image, (0,0))
        for piece in self.next_piece.pieces:
            if self.next_piece.shape == 2 and self.next_piece.shape_rotation == 1:
                x = x_offset
            else:
                x = x_offset + ((piece.col - 6) * self.cell_width)
            y = y_offset + (piece.row * self.cell_height)
            self.queue_image.blit(piece.image, (x, y))

    def __draw_current_piece(self):
            for piece in self.current_piece.pieces:
                if piece.row <= 0:
                    piece.row = 0
                    self.game_over = True
                self.cells[piece.row][piece.col].active = True
                self.cells[piece.row][piece.col].image = piece.image

    def update(self):
        if self.game_over and not self.paused:
            self.paused = True
            self.__draw_game_over()

        if self.paused:
            return

        self.__refresh_screen()

        time = pygame.time.get_ticks()
        if self.current_piece.active:
            speed = self.shape_speed
            if self.slow_time:
                speed = self.slow_time_shape_speed
            if self.key_down_flag:
                speed = self.down_key_shape_speed
            if self.key_left_flag:
                if time - self.last_strafe >= self.strafe_rate:
                    self.current_piece.move_left()
                    self.last_strafe = time
            elif self.key_right_flag:
                if time - self.last_strafe >= self.strafe_rate:
                    self.current_piece.move_right()
                    self.last_strafe = time
            if time - self.current_piece.last_move >= speed:
                self.current_piece.move_down()
                self.current_piece.last_move = time
        else:
            self.__draw_current_piece()
            self.check_rows()
            self.generate_piece()

    def register_game_key_down(self, key):
        if key == pygame.K_p:
            self.paused = not self.paused
        if self.paused:
            if self.game_over:
                self.reset()
        else:
            if key == pygame.K_g:
                self.toggle_grid()
                self.update(pygame.time.get_ticks())
            elif key == pygame.K_s:
                self.toggle_slow_time()
            elif key == pygame.K_LEFT:
                if self.last_strafe == 0:
                    self.current_piece.move_left()
                    self.last_strafe = (pygame.time.get_ticks()+self.strafe_tick_lag)
                    self.key_left_flag = True
            elif key == pygame.K_RIGHT:
                if self.last_strafe == 0:
                    self.current_piece.move_right()
                    self.last_strafe = (pygame.time.get_ticks()+self.strafe_tick_lag)
                    self.key_right_flag = True
            elif key == pygame.K_DOWN:
                self.key_down_flag = True
            elif key == pygame.K_UP:
                self.current_piece.rotate()

    def register_game_key_up(self, key):
        if key == pygame.K_DOWN:
            self.key_down_flag = False
        elif key == pygame.K_LEFT:
            self.key_left_flag = False
            self.last_strafe = 0
        elif key == pygame.K_RIGHT:
            self.key_right_flag = False
            self.last_strafe = 0

    def toggle_grid(self):
        self.show_grid = not self.show_grid

    def toggle_slow_time(self):
        self.slow_time = not self.slow_time

    def check_rows(self):
        row_count = 0
        for row in range(self.rows):
            flag_row = True
            for col in range(self.columns):
                if self.cells[row][col].active:
                    flag_row = True
                    continue
                if not self.cells[row][col].active:
                    flag_row = False
                    break
            if flag_row:
                self.shift_row(row)
                row_count += 1
                self.rows_shifted += 1
        self.__update_score(row_count)

    def shift_row(self, row_number):
        for row in range(row_number, 0, -1):
            for col in range(self.columns):
                self.cells[row][col].active = self.cells[row-1][col].active
                self.cells[row][col].image = self.cells[row-1][col].image

    def __update_score(self, rows_cleared):
        self.score += pow(rows_cleared,self.score_row_exponent)*self.score_row_multiplier
        self.score += self.level * rows_cleared * self.score_accumulator_multiplier

        if self.rows_shifted >= (self.level*self.level)+(self.level*6):
            self.level += 1
            self.shape_speed -= self.speed_change_per_level
            if self.shape_speed < self.speed_minimum:
                self.shape_speed = self.speed_minimum

    def __reset_key_flags(self):
        self.key_down_flag = False
        self.key_left_flag = False
        self.key_right_flag = False

    def __refresh_screen(self):
        self.screen.blit(self.board_bg_image, (self.coordinate_x,self.coordinate_y))
        self.__draw_sidebar()
        self.__draw_grid()

    def __draw_game_over(self):
        xx = self.game_over_image.get_width()
        yy = self.game_over_image.get_height()
        draw_shape = (
            (self.window_width - xx)/2,
            (self.window_height - yy)/2,
        )
        self.screen.blit(self.game_over_image, draw_shape)

    def __render_label(self, message, location, params=None):
        _message = message
        if params is not None:
            _message = _message.format(*params)
        self.screen.blit(self.font.render(_message, True, self.font_color), location)

    def __draw_sidebar(self):
        self.screen.blit(self.side_bar_image, (self.cell_width*self.columns,0))
        x_coordinate = (self.columns + 1) * self.cell_width
        y_coordinate = self.cell_height
        self.screen.blit(self.queue_image, (x_coordinate, y_coordinate))

        font_w_next,font_h = self.font.size(self.string_next)
        x_coordinate += ((self.queue_image.get_width()/2) - (font_w_next/2))
        y_coordinate -= font_h
        self.__render_label(self.string_next, (x_coordinate,y_coordinate))

        screen_midpoint_y = self.screen.get_height()/2
        self.__render_label(self.string_level,
            location=((self.columns+1)*self.cell_width, screen_midpoint_y),
            params=[self.level]
        )

        self.__render_label(self.string_rows,
            location=((self.columns+1)*self.cell_width, screen_midpoint_y - 2*font_h),
            params=[self.rows_shifted]
        )

        self.__render_label(self.string_score,
            location=((self.columns+1)*self.cell_width, screen_midpoint_y - 4*font_h),
            params=[self.score]
        )

        for buttons in self.buttons:
            buttons.draw(self.screen)

    def __draw_grid(self):
        border_topx, border_topy = self.cells[0][0].rect.topleft
        border_btmx, border_btmy = self.cells[self.rows-1][self.columns-1].rect.bottomright
        pygame.draw.rect(self.screen, self.background_color, ((border_topx,border_topy),(border_btmx+1,border_btmy)), 1)

        for item in self.cells:
            for cell in item:
                if self.show_grid:
                    self.screen.blit(cell.image, cell.rect.topleft)
                if cell.active:
                    self.screen.blit(cell.image, cell.rect.topleft)
        for piece in self.current_piece.pieces:
            piece_position = self.cells[piece.row][piece.col].rect.topleft
            self.screen.blit(piece.image, piece_position)
