import sys
import config

if config.backend == 0:
    import ultimateraylib as rl
elif config.backend == 1:
    import pygame
    pygame_screen: pygame.Surface
elif config.backend == 2:
    import pyglet
    pyglet_window: pyglet.window.BaseWindow

else:
    print(f"Error: Invalid Backend {config.backend}")
    sys.exit(600)

def init(title="NebulaOS Comet"):
    if config.backend == 0:
        rl.set_config_flags(rl.FLAG_WINDOW_RESIZABLE)
        rl.init_window(title=title)
    elif config.backend == 1:
        global pygame_screen
        pygame_screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption(title)
    elif config.backend == 2:
        global pyglet_window
        pyglet_window = pyglet.window.Window(800, 600, title)
