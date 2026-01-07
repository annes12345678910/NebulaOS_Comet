import ultimateraylib as rl
from pathlib import Path

fold = Path(__file__).parent

def load_texture(file: str) -> rl.Texture2D:
    return rl.load_texture(str(fold / file))

def load_sound(file: str) -> rl.Sound:
    return rl.load_sound(str(fold / file))

def load_font(file: str) -> rl.Font:
    return rl.load_font(str(fold / file))

class DynamicFont:
    MODE_NORMAL = 'normal'
    MODE_ITALIC = 'italic'
    MODE_BOLD = 'bold'
    MODE_BOLD_ITALIC = 'bold-italic'
    def __init__(self, fontname="Arial", ext='ttf', mode='normal') -> None:
        self.mode = mode
        self.normal = load_font(f"assets/font/{fontname}.{ext}")
        self.bold = load_font(f"assets/font/{fontname}-bold.{ext}")
        self.italic = load_font(f"assets/font/{fontname}-italic.{ext}")
        self.bold_italic = load_font(f"assets/font/{fontname}-bold-italic.{ext}")

    def get_font(self):
        match self.mode:
            case self.MODE_NORMAL:
                return self.normal
            case self.MODE_BOLD:
                return self.bold
            case self.MODE_ITALIC:
                return self.italic
            case self.MODE_BOLD_ITALIC:
                return self.bold_italic
            case _:
                return self.normal

    def draw(self, text="Text", pos=rl.Vector2(0,0), font_size = 20, spacing = 1, color=rl.BLACK):
        rl.draw_text_ex(self.get_font(), text, pos, font_size, spacing, color)

default_font: rl.Font
def init():
    global default_font
    default_font = load_font("assets/font/nebulaos-default.otf")

def test():
    import random
    rl.init_window()
    rl.set_target_fps(60)
    font = DynamicFont()
    opo = [DynamicFont.MODE_BOLD, DynamicFont.MODE_ITALIC, DynamicFont.MODE_NORMAL]
    frame = 0
    poop = ''
    while not rl.window_should_close():
        frame += 1
        rl.begin_drawing()
        rl.clear_background(rl.BLACK)
        if (frame % 30) == 0:
            poop = str(random.randint(0, 10000))
            font.mode = random.choice(opo)
        font.draw(text=poop, color=rl.RED)
        
        rl.end_drawing()
    rl.close_window()
if __name__ == "__main__":
    test()
