import sys
import config

if config.backend == 0:
    import ultimateraylib as rl
elif config.backend == 1:
    import pygame
    pygame_screen: pygame.Surface
elif config.backend == 2:
    import pyglet
    import pyglet.gl as gl
    pyglet_window: pyglet.window.BaseWindow

else:
    print(f"Error: Invalid Backend {config.backend}")
    sys.exit(600)

#    if config.backend == 0: # raylib
#    if config.backend == 1: # pygame
#    if config.backend == 2: # pyglet

def init(title="NebulaOS Comet"):
    if config.backend == 0:
        rl.set_config_flags(rl.FLAG_WINDOW_RESIZABLE)
        rl.init_window(title=f"{title} (raylib)")
        rl.init_audio_device()
    elif config.backend == 1:
        global pygame_screen
        pygame.init()
        pygame_screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption(f"{title} (Pygame)")
    elif config.backend == 2:
        global pyglet_window
        pyglet_window = pyglet.window.Window(800, 600, f"{title} (pyglet)", resizable=True)


def run(fps=60):
    if config.backend == 0: # raylib
        while not rl.window_should_close():
            upd_event()
            draw_event()
        rl.close_window()
        rl.close_audio_device()

    if config.backend == 1: # pygame
        pygame_should_close = False
        while not pygame_should_close:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame_should_close = True
            upd_event()
            draw_event()
        pygame.quit()

    if config.backend == 2: # pyglet
        pyglet_window.on_draw = draw_event
        pyglet.clock.schedule_interval(upd_event, 1/fps)
        pyglet.app.run()

def fill_bg_color(r: int, g: int, b: int, a: int = 255):
    if config.backend == 0: # raylib
        rl.clear_background(rl.make_color(r, g, b, a))
    if config.backend == 1: # pygame
        pygame_screen.fill((r, g, b, a))
    if config.backend == 2: # pyglet
        gl.glClearColor(r / 255, g / 255, b / 255, a / 255)
        pyglet_window.clear()

# draw shapes
def draw_rectangle(x: int, y: int, width: int, height: int, r: int, g: int, b: int, a: int = 255):
    if config.backend == 0: # raylib
        rl.draw_rectangle(x, y, width, height, rl.make_color(r, g, b, a))
    if config.backend == 1: # pygame
        e = pygame.Rect(x, y, width, height)
        pygame.draw.rect(pygame_screen, (r, g, b, a), e)
    if config.backend == 2: # pyglet
        o = pyglet.shapes.Rectangle(x, pyglet_window.height - y, width, -height, (r, g, b, a))
        o.draw()

def draw_circle(x: int, y: int, radius: int, r: int, g: int, b: int, a: int = 255):
    if config.backend == 0: # raylib
        rl.draw_circle(x, y, radius, rl.make_color(r, g, b, a))
    if config.backend == 1: # pygame
        pygame.draw.circle(pygame_screen, (r, g, b, a), (x, y), radius)
    if config.backend == 2: # pyglet
        pyglet.shapes.Circle(x, pyglet_window.height - y, radius, color=(r, g, b, a)).draw()

def draw_text(text: str, x: int, y: int, size: int, r: int, g: int, b: int, a: int = 255):
    if config.backend == 0: # raylib
        rl.draw_text(text, x, y, size, rl.make_color(r, g, b, a))
    if config.backend == 1: # pygame
        pyfnt = pygame.font.SysFont(None, size)
        surf = pyfnt.render(text, False, (r, g, b, a))
        pygame_screen.blit(surf, (x, y))
    if config.backend == 2: # pyglet
        pyglet.text.Label(
            text, x, pyglet_window.height - y, 
            font_name='Times New Roman',
            font_size=size,
            color=(r, g, b, a)
        ).draw()

# GUI

def gui_button(text: str, x: int, y: int, width: int, height: int, text_size = 20):
    if config.backend == 0:
        rl.gui_button(rl.make_rect(x, y, width, height), text)
    else:
        draw_rectangle(x, y, width, height, 245, 245, 245)
        draw_text(text, x, y, text_size, 255, 255, 255)


# drawing
def begin_drawing():
    if config.backend == 0: # raylib
        rl.begin_drawing()

def end_drawing():
    if config.backend == 0: # raylib
        rl.end_drawing()
    if config.backend == 1: # pygame
        pygame.display.flip()

def get_window_size():
    if config.backend == 0: # raylib
        return (rl.get_screen_width(), rl.get_screen_height())
    if config.backend == 1: # pygame
        return (pygame_screen.get_width(), pygame_screen.get_height())
    if config.backend == 2: # pyglet
        return (pyglet_window.width, pyglet_window.height)

# events
def _dummy(*args):
    pass

draw_event = _dummy
'What will i draw?'
upd_event = _dummy
"the function linked to this should have a 'dt' argument"