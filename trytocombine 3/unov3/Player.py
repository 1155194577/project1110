import random 
from Cards import *
class Player(): 
    def __init__(self,name,manually) -> None:
        self.name = name
        self.hand = []
        self.CurrentNoOfCard = len(self.hand)
        self.prev = None
        self.next = None 
        self.manually = manually
    def IsvalidCard(self,CardInHand,frontcard,currentColour):
        if CardInHand.color.value == 5: ## It is always valid to discard WildCard 
          return True 
        if frontcard.color.value == 5 and  CardInHand.color == currentColour: ## If the last player discard WildCard , then it is valid to discard the selected colour    
           return True 
        if CardInHand.color == frontcard.color or CardInHand.value == frontcard.value: ## if the last player discard numbercard ,then it is valid to discard Same Color/same number card.
           return True
        else:
           return False
    
    def HasValidCard(self,frontcard,currentColour):
        for card in self.hand: 
            if self.IsvalidCard(card,frontcard,currentColour):
                return True
        return False
    
    def printHand(self,frontcard,currentColour):
        for index,card in enumerate(self.hand):
            if self.IsvalidCard(card,frontcard,currentColour):
                print([index],[card],end=" ")
            else:
                print(["X"],[card],end=" ") 
            
        print(["D"],["Draw"],end=" ")     
    
    def DiscardCard(self,manually,frontcard,currentColour):
        if manually:
            while True:  
              UserOption = input("Enter option: ")
              if UserOption != 'D':
                selectedCard = self.hand[int(UserOption)]
                if self.IsvalidCard(selectedCard,frontcard,currentColour):
                  print(f"Discarded [{selectedCard}]")
                  self.hand.remove(selectedCard)
                  return selectedCard   
              elif UserOption == 'D': 
                return 'D'  
  
                        
              
    def ChooseColour(self):
        if self.manually:
          ChosenColor = int(input("Choose a color [1:R , 2:Y , 3:B , 4:G]: "))
        else: 
            ChosenColor = random.randint(1,4)  
        for color in Color:
            if color.value == ChosenColor: 
                print(color.name) 
                return color
        
class Bot(Player):
    def __init__(self, name,manually) -> None:
        super().__init__(name,manually)


        
class Human(Player):
  
    def __init__(self, name,manually) -> None:
        super().__init__(name,manually)       

    def __str__(self) -> str:
        return "Human"