import sys
import time
import config
import style
import copy

class Point:
    def __init__(self, x:int, y:int) -> None:
        self.x = x
        self.y = y

# collisions (because pyglet dont have collisions)
class Rect:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def collidepoint(self, point: Point):
        if (point.x >= self.x and
            point.x <= self.x + self.width and
            point.y >= self.y and
            point.y <= self.y + self.height):
            return True
        return False

if config.backend == 0:
    import ultimateraylib as rl
elif config.backend == 1:
    import pygame
    pygame_screen: pygame.Surface
    pygame_mouse_scroll = 0
elif config.backend == 2:
    import pyglet
    import pyglet.gl as gl
    from pyglet.window import mouse
    pyglet_window: pyglet.window.BaseWindow
    pyglet_mouse: mouse.MouseStateHandler
    pyglet_mouse_scroll = 0

else:
    print(f"Error: Invalid Backend {config.backend}")
    sys.exit(600)

left_pressed = False

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
        global pyglet_window, pyglet_mouse
        pyglet_window = pyglet.window.Window(800, 600, f"{title} (pyglet)", resizable=True)
        pyglet_mouse = mouse.MouseStateHandler()
        pyglet_window.push_handlers(pyglet_mouse)

# run a window loop
def run(fps=60):
    global pygame_mouse_scroll, left_pressed
    if config.backend == 0: # raylib
        rl.set_target_fps(fps)
        while not rl.window_should_close():
            upd_event()
            draw_event()
        rl.close_window()
        rl.close_audio_device()

    if config.backend == 1: # pygame
        pygame_should_close = False
        clock = pygame.time.Clock()
        while not pygame_should_close:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame_should_close = True
                if event.type == pygame.MOUSEWHEEL:
                    pygame_mouse_scroll = event.y
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        left_pressed = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        left_pressed = False
            upd_event()
            draw_event()
            clock.tick(fps)
        pygame.quit()

    if config.backend == 2: # pyglet
        def _scrolle(x, y, scroll_x, scroll_y):
            global pyglet_mouse_scroll
            pyglet_mouse_scroll = scroll_y
        
        def _mousedowne(x:int, y:int, button:int, modifiers:int):
            global left_pressed
            if button == mouse.LEFT:
                left_pressed = True

        def _mouseupe(x:int, y:int, button:int, modifiers:int):
            global left_pressed
            if button == mouse.LEFT:
                left_pressed = False

        pyglet_window.on_draw = draw_event
        pyglet_window.on_mouse_scroll = _scrolle
        pyglet_window.on_mouse_press = _mousedowne
        pyglet_window.on_mouse_release = _mouseupe

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
    splits = []
    offsety = 0
    if config.backend == 0: # raylib
        # raylib supports newline text
        rl.draw_text(text, x, y, size, rl.make_color(r, g, b, a))
    else:
        splits = text.split('\n')

    if config.backend == 1: # pygame
        pyrenders: list[pygame.Surface] = []

        pyfnt = pygame.font.SysFont(None, size)
        for i in splits:
            pyrenders.append(pyfnt.render(i, False, (r, g, b, a)))
        
        for i in pyrenders:
            offsety += size
            pygame_screen.blit(i, (x, y + offsety))

    if config.backend == 2: # pyglet
        for i in splits:
            offsety += size
            pyglet.text.Label(
                text, x, pyglet_window.height - (y + offsety), 
                font_name='Times New Roman',
                font_size=size,
                anchor_x="left",
                anchor_y="top",
                color=(r, g, b, a)
            ).draw()

def draw_line(x1: int, y1: int, x2: int, y2: int, thick: float, r: int, g: int, b: int, a: int = 255):
    if config.backend == 0: # raylib
        rl.draw_line_ex(rl.Vector2(x1, y1), rl.Vector2(x2, y2), thick, rl.make_color(r, g, b, a))

    if config.backend == 1: # pygame
        pygame.draw.line(pygame_screen, (r, g, b, a), (x1, y1), (x2, y2), int(thick))

    if config.backend == 2: # pyglet
        pyglet.shapes.Line(x1, pyglet_window.height - y1, x2, pyglet_window.height - y2, thick, (r, g, b, a)).draw()

# GUI

def gui_button(text: str, x: int, y: int, width: int, height: int, text_size = 20):
    if config.backend == 0:
        return rl.gui_button(rl.make_rect(x, y, width, height), text)
    else:
        draw_rectangle(x, y, width, height, *style.BRIGHT)
        draw_text(text, x, y, text_size, *style.DARK)
        return Rect(x, y, width, height).collidepoint(Point(*get_mouse_pos())) and is_mouse_left_pressed()

