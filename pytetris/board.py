import pygame

from .buttons import NewGameButton
from .buttons import PauseButton
from .cell import Cell
from .shape import Shape
from .util import load_image

class GameBoard:
    def __init__(self, width, height):
        self.x = 0
        self.y = 0
        self.cells = []
        self.buttons =[]
        self.rows = 21
        self.cols = 14
        self.cell_width = 31
        self.width = self.cell_width * self.cols
        self.cell_height = 31
        self.height = self.cell_height * self.rows
        self.current_gp = None
        self.next_gp = None
        self.queue_image = pygame.Surface((162, 162))
        self.show_grid = False
        self.game_speed = 1000
        self.last_strafe = 0
        self.slow_time = False
        self.key_down_flag = False
        self.key_left_flag = False
        self.key_right_flag = False
        self.strafe_rate = 50
        self.last_strafe = 0
        self.paused = False
        self.game_over = False
        self.lines_done = 0
        self.level = 1
        self.score = 0

        self.screen_width = width
        self.screen_height = height

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 0, 32)

        self.__load_images()

        self.font = pygame.font.SysFont("arial black", 16)

        PauseButton(self, self.pause_button_image, ((self.cols+1)*self.cell_width, ((self.rows)*self.cell_height) - 45))
        NewGameButton(self, self.new_button_image, ((self.cols+4)*self.cell_width, ((self.rows)*self.cell_height) - 45))

    def __load_images(self):
        self.game_over_image = load_image('game_over.png')
        self.board_bg_image = load_image('board_bg.png', False)
        self.queue_bg_image = load_image('queue_bg_color.png', False)
        self.side_bar_image = load_image('side_bar.png', False)
        self.pause_button_image = load_image('start_stop_btn.png', False)
        self.new_button_image = load_image('new_game_btn.png', False)

    def initialize(self,time):
        self.current_gp = None
        self.next_gp = Shape.random(self)
        for row in range(self.rows):
            self.cells.append([])
            for col in range(self.cols):
                self.cells[row].append(Cell(
                    row=row,
                    column=col,
                    x_coordinate=col*self.cell_height + self.x,
                    y_coordinate=row*self.cell_width + self.y,
                ))
        self.next_gp.rotate_random()
        self.next_gp.set_row_offset()
        self.generate_gp(time)

    def reset(self):
        self.paused = False
        self.current_gp = None
        self.next_gp = Shape.random(self)
        self.game_speed = 1000
        self.slow_time = False
        self.game_over = False
        self.lines_done = 0
        self.level = 1
        self.score = 0
        for row in range(self.rows):
            for col in range(self.cols):
                self.cells[row][col].active = False
                self.cells[row][col].clear()
        self.next_gp.rotate_random()
        self.next_gp.set_row_offset()
        self.next_gp.set_col_offset()
        self.generate_gp(pygame.time.get_ticks())

    def generate_gp(self, time):
        self.key_down_flag = False
        self.key_left_flag = False
        self.key_right_flag = False
        self.current_gp = self.next_gp
        self.current_gp.last_move = time
        self.next_gp = Shape.random(self)
        self.next_gp.rotate_random()
        self.next_gp.set_row_offset()
        self.next_gp.set_col_offset()
        self.queue_image.fill((255,255,255))
        col_index = []
        row_index = []
        gp_rows = 0
        gp_cols = 0
        for gp in self.next_gp.pieces:
            if gp.row not in row_index:
                row_index.append(gp.row)
                gp_rows += 1
            if gp.col not in col_index:
                col_index.append(gp.col)
                gp_cols += 1
        x_offset = (self.queue_image.get_width()/2) - ((gp_cols * self.cell_width)/2)
        y_offset = (self.queue_image.get_height()/2) - ((gp_rows * self.cell_height)/2)
        self.queue_image.blit(self.queue_bg_image, (0,0))
        for gp in self.next_gp.pieces:
            if self.next_gp.shape == 2 and self.next_gp.shape_rotation == 1:
                x = x_offset
            else:
                x = x_offset + ((gp.col - 6) * self.cell_width)
            y = y_offset + (gp.row * self.cell_height)
            self.queue_image.blit(gp.image, (x, y))


    def update(self):
        if self.game_over and not self.paused:
            self.paused = True
            self.__draw_game_over()

        if self.paused:
            return

        self.__refresh_screen()

        time = pygame.time.get_ticks()
        if self.current_gp.active:
            speed = self.game_speed
            if self.slow_time:
                speed = 1000
            if self.key_down_flag:
                speed = 25
            elif self.key_left_flag:
                if time - self.last_strafe >= self.strafe_rate:
                    self.current_gp.move_left()
                    self.last_strafe = time
            elif self.key_right_flag:
                if time - self.last_strafe >= self.strafe_rate:
                    self.current_gp.move_right()
                    self.last_strafe = time
            if time - self.current_gp.last_move >= speed:
                self.current_gp.move_down()
                self.current_gp.last_move = time
        else:
            for gp in self.current_gp.pieces:
                if gp.row <= 0:
                    gp.row = 0
                    self.game_over = True
                self.cells[gp.row][gp.col].active = True
                self.cells[gp.row][gp.col].image = gp.image
            self.check_rows()
            self.generate_gp(time)

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
                    self.current_gp.move_left()
                    self.last_strafe = (pygame.time.get_ticks()+250)
                    self.key_left_flag = True
            elif key == pygame.K_RIGHT:
                if self.last_strafe == 0:
                    self.current_gp.move_right()
                    self.last_strafe = (pygame.time.get_ticks()+250)
                    self.key_right_flag = True
            elif key == pygame.K_DOWN:
                self.key_down_flag = True
            elif key == pygame.K_UP:
                self.current_gp.rotate()

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
            for col in range(self.cols):
                if self.cells[row][col].active:
                    flag_row = True
                    continue
                if not self.cells[row][col].active:
                    flag_row = False
                    break
            if flag_row:
                self.shift_row(row)
                row_count += 1
                self.lines_done += 1
        #if row_count >= 1:
            #remove_row_sound.play(0)
        self.score += pow(row_count,2)*100
        self.score += self.level * row_count * 20

        if self.lines_done >= (self.level*self.level)+(self.level*6):
            self.level += 1
            self.game_speed -= 65
            if self.game_speed < 100:
                self.game_speed = 100

    def shift_row(self, row_number):
        for row in range(row_number, 0, -1):
            for col in range(self.cols):
                self.cells[row][col].active = self.cells[row-1][col].active
                self.cells[row][col].image = self.cells[row-1][col].image

    def __refresh_screen(self):
        self.screen.fill((175,175,175))
        self.draw(self.screen)

    def __draw_game_over(self):
        xx = self.game_over_image.get_width()
        yy = self.game_over_image.get_height()
        draw_shape = (
            (self.screen_width - xx)/2,
            (self.screen_height - yy)/2,
        )
        self.screen.blit(self.game_over_image, draw_shape)

    def draw(self, surface):
        surface.blit(self.board_bg_image, (0,0))
        surface.blit(self.side_bar_image, ((14*31),0))
        x = (self.cols + 1) * self.cell_width
        y = self.cell_height
        surface.blit(self.queue_image, (x,y))
        #pygame.draw.rect(surface, (0,0,0), ((x-1,y-1),(self.queue_image.get_width()+2, self.queue_image.get_height()+2)), 2)

        font_w_next,font_h = self.font.size("NEXT")
        x += ((self.queue_image.get_width()/2) - (font_w_next/2))
        y -= font_h
        surface.blit(self.font.render("NEXT", True, (255,255,255)), (x,y))

        surface.blit(self.font.render("LEVEL: %d" %self.level, True, (255,255,255)), (x, (surface.get_height() - (20*font_h))))
        surface.blit(self.font.render("LINES: %d" %self.lines_done, True, (255,255,255)), (x, (surface.get_height() - (19*font_h))))
        surface.blit(self.font.render("SCORE: %d" %self.score, True, (255,255,255)), (x, (surface.get_height() - (18*font_h))))

        border_topx, border_topy = self.cells[0][0].rect.topleft
        border_btmx, border_btmy = self.cells[20][13].rect.bottomright
        pygame.draw.rect(surface, (0,0,0), ((border_topx,border_topy),(border_btmx+1,border_btmy)), 1)
        for item in self.cells:
            for cell in item:
                if self.show_grid:
                    surface.blit(cell.image, cell.rect.topleft)
                if cell.active:
                    surface.blit(cell.image, cell.rect.topleft)
        for gp in self.current_gp.pieces:
            gp_position = self.cells[gp.row][gp.col].rect.topleft
            surface.blit(gp.image, gp_position)
        for buttons in self.buttons:
            buttons.draw(surface)
        for buttons in self.buttons:
            buttons.draw(surface)
