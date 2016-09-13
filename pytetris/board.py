import pygame

from .buttons import NewGameButton
from .buttons import PauseButton
from .cell import Cell
from .grid import Grid
from .shape import Shape
from .shape_viewer import ShapeViewer
from .util import draw_label
from .util import load_image
from .util import label_dimensions

class GameBoard:
    SIMPLE_VALUE_NAMES = [
        "background_color", "button_height", "cell_height", "cell_width",
        "columns", "coordinate_x", "coordinate_y", "display_depth", "display_flags",
        "down_key_shape_speed", "grid_background_color", "level", "rows",
        "rows_shifted", "score", "score_accumulator_multiplier", "score_row_exponent",
        "score_row_multiplier", "speed_change_per_level", "speed_minimum", "shape_speed",
        "show_grid", "show_grid", "slow_time", "slow_time_shape_speed", "show_grid",
        "strafe_rate", "strafe_tick_lag", "string_level", "string_next", "string_rows",
        "string_score", "window_height", "window_width",
    ]

    def __init__(self, **kwargs):
        self.__load_simple_values(kwargs)

        self.buttons = []
        self.next_shape = None
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

        _, self.font_height = label_dimensions("TEST")
        self.__reset_key_flags()
        self.__load_images()

        shape_viewer_offset_x = (self.columns + 1) * self.cell_width
        shape_viewer_offset_y = self.cell_height
        self.shape_previewer = ShapeViewer("NEXT",
                (shape_viewer_offset_x, shape_viewer_offset_y),
                kwargs["queue_dimensions"],
                (self.cell_width, self.cell_height)
        )

        self.grid = Grid(
                (0,0),
                (self.columns,self.rows),
                (kwargs["cell_width"], kwargs["cell_height"]),
                kwargs["grid_background_color"],
                kwargs["show_grid"]
        )

        PauseButton(self, self.pause_button_image, ((self.columns+1)*self.cell_width, ((self.rows)*self.cell_height) - self.button_height))
        NewGameButton(self, self.new_button_image, ((self.columns+4)*self.cell_width, ((self.rows)*self.cell_height) - self.button_height))

        self.shape_skip_handler = kwargs.get("shape_skip_handler", None)
        self.clear_bottom_row_handler = kwargs.get("clear_bottom_row_handler", None)
        self.clear_top_row_handler = kwargs.get("clear_top_row_handler", None)

    def __load_simple_values(self, options):
        for value_name in self.SIMPLE_VALUE_NAMES:
           setattr(self, value_name, options[value_name])

    def __load_images(self):
        self.game_over_image = load_image('game_over.png')
        self.board_bg_image = load_image('board_bg.png', False)
        self.side_bar_image = load_image('side_bar.png', False)
        self.pause_button_image = load_image('start_stop_btn.png', False)
        self.new_button_image = load_image('new_game_btn.png', False)


    def __initialize_shapes(self):
        self.grid.clear_shape()
        self.generate_shape()

    def initialize(self):
        self.__initialize_shapes()

    def reset(self):
        self.shape_speed = self.original_shape_speed
        self.paused = False
        self.slow_time = False
        self.game_over = False
        self.rows_shifted = 0
        self.level = 1
        self.score = 0
        self.grid.reset()
        self.__initialize_shapes()

    def generate_shape(self):
        self.__reset_key_flags()

        self.grid.current_shape = self.shape_previewer.shape

        new_shape  = Shape.random(self.grid)
        new_shape.rotate_random()
        new_shape.set_row_offset()
        new_shape.set_col_offset()

        self.shape_previewer.shape = new_shape

        if self.grid.current_shape is None:
            self.generate_shape()
        else:
            self.grid.current_shape.last_move = pygame.time.get_ticks()
            self.shape_previewer.draw_shape()


    def update(self):
        if self.game_over:
            self.__draw_game_over()

        if self.paused:
            return

        self.__refresh_screen()

        time = pygame.time.get_ticks()
        if self.grid.current_shape.active:
            if self.key_left_flag:
                if time - self.last_strafe >= self.strafe_rate:
                    self.grid.current_shape.move_left()
                    self.last_strafe = time
            elif self.key_right_flag:
                if time - self.last_strafe >= self.strafe_rate:
                    self.grid.current_shape.move_right()
                    self.last_strafe = time
            if time - self.grid.current_shape.last_move >= self.get_speed():
                self.grid.current_shape.move_down()
                self.grid.current_shape.last_move = time
        else:
            if self.grid.update_and_validate():
                self.__update_score(self.grid.clear_and_count_rows())
                self.generate_shape()
            else:
                self.end_game()

    def end_game(self):
        self.game_over = True
        self.paused = True
        self.__draw_game_over()

    def get_speed(self):
        speed = self.shape_speed
        if self.slow_time:
            speed = self.slow_time_shape_speed
        if self.key_down_flag:
            speed = self.down_key_shape_speed
        return speed

    def register_game_key_down(self, key):
        if key == pygame.K_p:
            self.paused = not self.paused
        if self.paused:
            if self.game_over:
                self.reset()
        else:
            if key == pygame.K_g:
                self.grid.toggle_grid_marks()
                self.update()
            if key == pygame.K_k:
                if self.shape_skip_handler is not None:
                    self.shape_skip_handler()
                self.generate_shape()
            if key == pygame.K_i:
                if self.clear_top_row_handler is not None:
                    self.clear_top_row()
                self.grid.clear_top_row()
            if key == pygame.K_m:
                if self.clear_bottom_row_handler is not None:
                    self.clear_bottom_row()
                self.grid.clear_bottom_row()
            elif key == pygame.K_s:
                self.toggle_slow_time()
            elif key == pygame.K_LEFT:
                if self.last_strafe == 0:
                    self.grid.current_shape.move_left()
                    self.last_strafe = (pygame.time.get_ticks()+self.strafe_tick_lag)
                    self.key_left_flag = True
            elif key == pygame.K_RIGHT:
                if self.last_strafe == 0:
                    self.grid.current_shape.move_right()
                    self.last_strafe = (pygame.time.get_ticks()+self.strafe_tick_lag)
                    self.key_right_flag = True
            elif key == pygame.K_DOWN:
                self.key_down_flag = True
            elif key == pygame.K_UP:
                self.grid.current_shape.rotate()

    def register_game_key_up(self, key):
        if key == pygame.K_DOWN:
            self.key_down_flag = False
        elif key == pygame.K_LEFT:
            self.key_left_flag = False
            self.last_strafe = 0
        elif key == pygame.K_RIGHT:
            self.key_right_flag = False
            self.last_strafe = 0

    def toggle_slow_time(self):
        self.slow_time = not self.slow_time

    def __update_score(self, rows_cleared):
        self.rows_shifted += rows_cleared
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
        self.grid.draw(self.screen)

    def __draw_game_over(self):
        xx = self.game_over_image.get_width()
        yy = self.game_over_image.get_height()
        draw_shape = (
            (self.window_width - xx)/2,
            (self.window_height - yy)/2,
        )
        self.screen.blit(self.game_over_image, draw_shape)

    def __draw_sidebar(self):
        self.screen.blit(self.side_bar_image, (self.cell_width*self.columns,0))
        self.shape_previewer.draw(self.screen)

        screen_midpoint_y = self.screen.get_height()/2
        draw_label(self.screen, self.string_level,
            location=((self.columns+1)*self.cell_width, screen_midpoint_y),
            params=[self.level]
        )

        draw_label(self.screen,
            self.string_rows,
            location=((self.columns+1)*self.cell_width, screen_midpoint_y - 2*self.font_height),
            params=[self.rows_shifted]
        )

        draw_label(self.screen,
            self.string_score,
            location=((self.columns+1)*self.cell_width, screen_midpoint_y - 4*self.font_height),
            params=[self.score]
        )

        for buttons in self.buttons:
            buttons.draw(self.screen)

