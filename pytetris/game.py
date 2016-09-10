import pygame
from pygame.locals import *
from .board import *
from sys import exit

class Game:
    def __init__(self, **kwargs):
        self.is_running = False
        self.is_loaded = True
        pygame.mixer.pre_init(44100, -16, 2, 2048)
        pygame.init()

        self.screen_width = kwargs.get("screen_width", 651)
        self.screen_height = kwargs.get("screen_height", 651)
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), 0, 32)

    def __del__(self):
        self.is_loaded = False
        pygame.quit()

    def run(self):
        self.is_running = True
        pygame.display.set_caption("Pytris")
        clock = pygame.time.Clock()
        pygame.mixer.music.set_volume(0.3)
        load_music('bg_music.ogg')
        board = GameBoard()
        board.initialize(pygame.time.get_ticks())
        while self.is_running:
            if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed() ==(1,0,0):
                        position = pygame.mouse.get_pos()
                        for buttons in board.buttons:
                            buttons.check_click(position)
                if event.type == pygame.QUIT:
                    self.is_running = False
                if board.paused:
                    break
                if event.type == pygame.KEYDOWN:
                    self.__handle_key_down(event.key, board)
                if event.type == pygame.KEYUP:
                    self.__handle_key_up(event.key, board)
            self.__update_board(board)


    def __update_board(self, board):
        board.update(pygame.time.get_ticks())
        self.screen.fill((175,175,175))
        board.draw(self.screen)
        if board.game_over:
            board.puase = True
            x = self.screen_width
            y = self.screen_height
            xx = game_over_image.get_width()
            yy = game_over_image.get_height()
            self.screen.blit(game_over_image, ((x - xx)/2, (y - yy)/2))
        pygame.display.flip()


    def __handle_key_down(self, key, board):
        if key == pygame.K_ESCAPE:
            self.is_running = False
        if key == pygame.K_g:
            board.toggle_grid()
            board.update(pygame.time.get_ticks())
        if key == pygame.K_s:
            board.slow_time = not board.slow_time
        if key == pygame.K_LEFT:
            if board.last_strafe == 0:
                board.current_gp.move_left()
                board.last_strafe = (pygame.time.get_ticks()+250)
                board.key_left_flag = True
        if key == pygame.K_RIGHT:
            if board.last_strafe == 0:
                board.current_gp.move_right()
                board.last_strafe = (pygame.time.get_ticks()+250)
                board.key_right_flag = True
        if key == pygame.K_DOWN:
            board.key_down_flag = True
        if key == pygame.K_UP:
            board.current_gp.rotate()

    def __handle_key_up(self, key, board):
        if key == pygame.K_DOWN:
            board.key_down_flag = False
        if key == pygame.K_LEFT:
            board.key_left_flag = False
            board.last_strafe = 0
        if key == pygame.K_RIGHT:
            board.key_right_flag = False
            board.last_strafe = 0
