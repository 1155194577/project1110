import pygame
from pygame.transform import smoothscale, smoothscale_by
from pygame.image import load
from globals import *


def clip(surface: pygame.Surface, x, y, w, h) -> pygame.Surface:
    """Get a part of the image."""
    original = surface.copy()
    clipRect = pygame.Rect(x, y, w, h)
    original.set_clip(clipRect)
    clipped = surface.subsurface(original.get_clip())
    return clipped.copy()


def read_card_images(filename: str, n: int) -> list[pygame.Surface]:
    """Read n card images from the specified file.
    
    This is an ad hoc function that works only for a PNG image combining 
    card images in a 7x10 grid. It splits the image into n card images.
    """    
    images = []
    W, H = CARD_SIZE
    uno_big_image = load(filename).convert_alpha()
    for i in range(7):
        y = i * H
        for j in range(10):
            x = j * W
            image = clip(uno_big_image, x, y, W, H)
            if image.get_width() != W:
                image = smoothscale(image, (W, H))
            scaled_image = smoothscale_by(image, CARD_SCALE)
            images.append(scaled_image)
            if len(images) >= n:
                return images
    return images

