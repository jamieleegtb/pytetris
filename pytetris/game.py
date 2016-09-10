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
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                    else:
                        board.register_game_key_down(event.key)
                if event.type == pygame.KEYUP:
                    board.register_game_key_up(event.key)
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
