import os
import random
import itertools
import argparse
import pygame
from pygame.transform import smoothscale_by
from pygame.image import load
from globals import *
from unocard import Color, Value, Card, arrange
from cardreader import read_card_images
from deck import build_deck, deal_cards
from discard import DiscardArea
from shadow_font import ShadowFont
from color_tools import ColorPicker


# Parse the command-line arguments
parser = argparse.ArgumentParser(description='UNO Card Game')
parser.add_argument('-m', '--mode', choices=['console', 'gui'],
                    default='console', help='Select a mode (console, gui).')
args = parser.parse_args()


# Define the GUI mode function
def run_gui_mode():
    print("Running in GUI mode.")

    # Initialize Pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Set up the screen
    screen_width = 1080
    screen_height = 810
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Load the background images
    background_image = smoothscale_by(load(BACKGROUND_IMAGE).convert(), BACKGROUND_SCALE)
    discard_area = DiscardArea(DISCARD_AREA_IMAGE, x=100, y=100)
    discard_pile = pygame.sprite.Group()

    # Build the deck of cards
    draw_pile_image = smoothscale_by(load(UNO_BACK_IMAGE).convert_alpha(), CARD_SCALE)
    draw_pile_rect = draw_pile_image.get_rect(topleft=(850, 200))
    draw_pile = build_deck(args.mode)
    
    # Deal each player a hand of cards
    player1 = deal_cards(draw_pile, HAND_SIZE)
    player2 = deal_cards(draw_pile, HAND_SIZE)
    # Set card positions on the table
    arrange(player1)
    arrange(player2)
    
    turn = 1        # current turn
    hand = player1  # hand of cards of current player
    
    heading_font = ShadowFont("Arial", size=50, shadow_offset=5, bold=True)
    label_font = ShadowFont(ROBOTO_FONT, sysfont=False, bold=True)
    heading = heading_font.render('UNO Card Game')
    p1_label = label_font.render('Player 1')
    p2_label = label_font.render('Player 2')
    player_label = p1_label

    color_picker = ColorPicker(screen_width, screen_height)

    # Initialize dragging state and offset
    dragging = False
    offset_x = 0
    offset_y = 0
    card_picked = None    # the card being dragged
    discard_top = None    # the top card of the discard pile

    color_picking = False
    color_picked = None

    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if color_picking:
                        color_picked = color_picker.select()
                        if color_picked: ## if mouse click color plate
                            color_picking = False
                            print(color_picked)
                    else:
                        if draw_pile_rect.collidepoint(event.pos): ## if mouse click draw_pile
                            if len(draw_pile) > 0:
                                card_drawn = deal_cards(draw_pile, 1)[0]
                                hand.append(card_drawn)
                                arrange(hand)
                                print("Drawn", card_drawn)
                                print("Draw pile:", len(draw_pile))

                        for card in hand:
                            if card.rect.collidepoint(event.pos): ## if mouse click any of the card 
                                dragging = True
                                offset_x = event.pos[0] - card.rect.x
                                offset_y = event.pos[1] - card.rect.y
                                card_picked = card

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    #if not color_picking:
                    dragging = False

        if dragging:
            card_picked.rect.x = pygame.mouse.get_pos()[0] - offset_x
            card_picked.rect.y = pygame.mouse.get_pos()[1] - offset_y

        # Check if the mouse is over any card or option surface
        if color_picking:
            rects = color_picker.option_rects
        else:
            rects = [card.rect for card in hand]
            if len(draw_pile) > 0:
                rects += [draw_pile_rect]
        for rect in rects:
            if rect.collidepoint(pygame.mouse.get_pos()):
                # Change the cursor when it is over the surface
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                break
        else:
            # Reset the cursor to the default
            pygame.mouse.set_cursor(*pygame.cursors.arrow)

        if not dragging and card_picked and not card_picked.discarded:
            if discard_area.rect.contains(card_picked.rect): ## if the discard_area contain (card_picked)
                card_picked.discarded = True
                print("Discarded", card_picked)
                hand.remove(card_picked)

                if card_picked.color == Color.WILD:
                    print("Select color for next player.")
                    color_picking = True

                if len(hand) == 0:
                    running = False
                arrange(hand)
                discard_pile.add(card_picked)
                discard_top = card_picked
                print("Discard pile:", len(discard_pile.sprites()))
                turn += 1
                hand = player2 if turn % 2 == 0 else player1
                player_label = p2_label if turn % 2 == 0 else p1_label


        # Draw the background image, draw pile, discard pile
        screen.blit(background_image, (0, 0))
        screen.blit(heading, ((screen_width - heading.get_width()) // 2, 15))
        screen.blit(discard_area.image, discard_area.rect)
        discard_pile.draw(screen)
        if discard_top:
            bounding_box = discard_top.rect.inflate(6, 6)
            pygame.draw.rect(screen, BLUE, bounding_box, 3, border_radius=10)

        if len(draw_pile) > 0:
            screen.blit(draw_pile_image, draw_pile_rect) #(ok)

        # Draw the current player's hand
        screen.blit(player_label, (100, 550))  # OK
        for card in hand:
            screen.blit(card.image, card.rect) ##OK 

        if color_picking:
            screen.blit(color_picker.surf, color_picker.rect)

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

    # Quit the game
    pygame.quit()


# Define the console mode function
def run_console_mode():
    print("Running in console mode.")
    draw_pile = build_deck()
    print(draw_pile)
    print("Draw pile size:", len(draw_pile))


if __name__ == "__main__":
    if args.mode == 'gui':
        run_gui_mode()
    elif args.mode == 'console':
        run_console_mode() 
