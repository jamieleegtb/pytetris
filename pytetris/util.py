import pygame
import os

from .config import defaults

IMAGE_DIRECTORY=os.path.join('resources','images')

def load_image(filename,color_key=(255,0,255)):
    image = pygame.image.load(os.path.join(IMAGE_DIRECTORY, filename)).convert()
    if color_key:
        image.set_colorkey(color_key)
    return image

SOUND_DIRECTORY='resources'

def load_music(filename):
    pygame.mixer.music.load(os.path.join(SOUND_DIRECTORY, filename))


class _FontLoader:
    FONT = None
    FONT_DIRECTORY='resources'
    FONT_FILE = defaults["font_file"]
    FONT_SIZE = defaults["font_size"]
    FONT_COLOR = defaults["font_color"]

    @classmethod
    def get_font(cls):
        if cls.FONT is None:
            cls.FONT = pygame.font.Font(os.path.join(cls.FONT_DIRECTORY, cls.FONT_FILE), cls.FONT_SIZE)
        return cls.FONT

    @classmethod
    def render(cls, message):
        return cls.get_font().render(message, True, cls.FONT_COLOR)

def draw_label(screen, message, location, params=None):
    _message = message
    if params is not None:
        _message = _message.format(*params)
    screen.blit(_FontLoader.render(_message), location)

def label_dimensions(message):
    return _FontLoader.get_font().size(message)
