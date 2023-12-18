import random
import itertools
from globals import *
from unocard import Color, Value, Card
from cardreader import read_card_images


def build_deck(mode: str = 'console') -> list[Card]:
    """Create a deck of UNO cards."""
    deck = []
    for c in itertools.islice(Color, 0, 4):  # Red to Blue
        for v in itertools.islice(Value, 0, 13): # 0-9, skip, reverse, draw2
            num = 1 if v == Value.C0 else 2  # only 1 zero-card per color
            for i in range(num):
                deck.append(Card(c, v))

    for i in range(4):
        deck.append(Card(Color.WILD, Value.card))   # wild card
        deck.append(Card(Color.WILD, Value.draw4))  # wild draw4

    # Add images to cards in GUI mode
    if mode == 'gui':
        card_images = read_card_images(UNO_FRONT_IMAGE, 52) # 1-9 + other cards
        card_images += read_card_images(UNO_ZEROS_IMAGE, 4) # zero cards
        image_map = dict(zip(CARD_KEYS.split(), card_images))
        for card in deck:
            card.set_image(image_map[str(card)])

    random.shuffle(deck)
    return deck


def deal_cards(deck: list[Card], n: int) -> list[Card]:
    """Deal n cards from the deck."""
    cards = deck[:n]
    del deck[:n]
    return cards
