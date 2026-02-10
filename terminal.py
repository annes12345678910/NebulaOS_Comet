text = ""
inpt = ""
width = 400
height = 300
opened = False
import kernel
import ultimateraylib as rl
import renderer
import style

x = 0
y = 0
rtex = rl.RenderTexture()
scrolly = 0

# command functions

def meow(*args):
    rl.play_sound(kernel.sounds['meow'])
    return "Meow!"

# follow list_of_cmd.txt and maybee more!
cmds = {
    "meow":meow,

}

def printtxt(*args, sep=" ", endl="\n"):
    global text
    string = sep.join(str(arg) for arg in args)
    text = text + string + endl

def computecmd(string: str):
    cmd = string.split(" ")
    eo = cmd[0]

    if cmds.get(eo):
        return cmds[eo](*cmd[1:])
    elif cmd == "":
        return ""
    else:
        return f"Invalid command {eo}"

def get_collision():
    return renderer.Rect(x, y, width, height).collidepoint(renderer.Point(*renderer.get_mouse_pos()))

def draw_terminal():
    global text, inpt, rtex, scrolly

    if rtex.texture.width != width or rtex.texture.height != height:
        rtex = rl.load_render_texture(width, height)

    renderer.draw_rectangle(x, y, width, height, *style.BRIGHT)

    rl.draw_texture_rec(rtex.texture, rl.Rectangle(0, 0, width, -height), rl.Vector2(x,y), rl.WHITE)

    inpt = renderer.gui_textbox(inpt, 1024, x + 10, y + 10, width - 70, 50)
    prs = renderer.gui_button("Run", x + width - 55, y + 10, 50, 50)

    rl.begin_texture_mode(rtex)
    renderer.fill_bg_color(0, 0, 0, 0)
    renderer.draw_text(text, 10, int(scrolly), int(width / 20), *style.DARKEST)
    rl.end_texture_mode()

    if get_collision():
        scrolly -= renderer.get_mouse_scroll()

    if prs or get_collision() and rl.is_key_pressed(rl.KEY_ENTER):
        printtxt(f"> {inpt}")
        printtxt(computecmd(inpt))
        inpt = ""

def test():
    global x, y, rtex
    import ultimateraylib as rl
    rl.set_config_flags(rl.FLAG_WINDOW_RESIZABLE)
    rl.init_audio_device()
    rl.init_window(title="Skibidi")
    rl.set_target_fps(60)
    kernel.initicons()
    rtex = rl.load_render_texture(width, height)
    #printtxt("plp", 21)
    x = 10
    y = 10
    while not rl.window_should_close():
        rl.begin_drawing()
        rl.clear_background(rl.BLUE)
        draw_terminal()
        rl.end_drawing()
    rl.close_audio_device()
    rl.close_window()

if __name__ == "__main__":
    test()
