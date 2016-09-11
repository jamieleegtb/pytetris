import pygame

from .board import GameBoard
from .config import defaults
from .util import load_music

class Game:
    LEFT_MOUSE_SEQUENCE_INDEX = 1

    def __init__(self, **kwargs):
        options = defaults.copy()
        options.update(kwargs)
        self.is_running = False
        self.is_loaded = True

        pygame.mixer.pre_init(
            options["mixer_frequency"],
            options["mixer_size"],
            options["mixer_channels"],
            options["mixer_buffer_size"]
        )
        pygame.init()

        load_music(options["music_file"])
        pygame.mixer.music.set_volume(options["mixer_volume_music"])

        pygame.display.set_caption("Pytris")
        self.clock = pygame.time.Clock()

        self.board = GameBoard(**options)

    def __del__(self):
        self.is_loaded = False
        del self.board
        pygame.quit()

    def run(self):
        self.is_running = True
        self.board.initialize()

        while self.is_running:
            if not pygame.mixer.music.get_busy():
                    pygame.mixer.music.play()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[self.LEFT_MOUSE_SEQUENCE_INDEX] == 1 :
                        position = pygame.mouse.get_pos()
                        for buttons in self.board.buttons:
                            buttons.check_click(position)
                if event.type == pygame.QUIT:
                    self.is_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.is_running = False
                    else:
                        self.board.register_game_key_down(event.key)
                if event.type == pygame.KEYUP:
                    self.board.register_game_key_up(event.key)
            self.board.update()
            pygame.display.flip()
