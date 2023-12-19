import random
import itertools
from Cards import *
from pygame.sprite import Sprite,Group
from pygame.transform import smoothscale_by
import pygame
from pygame.image import load
from cardreader import read_card_images
from globals import UNO_FRONT_IMAGE,UNO_ZEROS_IMAGE,CARD_KEYS
class Deck(Group): 
    def __init__(self) -> None:
        super().__init__()
        self.cards = []
        
class DrawPile(Deck):
    def __init__(self) -> None:
        super().__init__()
    
    def build_deck(self,mode="console"):
        for c in itertools.islice(Color,0,4):
            for v in itertools.islice(Value,0,10): ## 0-9 : NumberCard , 10-12 : skip/Reverse/draw2 
                num = 1 if v == Value.C0 else 2
                for i in range(num):
                   ## print(c,v)
                    self.cards.append(Card(c,v))
            for v in itertools.islice(Value,10,13):
                num=2 
                for i in range(num):
                    ###print(v.name)
                    if v.name=='skip':
                        self.cards.append(Skip(c,v))
                    elif v.name=='reverse':
                        self.cards.append(Reverse(c,v))
                    elif v.name=='draw2':
                        self.cards.append(Draw2(c,v)) 
        self.AddWildCard()                 
        if mode == 'gui': ## debug purpose
                card_images = read_card_images(UNO_FRONT_IMAGE,52) 
                card_images += read_card_images(UNO_ZEROS_IMAGE,4)
                image_map = dict(zip(CARD_KEYS.split(),card_images))
                for card in self.cards:
                    card.set_image(image_map[str(card)])
                self.shuffle()    
                return self.cards
                                         
    def AddWildCard(self):
        c = Color.WILD
        v1 = Value.draw4
        v2 = Value.card
        for i in range(4):
            self.cards.append(WildCard(c,v2))
        for i in range(4):
            self.cards.append(WildDraw4(c,v1))
            
    def deal_cards(self,n): 
        cards = self.cards[:n]
        del self.cards[:n]
        return cards           

    def shuffle(self): 
        random.shuffle(self.cards)

class DiscardPile(Deck):
    def __init__(self) -> None:
        super().__init__()

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
        