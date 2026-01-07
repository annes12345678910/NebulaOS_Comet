text = ""
inpt = ""
width = 400
height = 300
opened = False
import kernel
import ultimateraylib as rl

x = 0
y = 0

def printtxt(*args, sep=" ", endl="\n"):
    global text
    string = sep.join(str(arg) for arg in args)
    text = text + string + endl

def computecmd(string: str):
    cmd = string.split(" ")

def draw_terminal():
    global text, inpt
    rl.draw_rectangle(x, y, width, height, rl.GRAY)
    pass

def test():
    global inpt
    import ultimateraylib as rl
    import load
    rl.set_config_flags(rl.FLAG_WINDOW_RESIZABLE)
    rl.init_window(title="Skibidi")
    rl.set_target_fps(60)
    printtxt("plp", 21)
    font = load.load_font("assets/img/nebulaos-default.otf")
    while not rl.window_should_close():
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)
        draw_terminal()
        rl.end_drawing()
    rl.close_window()
    pass

if __name__ == "__main__":
    test()
