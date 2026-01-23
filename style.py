import ultimateraylib as rl

black_theme = False

RAYWHITEWHITE = (250, 250, 250, 255)
DARKDARKGRAY = (50, 50, 50, 255)


BRIGHTEST = (0,0,0) if black_theme else (255,255,255)
BRIGHTBRIGHT = DARKDARKGRAY if black_theme else RAYWHITEWHITE
BRIGHT = (80, 80, 80, 255) if black_theme else (245, 245, 245, 255)
ICON = 'logowhite' if black_theme else 'logoblack'

def refresh():
    global BRIGHT, BRIGHTEST, BRIGHTBRIGHT, ICON
    BRIGHTEST = (0,0,0) if black_theme else (255,255,255)
    BRIGHTBRIGHT = DARKDARKGRAY if black_theme else RAYWHITEWHITE
    BRIGHT = (80, 80, 80, 255) if black_theme else (245, 245, 245, 255)
    ICON = 'logowhite' if black_theme else 'logoblack'

def changeblack(opo: bool):
    global black_theme
    black_theme = opo
    refresh()
