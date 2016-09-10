import pygame
import os

IMAGE_DIRECTORY=os.path.join('resources','images')

def load_image(filename,color_key=(255,0,255)):
    image = pygame.image.load(os.path.join(IMAGE_DIRECTORY, filename)).convert()
    if color_key: 
        image.set_colorkey(color_key)
    return image
