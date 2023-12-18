import pygame
from pygame.sprite import Sprite
from pygame.image import load
from pygame.transform import smoothscale_by


class DiscardArea(Sprite):
    """A sprite representing the discard area on the table."""
    def __init__(self, image, x, y):
        super().__init__()
        texture_image = smoothscale_by(load(image).convert(), 0.11)
        t_size = texture_image.get_size()
        surf = pygame.Surface(t_size, pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 255, 255), (0, 0, *t_size), border_radius=20)
        discard_surf = texture_image.copy().convert_alpha()
        discard_surf.blit(surf, (0, 0), None, pygame.BLEND_RGBA_MIN)
        self.image = discard_surf
        self.rect = self.image.get_rect(topleft=(x, y))