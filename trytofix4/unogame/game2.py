from Deck import *
from Player import *
from Cards import *
import pygame
import argparse
from globals import *
from pygame.transform import smoothscale_by
from pygame.image import load
from shadow_font import *
from color_tools import ColorPicker


class UnoGame:
    def __init__(self,drawpile,discardpile,maxNoOfplayer) -> None:
        self.players = []  ## a list that contain all players
        self.drawpile = drawpile
        self.discardpile = discardpile
        self.Clockwise = True ## the direction of discarding card (default as Clockwise)
        self.skipturn = False ## a flag that signal turnskipping
        self.turn = 0 ## integer , record the no of turn elapsed
        self.currentcolor = None
        
        
        ### GUI MODE ## 
        self.gui = True 
        self.screen = None
        self.background_image = None
        self.discard_area = None
    def CreatePlayers(self,HumanName="Johnny",NoOfBot=3):
        """This method create a list of player and convert it into LinkedLIst"""
        def ListToLinkedList(players): 
            """A helper function that Convert a List to Linked List"""
            if len(players) == 0: 
               return None 
            head = players[0]
            current = head
            for i in range(1,len(players)):
              new_player = players[i]
              current.next = new_player
              new_player.prev = current 
              current = current.next 
            current.next = head
            head.prev = current
            return head     
          
        self.players.append(Human(HumanName,True))
        print(f"Initializing {NoOfBot} Bots...")     
        for i in range(NoOfBot):
          self.players.append(Bot(f"Bot {i+1}",False)) 
        head = ListToLinkedList(self.players)
        return head
     
    def IsGameEnd(self):
        for player in self.players: ## iterate through hand of players ,
           if len(player.hand) == 0: ## if player discard all card 
              print(f"{player.name} win!") ## win 
              return True
        if len(self.drawpile.cards) == 0: ## if all cards are drawn ,
              print("All card Are Drawn! Game End!")
              return True
        else:
           return False 
    
    def NextTurn(self,currentplayer,clockwise):
        """This method is called when a turn is ended. Node are tranverse depending on
         clockwise and skipturn. 
        """
        if clockwise:  ## if clockwise => next person/anti-clockwise=>prev person
            return currentplayer.next
        else: 
            return currentplayer.prev   
                
    def DrawCards(self,player,n):
        cards = self.drawpile.deal_cards(n)
        for card in cards:
            player.hand.append(card)
        print(f"[Debug]: {player.name} drawn {cards}") 
        
    def IsActionCard(self,card):
         action = card.value.value 
         if action not in range(0,10):
           return True 
         else:
             return False 
    
    def UseActionCard(self,currentplayer,card,gui):
        ActionName = card.value.name 
        CardColorNumber = card.color.value 
        NextTurnPlayer = None 
        selectedColor = None 
        ## ActionName can be skip,draw2,draw4,reverse,card
        ## CardColorNumber = 5 is WILD
        print(ActionName)
        if ActionName == "skip":
            NextTurnPlayer = card.play(currentplayer,self.Clockwise)     
        elif ActionName == "draw2":
            NextTurnPlayer = card.play(currentplayer,self.Clockwise,self.drawpile)
        elif ActionName == "reverse":
            NextTurnPlayer = card.play(currentplayer,self.Clockwise)
            self.Clockwise = not self.Clockwise
        if CardColorNumber == 5: ## when Colour is WILD
            if ActionName == "draw4" and gui==False: 
                  NextTurnPlayer ,selectedColor = card.play(currentplayer,self.Clockwise,self.drawpile)
            elif ActionName == 'draw4' and gui == True:    
                 NextTurnPlayer = self.NextTurn(currentplayer,self.Clockwise)
                 NextTurnPlayer = self.NextTurn(NextTurnPlayer,self.Clockwise)
                 selectedColor = "PickInGui"
            elif ActionName == "card" and gui == False:
                NextTurnPlayer , selectedColor = card.play(currentplayer,self.Clockwise,self.drawpile)
            elif ActionName == "card" and gui == True:
                 NextTurnPlayer = self.NextTurn(currentplayer,self.Clockwise)
                 selectedColor = "PickInGui"
        return NextTurnPlayer , selectedColor             
    def UseNumberCard(self,currentplayer,card):
        NextTurnPlayer = card.play(currentplayer,self.Clockwise)              
        return NextTurnPlayer               
    def startConsole(self):
        if False:
          print("Running in Console Mode")
          user_name = input("What is your name?")
    
          while True: 
            NoofBot = int(input("How many bot do you wanna play with?"))
            if NoofBot in range(1,4): 
                break 
            else: 
                print("Invalid input! Valid No : 1,2,3") 
        
        self.drawpile.build_deck()
        self.drawpile.shuffle()
        head = self.CreatePlayers()
        for player in self.players:
            self.DrawCards(player,HAND_SIZE) ## the 7 is hard-cored , to be amended
            print(player.manually)
        currentPlayer = head 
        currentcolor = None 
        selectedcolor = None 
        
        
        FrontCard = self.drawpile.deal_cards(1)[0]
        while FrontCard.color.value == 5:
            print("drawn",FrontCard)
            self.drawpile.cards.append(FrontCard)
            self.drawpile.shuffle()
            print("shuffled")
            FrontCard = self.drawpile.deal_cards(1)[0]
        self.discardpile.cards.append(FrontCard)
        
        self.currentcolor = FrontCard.color      ## Note that this line of code assume the first FrontCard is not WILD
        while True: 
            if self.IsGameEnd():
                break 
            self.turn += 1 
            FrontCard = self.discardpile.cards[-1]
            
            if FrontCard.color.value != 5: 
                self.currentcolor = FrontCard.color 
            else: 
                self.currentcolor = selectedcolor 
                
            print(f"Turn {self.turn}: This is {currentPlayer.name}'s turn.\nDiscard Pile: {FrontCard} Current Color: {self.currentcolor.name}, DrawPile : {len(self.discardpile.cards)}, Clockwise = {self.Clockwise}")
            if currentPlayer.HasValidCard(FrontCard,self.currentcolor) or self.currentcolor in [card.color for card in currentPlayer.hand]:
                currentPlayer.printHand(FrontCard,self.currentcolor)
                selectedCard = currentPlayer.DiscardCard(FrontCard,self.currentcolor)
                if selectedCard != 'D': 
                  if self.IsActionCard(selectedCard):
                     NextTurnPlayer , selectedcolor = self.UseActionCard(currentPlayer,selectedCard,False) 
                     print(NextTurnPlayer,selectedcolor)
                     currentPlayer = NextTurnPlayer
                     if selectedcolor is not None: 
                         currentcolor = selectedcolor
                  else:  ## numberCard 
                     NextTurnPlayer = self.UseNumberCard(currentPlayer,selectedCard)
                     currentPlayer = NextTurnPlayer
                  self.discardpile.cards.append(selectedCard)   
                else:
                    self.DrawCards(currentPlayer,1) 
                    currentPlayer = self.NextTurn(currentPlayer,self.Clockwise)     
            else: 
              print(f"The Player {currentPlayer.name} has no ValidCard!")
              self.DrawCards(currentPlayer,1)
              if not currentPlayer.HasValidCard(FrontCard,self.currentcolor): 
                NextTurnPlayer  = self.NextTurn(currentPlayer,self.Clockwise) 
                currentPlayer = NextTurnPlayer
    def BetterGUI(self,screen_width=1080,screen_height=810): ## this function try to combine gui mode and console mode 
            print("Running in GUI mode.")
            # Initialize Pygame
            pygame.init()
            clock = pygame.time.Clock()
           
            #Set up the screen 
            screen = pygame.display.set_mode((screen_width,screen_height))  ## the screen
            
            ##Load Background image 
            background_image = smoothscale_by(load(BACKGROUND_IMAGE).convert(),BACKGROUND_SCALE) ## bg image
            discard_area = DiscardArea(DISCARD_AREA_IMAGE,x=100,y=100)  
            
            ##Build the deck of cards 
            draw_pile_image = smoothscale_by(load(UNO_BACK_IMAGE).convert_alpha(),CARD_SCALE)
            draw_pile_rect =  draw_pile_image.get_rect(topleft=(850,200))
            self.drawpile.build_deck("gui")
          
            ## initialize players 
            head = self.CreatePlayers()
            for player in self.players:
               self.DrawCards(player,7) ## the 7 is hard-cored , to be amended
            currentPlayer = head 
           
            ## initialize background msuic
            card_drawn_sound = pygame.mixer.Sound("cardPlace1.wav")
            background_sound = pygame.mixer.Sound("along_the_way.ogg")
            background_sound.set_volume(0.5)
            background_sound.play()
            ## Game state ## 
            self.currentcolor = None
            dragging = False
            offset_x = 0
            offset_y = 0
            running = True
            self.Clockwise = True # by default True
            printed = False 
            card_picked = None 
            new_turn = True
            ### color picking ### 
            color_picking = False
            color_picker = ColorPicker(screen_width, screen_height)
            color_picked = None 
            
            ## initialize Font ####
            heading_font = ShadowFont("Arial",size=50,shadow_offset=5,bold=True)
            label_font = ShadowFont(ROBOTO_FONT, sysfont=False, bold=True)
            heading = heading_font.render("UNO Card Game")
            player_label = label_font.render(currentPlayer.name)
            current_label = player_label
            
            ###### Get Front card from drawpile #####
            FrontCard = self.drawpile.deal_cards(1)[0]
            FrontCard.rect.x , FrontCard.rect.y = 300,300
            self.discardpile.add(FrontCard)
            self.currentcolor = FrontCard.color 
           ### print(f"[debug], {FrontCard} drawn , color is {FrontCard.color}" )
            while running:
            ########### Draw everything ##############
              if self.IsGameEnd():
                  break 
              
              screen.blit(background_image,(0,0)) #Background image
              screen.blit(heading, ((screen_width - heading.get_width()) // 2, 15)) ## heading
              screen.blit(discard_area.image, discard_area.rect) ## discard area
              self.discardpile.draw(screen) ## draw the discard_pile sprite group
              if len(self.drawpile.cards) > 0: 
                 screen.blit(draw_pile_image,draw_pile_rect) ## drawpile
                 
              arrange(currentPlayer.hand)  ## arrange player hand 
              screen.blit(current_label,(110,550)) ## show player name
              
            ###########console mode stuff #############
              FrontCard = self.discardpile.sprites()[-1]
              if FrontCard.color.value != 5: ## if the color is not WILD
                  self.currentcolor = FrontCard.color 
              else:
                  self.currentcolor = color_picked
                      
              if self.currentcolor is not None and new_turn:   
               print(f"Turn {self.turn}: This is {currentPlayer.name}'s turn.\n Discard Pile: {FrontCard} Current Color: {self.currentcolor.name}, Drawpile : {len(self.discardpile.sprites())} , Clockwise : {self.Clockwise}")
               currentPlayer.printHand(FrontCard,self.currentcolor)
               self.turn += 1
               new_turn = False 
              if True:
                  
            ###############event handling ###############
               for event in pygame.event.get():
                if event.type == pygame.QUIT: ## if quit then end loop
                  running = False 
                  
                elif event.type == pygame.MOUSEBUTTONDOWN: ## if some button on the mouse is clicked
                    
                   if event.button == 1:  ## if left mouse is clicked
                      if color_picking:
                        color_picked = color_picker.select()
                        if color_picked: ## if mouse click color plate
                            color_picking = False
                            print(color_picked)
                            new_turn = True 
                      if draw_pile_rect.collidepoint(event.pos): ## if mouse click draw_pile
                           # print("[Debug] The draw_pile is clicked!")
                            self.DrawCards(currentPlayer,1)
                            card_drawn_sound.play()
                            currentPlayer = self.NextTurn(currentPlayer,self.Clockwise)
                            current_label = label_font.render(currentPlayer.name) ## change the label to nextPlayer
                            
                      for card in currentPlayer.hand:
                            if card.rect.collidepoint(event.pos): ## if mouse click any of the card 
                                #print(f"The card {card} is picked!")
                                Isvalid = currentPlayer.IsvalidCard(card,FrontCard,self.currentcolor)
                                print(Isvalid)
                                dragging = True
                                offset_x = event.pos[0] - card.rect.x
                                offset_y = event.pos[1] - card.rect.y
                                card_picked = card
                elif event.type == pygame.MOUSEBUTTONUP: ## elif some button is released 
                    if event.button == 1: 
                        dragging = False
                if card_picked is not None:
                  print("debug",card_picked)  
                  bounding_box = card_picked.rect.inflate(6, 6)
                  pygame.draw.rect(screen, BLUE, bounding_box, 3, border_radius=10)             
                        
                        
              if dragging:
                   card_picked.rect.x = pygame.mouse.get_pos()[0] - offset_x
                   card_picked.rect.y = pygame.mouse.get_pos()[1] - offset_y
                     
                   if discard_area.rect.contains(card_picked.rect): 
                            if Isvalid: 
                               if not card_picked.discarded:
                                currentPlayer.hand.remove(card_picked)
                                card_picked.discarded = True
                                discard_top = card_picked
                                
                               if self.IsActionCard(card_picked): 
                                  NextTurnPlayer , selectedcolor = self.UseActionCard(currentPlayer,card_picked,self.gui)
                                  currentPlayer = NextTurnPlayer 
                                  if selectedcolor == "PickInGui": 
                                      color_picking = True 
                                  dragging = False  
                                  new_turn = True
                                    
                               else: ## NumberCard 
                                     NextTurnPlayer = self.UseNumberCard(currentPlayer,card_picked)
                                     currentPlayer = NextTurnPlayer
                                     dragging = False
                                     new_turn = True
                                
                               arrange(currentPlayer.hand)
                               current_label = label_font.render(currentPlayer.name)
                               self.discardpile.add(card_picked)
                               self.discardpile.update()
                                
                               discard_top = card_picked
                               if discard_top:
                                   bounding_box = discard_top.rect.inflate(6, 6)
                                   pygame.draw.rect(screen, BLUE, bounding_box, 3, border_radius=10)    
                            else:
                                print("[Debug] Invalid Card!",card_picked)
                                failure_sound = pygame.mixer.Sound('lose2.wav')
                                failure_sound.play()
                                failure_sound.set_volume(1)
                                pygame.time.wait(int(failure_sound.get_length() )* 50) 

              for card in currentPlayer.hand:
                  screen.blit(card.image, card.rect)   
              self.discardpile.draw(screen)     
              if color_picking: 
                     screen.blit(color_picker.surf,color_picker.rect)
              pygame.display.update()
              pygame.display.flip()     
              clock.tick(FPS)
            pygame.quit()    
            
            
            
                     
               
### client_side ###  
parser = argparse.ArgumentParser(description='UNO Card Game')
parser.add_argument('-m', '--mode', choices=['console', 'gui'],
                    default='console', help='Select a mode (console, gui).')
args = parser.parse_args()

if __name__ == "__main__":             
  drawpile = DrawPile()
 ##drawpile.shuffle()
  discardpile = DiscardPile()
  print(drawpile,discardpile)
  Game = UnoGame(drawpile,discardpile,3)
  if args.mode == "console":
   Game.startConsole()
  elif args.mode == "gui":
    Game.BetterGUI()


