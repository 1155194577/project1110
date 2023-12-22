import pygame
from Deck import *
from Player import *
from Cards import *
import argparse
from globals import *
from pygame.transform import smoothscale_by
from pygame.image import load
from shadow_font import *
from color_tools import ColorPicker
import time


class UnoGame:
    def __init__(
            self,
            drawpile,
            discardpile,
            maxNoOfplayer=MAXNOOFPLAYER) -> None:
        self.players = []  # a list that contain all players
        self.drawpile = drawpile
        self.discardpile = discardpile
        # the direction of discarding card (default as Clockwise)
        self.Clockwise = True
        self.turn = 0  # integer , record the no of turn elapsed
        self.currentcolor = None

        ### GUI MODE ##
        self.gui = True
    @staticmethod
    def ListToLinkedList(players)->Player:
        """A helper/utility function that Convert a List to Linked List"""
        if len(players) == 0:
            return None
        head = players[0]
        current = head
        for i in range(1, len(players)):
            new_player = players[i]
            current.next = new_player
            new_player.prev = current
            current = current.next
        current.next = head
        head.prev = current
        return head

    def CreatePlayers(self, HumanName=DEFAULTNAME, NoOfBot=NOOFBOTS)->Player:
        """This method create a list of player and convert it into LinkedLIst"""
        self.players.append(Human(HumanName, True))
        if ISDEBUGGING:
            print(f"Initializing {NoOfBot} Bots...")
        for i in range(NoOfBot):
            self.players.append(Bot(f"Bot {i+1}", False))
        head = self.ListToLinkedList(self.players)
        return head

    def IsGameEnd(self)->Player:
        """This method determine whether the game is ended or not"""
        for player in self.players:  # iterate through hand of players ,
            if len(player.hand) == 0:  # if player discard all card
                print(f"{player.name} win!")  # win
                return True
        if len(self.drawpile.cards) == 0:  # if all cards are drawn ,
            print("All card Are Drawn! Game End!")
            return True
        else:
            return False

    def NextTurn(self, currentplayer, clockwise)->Player:
        """This method is called when a turn is ended. Node are tranverse depending on
         clockwise and skipturn.
        """
        if clockwise:  # if clockwise => next person/anti-clockwise=>prev person
            return currentplayer.next
        else:
            return currentplayer.prev
            

    def DrawCards(self, player, n)->None:
        """This method assign card to a particular player"""
        cards = self.drawpile.deal_cards(n)
        for card in cards:
            player.hand.append(card)

        if ISDEBUGGING:
            print(f"[Debug]: {player.name} drawn {cards}")

        elif not ISDEBUGGING:
            if isinstance(player, Human):
                print(f" {player.name} drawn {cards}")
            elif isinstance(player, Bot):
                print(f"{player.name} drawn {len(cards)} card(s)")

    def IsActionCard(self, card)->bool:
        """This method check whether a card is actioncard or not"""
        action = card.value.value
        return action not in range(0, 10)
         

    def UseActionCard(self, current_player, card, gui)->[Player,Color]:
      """This method is called when an ActionCard is played. It will return the next turn player and selected color (if a wildcard is played) to the client side"""

      action_name = card.value.name
      next_turn_player = None
      selected_color = None

      # ActionName can be skip, draw2, draw4, reverse, card
      # CardColorNumber = WILD
      # Match action_name with different cases
      match action_name:
        case "skip":
            # Execute card.play() for skip action
            next_turn_player = card.play(current_player, self.Clockwise)
        case "draw2":
            # Execute card.play() for draw2 action
            next_turn_player = card.play(current_player, self.Clockwise, self.drawpile)
        case "reverse":
            # Execute card.play() for reverse action and update clockwise direction
            next_turn_player = card.play(current_player, self.Clockwise)
            self.Clockwise = not self.Clockwise
        case "draw4":
            match gui:
                case False:
                    # Execute card.play() for draw4 action without GUI
                    next_turn_player, selected_color = card.play(current_player, self.Clockwise, self.drawpile)
                case True:
                    # Execute card.play() for draw4 action with GUI and select color in GUI
                    next_turn_player = self.NextTurn(current_player, self.Clockwise)
                    next_turn_player = self.NextTurn(next_turn_player, self.Clockwise)
                    selected_color = "PickInGui"
        case "card":
            match gui:
                case False:
                    # Execute card.play() for card action without GUI
                    next_turn_player, selected_color = card.play(current_player, self.Clockwise, self.drawpile)
                case True:
                    # Execute card.play() for card action with GUI and select color in GUI
                    next_turn_player = self.NextTurn(current_player, self.Clockwise)
                    selected_color = "PickInGui"

      return next_turn_player, selected_color


    def UseNumberCard(self, currentplayer, card)->Player:
        """This method is called when a NumberCard is played. IT will return the Next turn player """
        return card.play(currentplayer, self.Clockwise)

    def startConsole(self)->None:
        """This is the main loop of Console mode"""
        user_name = DEFAULTNAME
        if not ISDEBUGGING:  # prompt user input
            print("Running in Console Mode (non-debug mode)")
            user_name = input("What is your name?")
            while True:
                UserInput = input("How many Bot do you wanna play with?")
                try:
                    NoofBot = int(UserInput)
                except ValueError:
                    print("Invalid input! Expected integer!")
                else:
                    if NoofBot in range(1, MAXNOOFPLAYER):
                        break
                    else:
                        allow_bot = ",".join([str(i)
                                             for i in range(1, MAXNOOFPLAYER)])
                        print(
                            f"Invalid input!allowed Number of Bot:{allow_bot}")
        else:
            print("Running in Console Mode (debug mode)")
        self.drawpile.build_deck()  # build the draw pile
        self.drawpile.shuffle()  # shuffle the pile

        # initialize the players linked list
        head = self.CreatePlayers(HumanName=user_name)
        for player in self.players:
            self.DrawCards(player, HAND_SIZE)
        currentPlayer = head
        currentcolor = None
        selectedcolor = None

        FrontCard = self.drawpile.deal_cards(1)[0]
        # We have to ensure that the first card is a coloured Card.
        while FrontCard.color.value == 5:

            if ISDEBUGGING:
                print("[Debug] drawn", FrontCard)

            # if the firstdrawn Card is Wild , put it back to drawpile
            self.drawpile.cards.append(FrontCard)
            self.drawpile.shuffle()  # shuffle it

            if ISDEBUGGING:
                print("[Debug] shuffled")

            FrontCard = self.drawpile.deal_cards(1)[0]  # draw another card
        self.discardpile.cards.append(FrontCard)

        # Note that this line of code assume the first FrontCard is not WILD
        self.currentcolor = FrontCard.color
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
            if currentPlayer.HasValidCard(
                    FrontCard, self.currentcolor) or self.currentcolor in [
                    card.color for card in currentPlayer.hand]:
                currentPlayer.printHand(
                    FrontCard, self.currentcolor, ISDEBUGGING)
                selectedCard = currentPlayer.DiscardCard(
                    FrontCard, self.currentcolor)
                if selectedCard != 'D':
                    if self.IsActionCard(selectedCard):
                        NextTurnPlayer, selectedcolor = self.UseActionCard(
                            currentPlayer, selectedCard, False)
                # print(NextTurnPlayer,selectedcolor)
                        currentPlayer = NextTurnPlayer
                        if selectedcolor is not None:
                            currentcolor = selectedcolor
                    else:  # numberCard
                        NextTurnPlayer = self.UseNumberCard(
                            currentPlayer, selectedCard)
                        currentPlayer = NextTurnPlayer
                    self.discardpile.cards.append(selectedCard)
                else:
                    self.DrawCards(currentPlayer, 1)
                    currentPlayer = self.NextTurn(
                        currentPlayer, self.Clockwise)
            else:
                if ISDEBUGGING:
                    print(
                        f"[Debug] The Player {currentPlayer.name} has no ValidCard!")
                self.DrawCards(currentPlayer, 1)
                if not currentPlayer.HasValidCard(
                        FrontCard, self.currentcolor):
                    NextTurnPlayer = self.NextTurn(
                        currentPlayer, self.Clockwise)
                    currentPlayer = NextTurnPlayer

    def BetterGUI(self, screen_width=1080, screen_height=810)->None:
        """This method is the main loop of GUI mode"""
        print("Running in GUI mode.")
        # Initialize Pygame
        pygame.init()
        clock = pygame.time.Clock()

        # Set up the screen
        screen = pygame.display.set_mode(
            (screen_width, screen_height), pygame.SRCALPHA)  # the screen

        # Load Background image
        background_image = smoothscale_by(
            load(BACKGROUND_IMAGE).convert(),
            BACKGROUND_SCALE)  # bg image
        discard_area = DiscardArea(DISCARD_AREA_IMAGE, x=100, y=100)

        # Build the deck of cards
        draw_pile_image = smoothscale_by(
            load(UNO_BACK_IMAGE).convert_alpha(), CARD_SCALE)
        draw_pile_rect = draw_pile_image.get_rect(topleft=(850, 200))
        self.drawpile.build_deck("gui")

        # initialize players
        head = self.CreatePlayers()
        for player in self.players:
            self.DrawCards(player, HAND_SIZE)
        currentPlayer = head

        # initialize background msuic
        hover_sound = pygame.mixer.Sound(HOVERSOUND)
        failure_sound = pygame.mixer.Sound(FAILURESOUND)
        change_colour_sound = pygame.mixer.Sound(CHANGECOLOUR)
        card_place_sound = pygame.mixer.Sound(CARDPLACEDSOUND)
        card_drawn_sound = pygame.mixer.Sound(CARDDRAWNSOUND)
        background_sound = pygame.mixer.Sound(BACKGROUND_MUSIC)
        endgame_music = pygame.mixer.Sound(ENDGAMEMUSIC)
        card_place_sound.set_volume(1)
        background_sound.set_volume(0.3)
        ## Game state ##
        self.currentcolor = None
        dragging = False
        offset_x = 0
        offset_y = 0
        running = True
        self.Clockwise = True  # by default True
        printed = False
        card_picked = None
        new_turn = True
        ### color picking ###
        color_picking = False
        color_picker = ColorPicker(screen_width, screen_height)
        color_picked = None
        gameEnd = False
        ## initialize Font ####
        heading_font = ShadowFont("Arial", size=50, shadow_offset=5, bold=True)
        label_font = ShadowFont(ROBOTO_FONT, sysfont=False, bold=True)
        heading = heading_font.render("UNO Card Game")
        player_label = label_font.render(currentPlayer.name)
        current_label = player_label
        gameEnd_label = heading_font.render("GAME END")
        Clickme_label = heading_font.render("CLick Button To Quit!")
        EndGameHeading = heading_font.render("Merry Christmas!")
        button_rect = pygame.Rect(500, 500, 100, 100)
        ###### Get Front card from drawpile #####
        FrontCard = self.drawpile.deal_cards(1)[0]
        while FrontCard.color.value == 5:
            self.drawpile.add(FrontCard)
            self.drawpile.shuffle()
            FrontCard = self.drawpile.deal_cards(1)[0]

        FrontCard.rect.x, FrontCard.rect.y = 300, 300
        self.discardpile.add(FrontCard)
        self.currentcolor = FrontCard.color
        background_sound.play()
        endgame_music.play()
        endgame_music.set_volume(0)
        ### print(f"[debug], {FrontCard} drawn , color is {FrontCard.color}" )
        while running:
            ########### Draw everything ##############
            if self.IsGameEnd():
                gameEnd = True
                background_sound.set_volume(0)
                endgame_music.set_volume(1)
            if not gameEnd:
                screen.blit(background_image, (0, 0))  # Background image
                screen.blit(
                    heading, ((screen_width - heading.get_width()) // 2, 15))  # heading
                screen.blit(
                    discard_area.image,
                    discard_area.rect)  # discard area
                # draw the discard_pile sprite group
                self.discardpile.draw(screen)
                if len(self.drawpile.cards) > 0:
                    screen.blit(draw_pile_image, draw_pile_rect)  # drawpile

                arrange(currentPlayer.hand)  # arrange player hand
                screen.blit(current_label, (110, 550))  # show player name

                if self.currentcolor is not None:
                    screen.blit(
                        label_font.render(
                            self.currentcolor.name), (20, 20))
        ###########console mode stuff #############
            FrontCard = self.discardpile.sprites()[-1]
            if FrontCard.color.value != 5:  # if the color is not WILD
                self.currentcolor = FrontCard.color
            else:
                self.currentcolor = color_picked
            if self.currentcolor is not None and new_turn and ISDEBUGGING:
                print(f"Turn {self.turn}: This is {currentPlayer.name}'s turn.\n Discard Pile: {FrontCard} Current Color: {self.currentcolor.name}, Drawpile : {len(self.discardpile.sprites())} , Clockwise : {self.Clockwise}")
                currentPlayer.printHand(
                    FrontCard, self.currentcolor, ISDEBUGGING)
                self.turn += 1
                new_turn = False
            if True:

                ###############event handling ###############
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # if quit then end loop
                        running = False
                    elif event.type == pygame.MOUSEMOTION:
                        mousepos = pygame.mouse.get_pos()
                        for card in currentPlayer.hand:
                            if card.rect.collidepoint(event.pos):
                                card.hovered = True
                                hover_sound.play()
                                if ISDEBUGGING:
                                    print(
                                        f"[Debug] The card {card} is hovered!")
                            else:
                                card.hovered = False
                            if card.hovered or card.rect.collidepoint(
                                    mousepos):
                                pass
                           ##     print("mouse is hovering on ",card)
                              #  bounding_box = card.rect.inflate(6, 6)
                              #  pygame.draw.rect(screen, BLACK, bounding_box, 3, border_radius=10)

                    elif event.type == pygame.MOUSEBUTTONDOWN:  # if some button on the mouse is clicked

                        if event.button == 1:  # if left mouse is clicked
                            if button_rect.collidepoint(
                                    pygame.mouse.get_pos()):
                                print("button clicked!")
                                running = False

                            if color_picking:
                                color_picked = color_picker.select()
                                if ISDEBUGGING:
                                    print(f"[Debug] Now selecing Color!")
                                if color_picked:  # if mouse click color plate
                                    color_picking = False
                                    if ISDEBUGGING:
                                        print(
                                            f"[Debug] The color {color_picked.name} is selected!")

                                    currentPlayer = self.NextTurn(
                                        currentPlayer, self.Clockwise)
                                    current_label = label_font.render(
                                        currentPlayer.name)  # change the label to nextPlayer
                                    change_colour_sound.play()
                                    new_turn = True
                            if draw_pile_rect.collidepoint(
                                    event.pos):  # if mouse click draw_pile
                                # print("[Debug] The draw_pile is clicked!")
                                self.DrawCards(currentPlayer, 1)
                                card_drawn_sound.play()
                                currentPlayer = self.NextTurn(
                                    currentPlayer, self.Clockwise)
                                current_label = label_font.render(
                                    currentPlayer.name)  # change the label to nextPlayer

                            for card in currentPlayer.hand:
                                if card.rect.collidepoint(
                                        event.pos):  # if mouse click any of the card
                                    #print(f"The card {card} is picked!")
                                    Isvalid = currentPlayer.IsvalidCard(
                                        card, FrontCard, self.currentcolor)
                                  #  print(Isvalid)
                                    dragging = True
                                    offset_x = event.pos[0] - card.rect.x
                                    offset_y = event.pos[1] - card.rect.y
                                    card_picked = card
                    elif event.type == pygame.MOUSEBUTTONUP:  # elif some button is released
                        if event.button == 1:
                            dragging = False

            if dragging:
                card_picked.rect.x = pygame.mouse.get_pos()[0] - offset_x
                card_picked.rect.y = pygame.mouse.get_pos()[1] - offset_y

                if discard_area.rect.contains(card_picked.rect):
                    if Isvalid:
                        if not card_picked.discarded:
                            currentPlayer.hand.remove(card_picked)
                            self.discardpile.add(card_picked)
                            card_picked.discarded = True
                            FrontCard = card_picked

                        if self.IsActionCard(card_picked):
                            NextTurnPlayer, selectedcolor = self.UseActionCard(
                                currentPlayer, card_picked, self.gui)
                            if selectedcolor != "PickInGui":
                                currentPlayer = NextTurnPlayer
                            elif selectedcolor == "PickInGui":
                                color_picking = True
                            dragging = False
                            new_turn = True
                            ##new_turn = True

                        else:  # NumberCard
                            NextTurnPlayer = self.UseNumberCard(
                                currentPlayer, card_picked)
                            currentPlayer = NextTurnPlayer
                            dragging = False
                            new_turn = True
                            card_place_sound.play()
                        arrange(currentPlayer.hand)
                        current_label = label_font.render(currentPlayer.name)
                        self.discardpile.update()

                    else:
                        if ISDEBUGGING:
                            print("Invalid Card!", card_picked)
                        failure_sound.play()
                        failure_sound.set_volume(1)
                        pygame.time.wait(int(failure_sound.get_length()) * 50)

            if isinstance(currentPlayer, Bot):

                print(f"NOw is {currentPlayer.name} turn")
                print("computer thinking")
                if currentPlayer.HasValidCard(
                        FrontCard, self.currentcolor) or self.currentcolor in [
                        card.color for card in currentPlayer.hand]:
                    currentPlayer.printHand(
                        FrontCard, self.currentcolor, ISDEBUGGING)

                    card_picked = currentPlayer.DiscardCard(
                        FrontCard, self.currentcolor)
                    print(card_picked)
                    discard_top = card_picked
                    if card_picked != 'D':
                        card_picked.rect.x, card_picked.rect.y = random.randint(
                            100, 700), random.randint(100, 300)
                    self.discardpile.add(card_picked)
                    self.discardpile.update()
                    if self.IsActionCard(card_picked):
                        NextTurnPlayer, selectedcolor = self.UseActionCard(
                            currentPlayer, card_picked, False)
                        if selectedcolor is not None:
                            color_picked = selectedcolor
                            self.currentcolor = color_picked
                            ###print("The color now is dsadas",self.currentcolor)
                        currentPlayer = NextTurnPlayer
                    else:
                        currentPlayer = self.UseNumberCard(
                            currentPlayer, card_picked)

                    current_label = label_font.render(currentPlayer.name)
                else:
                    if ISDEBUGGING:
                        print(
                            f"[Debug] The Player {currentPlayer.name} has no ValidCard!")
                    self.DrawCards(currentPlayer, 1)
                    if not currentPlayer.HasValidCard(
                            FrontCard, self.currentcolor):
                        NextTurnPlayer = self.NextTurn(
                            currentPlayer, self.Clockwise)
                        currentPlayer = NextTurnPlayer
                        current_label = label_font.render(currentPlayer.name)
            for card in currentPlayer.hand:
                if not gameEnd:
                    screen.blit(card.image, card.rect)
                if card.hovered:
                    bounding_box = card.rect.inflate(6, 6)
                    pygame.draw.rect(
                        screen, BLACK, bounding_box, 10, border_radius=10)
            if not ISDEBUGGING and isinstance(currentPlayer, Bot):
                pygame.draw.rect(screen, BLACK, ((0, 600, 2000, 300)))

            self.discardpile.draw(screen)
            for card in self.discardpile:
                if card == FrontCard and not gameEnd:
                    bounding_box = card.rect.inflate(10, 10)
                    pygame.draw.rect(
                        screen, (255, 255, 0), bounding_box, 15, border_radius=10)
                    pygame.display.flip()
                    #pygame.draw.rect(screen, BLACK, bounding_box, 5, border_radius=10)
            if color_picking and not gameEnd:
                screen.blit(color_picker.surf, color_picker.rect)
            if gameEnd:
                endgame_music.set_volume(1)
                screen.fill((255, 105, 180, 128))
                x = (screen_width - gameEnd_label.get_width()) // 2
                y = (screen_height - gameEnd_label.get_height()) // 2
                screen.blit(gameEnd_label, (x, y))
                screen.blit(Clickme_label, (x - 100, y + 200))
                button_rect.x = x + 450
                button_rect.y = y + 200
                screen.blit(
                    EndGameHeading,
                    ((screen_width - EndGameHeading.get_width()) // 2,
                     15))  # heading
                if button_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(screen, BLUE, button_rect)
                else:
                    pygame.draw.rect(screen, RED, button_rect)
            pygame.display.update()
            clock.tick(FPS)
        pygame.quit()


### client_side ###
parser = argparse.ArgumentParser(description='UNO Card Game')
parser.add_argument(
    '-m',
    '--mode',
    choices=[
        'console',
        'gui',
        'console_debug',
        'gui_debug'],
    default='console',
    help='Select a mode (console, gui).')
args = parser.parse_args()

if __name__ == "__main__":
    drawpile = DrawPile()
    discardpile = DiscardPile()
    Game = UnoGame(drawpile, discardpile, MAXNOOFPLAYER)
    if args.mode == "console":
        ISDEBUGGING = False
        Game.startConsole()
    elif args.mode == "gui":
        ISDEBUGGING = False
        Game.BetterGUI()
    elif args.mode == "console_debug":
        ISDEBUGGING = True
        Game.startConsole()
    elif args.mode == "gui_debug":
        ISDEBUGGING = True
        Game.BetterGUI()
