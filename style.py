
black_theme = False


def refresh():
    global BRIGHT, BRIGHTEST, BRIGHTBRIGHT, ICON, DARK, DARKDARK, DARKEST
    RAYWHITEWHITE = (250, 250, 250, 255)
    DARKDARKGRAY = (50, 50, 50, 255)

    BRIGHTEST = (0,0,0,255) if black_theme else (255,255,255,255)
    BRIGHT = (80,80,80,255) if black_theme else (245,245,245,255)

    DARKEST = (255,255,255,255) if black_theme else (0,0,0,255)
    DARK = (245,245,245,255) if black_theme else (80,80,80,255)

    BRIGHTBRIGHT = DARKDARKGRAY if black_theme else RAYWHITEWHITE
    DARKDARK = RAYWHITEWHITE if black_theme else DARKDARKGRAY

    ICON = 'logowhite' if black_theme else 'logoblack'

refresh()

def changeblack(opo: bool):
    global black_theme
    black_theme = opo
    refresh()
