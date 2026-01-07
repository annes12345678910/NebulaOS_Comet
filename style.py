import ultimateraylib as rl

black_theme = False

RAYWHITEWHITE = rl.make_color(250, 250, 250, 255)
DARKDARKGRAY = rl.make_color(50, 50, 50, 255)


BRIGHTEST = rl.BLACK if black_theme else rl.WHITE
BRIGHTBRIGHT = DARKDARKGRAY if black_theme else RAYWHITEWHITE
BRIGHT = rl.DARKGRAY if black_theme else rl.RAYWHITE
ICON = 'logowhite' if black_theme else 'logoblack'

def refresh():
    global BRIGHT, BRIGHTEST, BRIGHTBRIGHT, ICON
    BRIGHTEST = rl.BLACK if black_theme else rl.WHITE
    BRIGHTBRIGHT = DARKDARKGRAY if black_theme else RAYWHITEWHITE
    BRIGHT = rl.DARKGRAY if black_theme else rl.RAYWHITE
    ICON = 'logowhite' if black_theme else 'logoblack'

def changeblack(opo: bool):
    global black_theme
    black_theme = opo
    refresh()
