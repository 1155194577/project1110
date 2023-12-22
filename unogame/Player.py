import random
from Cards import *


class Player():
    def __init__(self, name, manually) -> None:
        self.name = name
        self.hand = []
        self.CurrentNoOfCard = len(self.hand)
        self.prev = None
        self.next = None
        self.manually = manually

    def IsvalidCard(self, CardInHand, frontcard, currentColour):
        """This method check whether a card is valid to discard"""
        if CardInHand.color.value == 5:  # It is always valid to discard WildCard
            return True
        # If the last player discard WildCard , then it is valid to discard the
        # selected colour
        if frontcard.color.value == 5 and CardInHand.color == currentColour:
            return True
        # if the last player discard numbercard ,then it is valid to discard
        # Same Color/same number card.
        if CardInHand.color == frontcard.color or CardInHand.value == frontcard.value:
            return True
        else:
            return False

    def HasValidCard(self, frontcard, currentColour):
        """This method call the IsvalidCard() method to check whether the player has valid card to discard"""
        for card in self.hand:
            if self.IsvalidCard(card, frontcard, currentColour):
                return True
        return False

    def printHand(self, frontcard, currentColour, isdebugging):
        """This method print out the hand of players"""
        for index, card in enumerate(self.hand):
            if isinstance(self, Human):
                if self.IsvalidCard(card, frontcard, currentColour):
                    print([index], [card], end=" ")
                elif not self.IsvalidCard(card, frontcard, currentColour):
                    print(['X'], [card], end=" ")
            elif isinstance(self, Bot):
                if isdebugging:
                    if self.IsvalidCard(card, frontcard, currentColour):
                        print([index], [card], end=" ")
                    elif not self.IsvalidCard(card, frontcard, currentColour):
                        print(['X'], [card], end=" ")
                else:
                    print(['X'], ['X'], end=' ')

        print(["D"], ["Draw"], end=" ")

    def DiscardCard(self, frontcard, currentColour):
        """This method allow player to discard card. Whether discard automatically or not depends on the self.manually flag"""
        if self.manually:
            while True:
                UserOption = input("Enter option: ")
                try:
                    choice = int(UserOption)
                except ValueError:
                    print("The input value cannot be converted to integer!")
                    if UserOption == 'D' or UserOption == 'd':
                        return 'D'
                    else:
                        print("Invalid input!")
                else:
                    if choice <= len(self.hand) - 1:
                        selectedCard = self.hand[choice]
                        if self.IsvalidCard(
                                selectedCard, frontcard, currentColour):
                            print(f"{self.name} Discarded [{selectedCard}]")
                            self.hand.remove(selectedCard)
                            return selectedCard
                        else:
                            print("Invalid Input!")
                    else:
                        print("Invalid Input!")

        else:
            for card in self.hand:
                if self.IsvalidCard(card, frontcard, currentColour):
                    print(f"{self.name} Discard {card}")
                    self.hand.remove(card)
                    return card
            if not self.HasValidCard(frontcard, currentColour):
                return 'D'

    def ChooseColour(self):
        """This method allow player to choose card via user input or random choice  """
        if self.manually:
            while True:
                try:
                    UserInput = input("Choose a color [1:R, 2:Y , 3:B , 4:G]:")
                    ChosenColor = int(UserInput)
                    if ChosenColor in [1, 2, 3, 4]:
                        break
                    else:
                        print("Invalidl Input! Out of range!")
        ##    ChosenColor = int(input("Choose a color [1:R , 2:Y , 3:B , 4:G]: "))
                except ValueError:
                    print("InValid Input!")

        else:
            ChosenColor = random.randint(1, 4)

        for color in Color:
            if color.value == ChosenColor:
                return color


class Bot(Player):
    def __init__(self, name, manually=False) -> None:
        super().__init__(name, manually)


class Human(Player):

    def __init__(self, name, manually=True) -> None:
        super().__init__(name, manually)

