from enum import Enum
from pygame.sprite import Sprite
import pygame 
from globals import ISDEBUGGING
class Color(Enum):
    """An enumeration of UNO card colors."""
    RED = 1
    YELLOW = 2
    BLUE = 3
    GREEN = 4
    WILD = 5
    
Value = Enum('Value', 'C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 skip reverse draw2 draw4 card', start=0)


class Card(Sprite):
    """
        A class representing a ship
        Attributes:
        color (Color) : the color of the card
        value (Value) : the value of the card
        discarded (bool) : whether the card is discarded
        hovered (bool) : whether the card is hovered by mouse  (GUI)
    """
    def __init__(self,color,value) -> None:
        
        """  Initialize the value of the card object  """
        super().__init__()
        self.color = color
        self.value = value 
        self.discarded = False 
        self.hovered = False
           
    def set_image(self,image):
        
        """ A setter that set image by input """
        self.image = image
        self.rect = self.image.get_rect()    
        return self 
    
    def set_pos(self,x,y):
        
        
        """A setter taht set position by input x y"""
        self.rect.topleft = (x,y)
        return self 
        
    def __repr__(self):
        """return the __str__() value """
        return self.__str__()

    def __str__(self):
        """a string that represent the card number and card value by two words , e.g B6 , G9"""
        special = True if self.value.value > Value.C9.value else False
        if self.color == Color.WILD and self.value.value < Value.draw4.value:
            return str(None)  # no such card type
        #return str(self.color)[6:] + ' ' + str(self.value)[6:]  # full name
        return str(self.color)[6] + str(self.value)[6 if special else 7]  # abbreviation
    def Next(self,currentPlayer,Clockwise): 
        """A function that determine who is going to play next"""
        if Clockwise: 
            return currentPlayer.next
        else: 
            return currentPlayer.prev   
              
    def play(self,currentPlayer,Clockwise):
        """A function that return the player next turn"""
        NextTurnPlayer = self.Next(currentPlayer,Clockwise)
        return NextTurnPlayer
        
class ActionCard(Card):
    def __init__(self,color,value) -> None:
     """
       A class that define the Action card class. It is a inheritance of Card object
       New Attributes:     action (str) 
    """
     super().__init__(color,value)
     
     self.action = value.name ## actions can be skip,reverse,draw2,draw4,card
    
class Reverse(ActionCard):
    """A class that define the reverse card class , it is a inheritance of ActionCard object"""
    def __init__(self, color, value) -> None:
        super().__init__(color, value)
    def Reverse(self,currentplayer,clockwise):
        """This function is called to negate the current clockwise flag."""
        clockwise = not clockwise  
        NextTurnPlayer = self.Next(currentplayer,clockwise)
        return NextTurnPlayer
    def play(self,currentplayer,clockwise): 
        """This function override the superclass function and reverse the current playing direction"""
        print("Direction is reversed!")
        NextTurnPlayer = self.Reverse(currentplayer,clockwise)
        return NextTurnPlayer
     
class Skip(ActionCard):
    """A class that define the skip card class , it is an inheritance of the ActionCard object"""
    def __init__(self, color, value) -> None:
        super().__init__(color, value)
    def skip(self,currentplayer,clockwise):
        """This function is called to skip the next player and give the next next player as return value"""
        print("The turn is Skip!!")
        if clockwise:  ## if clockwise => next person/anti-clockwise=>prev person
            return currentplayer.next.next
        else: 
            return currentplayer.prev.prev 
 
    def play(self,currentplayer,clockwise): 
        NextTurnPlayer = self.skip(currentplayer,clockwise)
        return NextTurnPlayer 
  
class Draw2(Skip):
    """
       A class that define the Draw2 class. Since the nextturn player is skipped , the Draw2 class is 
       inheriting the Skip card to enhance code reuse 
    
    """
    def __init__(self, color, value) -> None:
        super().__init__(color, value)
    
    @staticmethod    
    def drawNcard(player,n,drawpile):     
        """This is a utility/helper function that allow player to draw a total of n card , where the value of n depends on the card"""
        cards = drawpile.deal_cards(n)
        for card in cards:
            player.hand.append(card)   
        if ISDEBUGGING:    
          print(f"[Debug]: {player.name} drawn {cards}")    
     
    def draw2(self,currentplayer,clockwise,drawpile):
        """
        This function call the static drawNcard function and draw2 card to the nextturn player , also , the nextturn player is skipped ,
        so the next next turn player is returned 
        """
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
    """This is a class that define the wildCard class """
    def __init__(self, color, value) -> None:
        super().__init__(color, value)      
    
    def ChangeColour(self,player,clockwise,drawpile):   
        """This function allow player to change colour by user"""
        selectedColor = player.ChooseColour()
        print(f"The colour is changed to {selectedColor.name}")
        NextTurnPlayer = self.Next(player,clockwise)
        return NextTurnPlayer,selectedColor
            
    def play(self,player,clockwise,drawpile):
        """This function allow player to change colour by calling the helper ChangeColour function"""
        NextTurnPlayer , selectedColor = self.ChangeColour(player,clockwise,drawpile) 
        return NextTurnPlayer, selectedColor

class WildDraw4(Draw2,WildCard):
    """This is a class that define the wildCard class , it inherits Draw2 and Wildcard"""
    def __init__(self, color, value) -> None:
        super().__init__(color, value)
    def wildDraw4(self,currentplayer,clockwise,drawpile):
        """This is a function that give four card to the next player and skip"""
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
        if not card.hovered:
          card.set_pos(100 + i*gap_width, 600)   
        else:
          card.set_pos(100 + i*gap_width, 600-20)     