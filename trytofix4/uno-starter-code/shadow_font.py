import pygame
import globals


class ShadowFont:
    """A class for creating text with shadow."""
    def __init__(self, font="Arial", size=30, shadow_offset=2, 
            sysfont=True, bold=False, italic=False):
        if sysfont:
            self.font = pygame.font.SysFont(font, size, bold=bold, italic=italic)
        else:
            self.font = pygame.font.Font(font, size)  # a font loaded from ttf file
            self.font.bold = bold
            self.font.italic = italic
        self.shadow_offset = shadow_offset

    def render(self, text, 
            text_color=globals.WHITE, shadow_color=globals.BLACK) -> pygame.Surface:
        """Create a transparent surface containing the text and shadow."""
        text_surf = self.font.render(text, True, text_color)
        shadow_surf = self.font.render(text, True, shadow_color)
        offset = self.shadow_offset
        w, h = text_surf.get_width() + offset + 1, text_surf.get_height() + offset + 1
        surf = pygame.Surface((w, h), pygame.SRCALPHA)  
        surf.fill((0, 0, 0, 0))   # a transparent surface
        # Blit the text surfaces onto the transparent surface
        surf.blit(shadow_surf, (offset, offset))
        surf.blit(text_surf, (0, 0))
        return surf