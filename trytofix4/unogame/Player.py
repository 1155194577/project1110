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
    
    def printHand(self,frontcard,currentColour,isdebugging):
        for index,card in enumerate(self.hand):
            if isinstance(self,Human):
               if self.IsvalidCard(card,frontcard,currentColour):
                   print([index],[card],end=" ")
               elif not self.IsvalidCard(card,frontcard,currentColour):
                   print(['X'],[card],end=" ")
            elif  isinstance(self,Bot):
                if isdebugging:  
                     if self.IsvalidCard(card,frontcard,currentColour):
                        print([index],[card],end=" ")
                     elif not self.IsvalidCard(card,frontcard,currentColour):
                        print(['X'],[card],end=" ") 
                else:         
                    print(['X'],['X'],end=' ')
   
        print(["D"],["Draw"],end=" ")     
    
    def DiscardCard(self,frontcard,currentColour):
        if self.manually:
            while True:  
               UserOption = input("Enter option: ")
               try: 
                   choice = int(UserOption)
               except ValueError: 
                   print("debug , the input value cannot be converted to integer")
                   if UserOption == 'D' or UserOption == 'd':
                       return 'D'
                   else:
                       print("Invalid input!")
               else: 
                    if choice <= len(self.hand)-1: 
                      print("debug : in range")  
                      selectedCard = self.hand[choice] 
                      if self.IsvalidCard(selectedCard,frontcard,currentColour):
                         print(f"Discarded [{selectedCard}]")
                         self.hand.remove(selectedCard)
                         return selectedCard   
                      else: 
                         print("Invalid Input!")
                    else:
                        print("Invalid Input (Out of Range)!") 
                      
        else: 
            print(self.name)
            for card in self.hand: 
                if self.IsvalidCard(card,frontcard,currentColour): 
                    print("[debug] Computer Chose",card)
                    self.hand.remove(card)
                    return card 
            if not self.HasValidCard(frontcard,currentColour):
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