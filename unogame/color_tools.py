import pygame
from shadow_font import ShadowFont
from Cards import Color
from globals import RED, YELLOW, BLUE, GREEN, GRAY, BLACK


class ColorPicker:
    """A class for creating a color picker interface."""
    
    colors = [RED, YELLOW, BLUE, GREEN]
    options = [Color.RED, Color.YELLOW, Color.BLUE, Color.GREEN]

    def __init__(self, screen_width, screen_height):
        # create the color picker surface
        square_size = 80
        margin = 15
        left = margin
        top = 4 * margin
        w = len(ColorPicker.colors) * (square_size + margin) + margin
        h = top + square_size + margin
        self.surf = pygame.Surface((w, h))
        self.surf.fill(GRAY)
        pygame.draw.rect(self.surf, BLACK, self.surf.get_rect(), 2)

        # set the popup surface at center of screen
        popup_left = (screen_width - w) // 2
        popup_top = (screen_height - h) // 2
        self.rect = self.surf.get_rect(topleft=(popup_left, popup_top))
        
        # draw text label and option boxes
        font = ShadowFont("Arial", size=25, bold=True)
        text = font.render('Pick a color:')
        self.surf.blit(text, (margin, margin))
        self.option_rects = []
        for i, color in enumerate(ColorPicker.colors):
            x = left + (square_size + margin) * i
            y = top
            rect = pygame.draw.rect(self.surf, color, (x, y, square_size, square_size))
            rect.x += popup_left
            rect.y += popup_top
            self.option_rects.append(rect)

    def select(self) -> Color:
        for option, option_rect in zip(self.options, self.option_rects):
            if option_rect.collidepoint(pygame.mouse.get_pos()):
                return option
        return None


