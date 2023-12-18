from enum import Enum
from pygame.sprite import Sprite
import pygame 
class Color(Enum):
    """An enumeration of UNO card colors."""
    RED = 1
    YELLOW = 2
    BLUE = 3
    GREEN = 4
    WILD = 5
    
Value = Enum('Value', 'C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 skip reverse draw2 draw4 card', start=0)


class Card(Sprite):
    def __init__(self,color,value) -> None:
        """The object representing Card"""
        super().__init__()
        self.color = color
        self.value = value 
        self.discarded = False 
    
    def set_image(self,image):
        self.image = image
        self.rect = self.image.get_rect()    
        return self 
    
    def set_pos(self,x,y):
        self.rect.topleft = (x,y)
        return self 
        
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        special = True if self.value.value > Value.C9.value else False
        if self.color == Color.WILD and self.value.value < Value.draw4.value:
            return str(None)  # no such card type
        #return str(self.color)[6:] + ' ' + str(self.value)[6:]  # full name
        return str(self.color)[6] + str(self.value)[6 if special else 7]  # abbreviation
    def Next(self,currentPlayer,Clockwise): 
        if Clockwise: 
            return currentPlayer.next
        else: 
            return currentPlayer.prev   
              
    def play(self,currentPlayer,Clockwise):
        NextTurnPlayer = self.Next(currentPlayer,Clockwise)
        return NextTurnPlayer
        
class ActionCard(Card):
    def __init__(self,color,value) -> None:
     super().__init__(color,value)
     self.action = value.name ## actions can be skip,reverse,draw2,draw4,card
    
class Reverse(ActionCard):
    def __init__(self, color, value) -> None:
        super().__init__(color, value)
    def Reverse(self,currentplayer,clockwise):
        clockwise = not clockwise  
        NextTurnPlayer = self.Next(currentplayer,clockwise)
        return NextTurnPlayer
    def play(self,currentplayer,clockwise): 
        print("[Debug] Direction is reversed!")
        NextTurnPlayer = self.Reverse(currentplayer,clockwise)
        return NextTurnPlayer
     
class Skip(ActionCard):
    def __init__(self, color, value) -> None:
        super().__init__(color, value)
    def skip(self,currentplayer,clockwise):
        print("[Debug] The turn is Skip!!")
        if clockwise:  ## if clockwise => next person/anti-clockwise=>prev person
            return currentplayer.next.next
        else: 
            return currentplayer.prev.prev 
 
    def play(self,currentplayer,clockwise): 
        NextTurnPlayer = self.skip(currentplayer,clockwise)
        return NextTurnPlayer 
  
class Draw2(Skip):
    def __init__(self, color, value) -> None:
        super().__init__(color, value)
        
    def drawNcard(self,player,n,drawpile):     
        cards = drawpile.deal_cards(n)
        for card in cards:
            player.hand.append(card)
        print(f"[Debug]: {player.name} drawn {cards}")    
     
    def draw2(self,currentplayer,clockwise,drawpile):
        NextNextturnplayer = self.skip(currentplayer,clockwise) 
        nextturnplayer = self.Next(currentplayer,clockwise)
        self.drawNcard(nextturnplayer,2,drawpile)
        return NextNextturnplayer   
    def play(self,currentplayer,clockwise,drawpile): 
        NextNextTurnPlayer = self.draw2(currentplayer,clockwise,drawpile)
        return NextNextTurnPlayer
        ## draw 2 card from DrawPile via deal_cards(self.n)
        ## append that to players' hand      
  
class WildCard(ActionCard):
    def __init__(self, color, value) -> None:
        super().__init__(color, value)      
    
    def ChangeColour(self,player,clockwise,drawpile):   
        selectedColor = player.ChooseColour()
        print(f"The colour is changed to {selectedColor}")
        NextTurnPlayer = self.Next(player,clockwise)
        return NextTurnPlayer,selectedColor
            
    def play(self,player,clockwise,drawpile):
        print("The function wildcard is execuated")
        NextTurnPlayer , selectedColor = self.ChangeColour(player,clockwise,drawpile) 
        return NextTurnPlayer, selectedColor

class WildDraw4(Draw2,WildCard):
    def __init__(self, color, value) -> None:
        super().__init__(color, value)
    def wildDraw4(self,currentplayer,clockwise,drawpile):
        print("the function wilddraw 4 is execuated")
        NextTurnPlayer , selectedColour = self.ChangeColour(currentplayer,clockwise,drawpile)
        self.drawNcard(NextTurnPlayer,4,drawpile)
        Nextnextturnplayer = self.skip(currentplayer,clockwise)
        return Nextnextturnplayer,selectedColour
        
    def play(self,currentplayer,clockwise,drawpile):
       NextNextTurnPlayer,selectedColour = self.wildDraw4(currentplayer,clockwise,drawpile)
       return NextNextTurnPlayer ,selectedColour
   
   
def arrange(hand: list[Card]) -> None:
    """Place a hand of cards on the table"""
    
    # for more cards, use small gap between cards
    gap_width = 40 if len(hand) > 15 else (60 if len(hand) > 8 else 110)
    for i, card in enumerate(hand):
        card.set_pos(100 + i*gap_width, 600)   