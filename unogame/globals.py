import os

# Global constants
FPS = 20
BACKGROUND_SCALE = 0.21
CARD_SCALE = 0.25

###IMAGE ###
BACKGROUND_IMAGE = os.path.join("..", "images", "background1.jpg")
DISCARD_AREA_IMAGE = os.path.join("..", "images", "discard-area1.jpg")
UNO_BACK_IMAGE = os.path.join("..", "images", "UNO-Back.png")
UNO_FRONT_IMAGE = os.path.join("..", "images", "UNO-Front.png")
UNO_ZEROS_IMAGE = os.path.join("..", "images", "UNO-Zeros.png")

## SOUND ##
BACKGROUND_MUSIC = os.path.join("..", "Sound", "bgm.ogg")
CARDDRAWNSOUND = os.path.join("..", "Sound", 'carddrawnsound.wav')
CARDPLACEDSOUND = os.path.join("..", "Sound", 'cardplacesound.wav')
CHANGECOLOUR = os.path.join("..", "Sound", "changecolour.ogg")
FAILURESOUND = os.path.join("..", "Sound", "failureSound.wav")
HOVERSOUND = os.path.join("..", "Sound", "HoverSound.wav")
ENDGAMEMUSIC = os.path.join("..", "Sound", "EndGameMusic.mp3")

## FONT ##
ROBOTO_FONT = os.path.join("..", "fonts", "RobotoCondensed.ttf")
CARD_SIZE = (410, 585)  # pixels
CARD_KEYS = (
    "R1 R2 R3 R4 R5 R6 R7 R8 R9 Wc "
    "Y1 Y2 Y3 Y4 Y5 Y6 Y7 Y8 Y9 Wc "
    "B1 B2 B3 B4 B5 B6 B7 B8 B9 Wd "
    "G1 G2 G3 G4 G5 G6 G7 G8 G9 Wd "
    "Rs Ys Bs Gs Rd Yd Bd Gd Rr Yr "
    "Br Gr R0 Y0 B0 G0"
)
HAND_SIZE = 7
# RGB Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (127, 127, 127)
RED = (212, 1, 0)
YELLOW = (255, 204, 2)
BLUE = (41, 127, 255)
GREEN = (43, 160, 90)
ISDEBUGGING = True
MAXNOOFPLAYER = 4
NOOFBOTS = 3
DEFAULTNAME = "johnny"
