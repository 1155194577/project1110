from enum import Enum
from pygame import Rect
from pygame.sprite import Sprite
from pygame.transform import scale_by


class Color(Enum):
    """An enumeration of UNO card colors."""
    RED = 1
    YELLOW = 2
    BLUE = 3
    GREEN = 4
    WILD = 5


# An enumeration of UNO card values 
# (defined in functional syntax)
Value = Enum('Value', 'C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 skip reverse draw2 draw4 card', start=0)


class Card(Sprite):
    """A class modeling a UNO card."""
    def __init__(self, color, value):
        super().__init__()
        self.color = color
        self.value = value
        self.discarded = False

    def set_image(self, image):
        self.image = image
        self.rect = self.image.get_rect()
        return self

    def set_pos(self, x, y):
        self.rect.topleft = (x, y)
        return self

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        special = True if self.value.value > Value.C9.value else False
        if self.color == Color.WILD and self.value.value < Value.draw4.value:
            return str(None)  # no such card type
        #return str(self.color)[6:] + ' ' + str(self.value)[6:]  # full name
        return str(self.color)[6] + str(self.value)[6 if special else 7]  # abbreviation


def arrange(hand: list[Card]) -> None:
    """Place a hand of cards on the table"""
    
    # for more cards, use small gap between cards
    gap_width = 40 if len(hand) > 15 else (60 if len(hand) > 8 else 110)
    for i, card in enumerate(hand):
        card.set_pos(100 + i*gap_width, 600)