def gui_textbox(text: str, max_length: int, x: int, y: int, width: int, height: int) -> str:
    if config.backend == 0: # raylib
        e = rl.make_rect(x, y, width, height)
        return rl.gui_text_box(e, text, max_length, rl.check_collision_point_rec(rl.get_mouse_position(), e))[1]
    if config.backend == 1: # pygame
        pass
    if config.backend == 2: # pyglet
        pass
    
    return ""

shiftmap = {
    "1":"!",
    "2":"@",
    "3":"#",
    '4':'$',
    '5':'%',
    '6':'^',
    '7':'&',
    '8':'*',
    '9':'(',
    '0':')',

    '§':'±',
    '`':'~',
    '-':'_',
    '=':'+',

    '[':'{',
    ']':'}',
    
    ';':':',
    "'":'"',
    '\\':'|',
    ',':'<',
    '.':'>',
    '/':'?'
}

def gui_multitextbox(text: str, x:int, y:int, textsize: int, r:int, g:int, b:int, a:int = 255) -> str:
    opo = copy.deepcopy(text)
    draw_rectangle(x, y, rl.measure_text(text.split('\n')[0] if text.count('\n') > 0 else text, textsize) + 10, int(rl.measure_text_ex(rl.get_font_default(), text, textsize, 1).y), r, g, b, a)
    draw_text(text, x + 5, y, textsize, 255 - r, 255 - g, 255 - b, a)

    o = rl.get_key_pressed()
    e = rl.get_key_name(o) if o >= 32 else ""
    skib = ""
    if e:
        skib = e.decode()
    if rl.is_key_down(rl.KEY_LEFT_SHIFT) or rl.is_key_down(rl.KEY_RIGHT_SHIFT):
        if len(skib) > 0  and 'a' <= skib <= 'z':
            opo += chr(ord(skib) - 32)
            #print(chr(ord(skib) - 32))
        elif shiftmap.get(skib, None):
            opo += shiftmap[skib]
        else:
            opo += skib
    else:
        opo += skib
    
    if rl.is_key_pressed(rl.KEY_ENTER):
        opo += "\n"
    
    if rl.is_key_down(rl.KEY_BACKSPACE):
        time.sleep(0.1)
        opo = opo[:-1]
    
    if rl.is_key_pressed(rl.KEY_SPACE):
        opo += ' '

    return opo

# drawing
def begin_drawing():
    if config.backend == 0: # raylib
        rl.begin_drawing()

def end_drawing():
    if config.backend == 0: # raylib
        rl.end_drawing()
    if config.backend == 1: # pygame
        pygame.display.flip()

# util
def get_window_size() -> tuple[int, int]:
    if config.backend == 0: # raylib
        return rl.get_screen_width(), rl.get_screen_height()
    if config.backend == 1: # pygame
        return pygame_screen.get_width(), pygame_screen.get_height()
    if config.backend == 2: # pyglet
        return pyglet_window.width, pyglet_window.height
    return 0,0

# mouse
def get_mouse_pos() -> tuple[int, int]:
    if config.backend == 0: # raylib
        rey = rl.get_mouse_position()
        return rey.x, rey.y
    if config.backend == 1: # pygame
        return pygame.mouse.get_pos()
    if config.backend == 2: # pyglet
        return pyglet_mouse['x'], pyglet_window.height - pyglet_mouse['y']
    return 0, 0

def get_mouse_scroll(macscroll = False) -> float:
    if config.backend == 0: # raylib
        return -rl.get_mouse_wheel_move() if macscroll else rl.get_mouse_wheel_move()
    if config.backend == 1: # pygame
        return -pygame_mouse_scroll if macscroll else pygame_mouse_scroll
    if config.backend == 2: # pyglet
        return -pyglet_mouse_scroll if macscroll else pyglet_mouse_scroll
    return 0

def is_mouse_left_down():
    if config.backend == 0: # raylib
        return rl.is_mouse_button_down(rl.MOUSE_BUTTON_LEFT)
    if config.backend == 1: # pygame
        return pygame.mouse.get_pressed()[0]
    if config.backend == 2: # pyglet
        return pyglet_mouse[mouse.LEFT] # pyright: ignore[reportArgumentType] shut up pylance
    return False

def is_mouse_left_pressed():
    if config.backend == 0: # raylib
        return rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT)
    else:
        return left_pressed

# events
def _dummy(*args):
    pass

draw_event = _dummy
'What will i draw?'
upd_event = _dummy
"the function linked to this should have a 'dt' argument"

def test_draw():
    global woe
    begin_drawing()
    fill_bg_color(140, 0, 0)
    e = get_mouse_pos()
    draw_text(f"{e[0], e[1]}", int(e[0] + 100), int(e[1] + 100), 20, 255, 0, 0)

    woe = gui_multitextbox(woe, 10, 10, 20, 0, 255, 0, 255)
    end_drawing()

def test():
    global draw_event, woe
    woe = ""
    draw_event = test_draw
    init(title="Renderer Test")
    run()

if __name__ == "__main__":
    test()