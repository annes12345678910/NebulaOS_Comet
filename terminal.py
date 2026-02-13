text = ""
inpt = ""
width = 400
height = 300
opened = False
import kernel
import ultimateraylib as rl
import renderer
import style
from savesys import *

x = 0
y = 0
rtex = rl.RenderTexture()
scrolly = 0

currentfolder = kernel.root

# command functions

def meow(*args):
    rl.play_sound(kernel.sounds['meow'])
    return "Meow!"

def write(*args):
    if len(args) < 3:
        return "Usage: write <file name> <file extension> <file content>"

    r = kernel.getfilebyname(f"./{args[0]}.{args[1]}", currentfolder)
    if r:
        r.contents = args[2]
    else:
        e = kernel.File(currentfolder, args[0], args[1])
        e.contents = args[2]
        files.append(
            e # this e is too lonely so im here
        )
    return f"{e.name}.{e.ext} Written!"

def ls(*args):
    try:
        e = kernel.getfolderbyname(args[0], currentfolder)
    except IndexError:
        e = currentfolder
        
    for i in files:
        if i.parent == e:
            printtxt(f"{i.name}.{i.ext}")

    for i in folders:
        if i.parent == e:
            printtxt(f"{i.name}")

def cd(*args):
    global currentfolder
    if args[0] == "..":
        currentfolder = currentfolder.parent if currentfolder.parent else currentfolder
        return ""
    else:
        e = kernel.getfolderbyname(args[0], currentfolder)
        if e:
            currentfolder = e
            return ""
    return "Invalid Folder"

def cat(*args):
    e = kernel.getfilebyname(args[0], currentfolder)
    if e:
        return e.contents.decode()
    return "Invalid File"

def clear(*args):
    global text
    text = ""
    return ""

def record(*args):
    r = kernel.getfilebyname(f"./{args[0]}.{args[1]}", currentfolder)
    if r:
        r.contents = text.encode()
    else:
        e = kernel.File(currentfolder, args[0], args[1])
        e.contents = text.encode()
        files.append(e)
    return ""

def help(*args):
    return """
System commands:

meow - MEOW MEOWW
ls (or dir) <optional folderpath> - list files and folders
write <filename> <extension> <contents> - write new file 
cd <folderpath> - change current folder
cat (or type) <filepath> - print out the contents of the filepath provided
clear (or cls) - clear all output
record (or rec) <filename> <extension> - record your terminal history into a file

help - Display this message

-- If you want to report any bugs, visit https://forms.gle/1N9vyiRtAMXobLFA9 .
"""

# follow list_of_cmd.txt and maybee more!
cmds = {
    "meow":meow,

    "ls":ls,
    "dir":ls,

    "write":write,

    "cd":cd,

    "cat":cat,
    "type":cat,

    "clear":clear,
    "cls":clear,

    "record":record,
    "rec":record,

    "help":help
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
    return renderer.Rect(x, y, int(width), int(height)).collidepoint(renderer.Point(*renderer.get_mouse_pos()))

def draw_terminal():
    global text, inpt, rtex, scrolly,width,height

    if rtex.texture.width != width or rtex.texture.height != height:
        rl.lib.UnloadRenderTexture(rtex)
        rtex = rl.load_render_texture(width, height)

    renderer.draw_rectangle(x, y, width, height, *style.BRIGHT)

    rl.draw_texture_rec(rtex.texture, rl.Rectangle(0, 0, width, -height), rl.Vector2(x,y), rl.WHITE)

    inpt = renderer.gui_textbox(inpt, 1024, x + 10, y + 10, width - 70, 50)
    prs = renderer.gui_button("Run", x + width - 55, y + 10, 50, 50)

    rec = renderer.Rect(x + width - 25, y + height - 25, 50, 50)
    #renderer.draw_rectangle(rec.x, rec.y, rec.width, rec.height, 255, 0, 0)
    if rec.collidepoint(renderer.Point(*renderer.get_mouse_pos())) and renderer.is_mouse_left_down():
        opo:rl.Vector2 = rl.get_mouse_delta()
        width += int(opo.x)
        height += int(opo.y)

    rl.begin_texture_mode(rtex)
    renderer.fill_bg_color(0, 0, 0, 0)
    renderer.draw_text(text, 10, int(scrolly), int(height / 20), *style.DARKEST)
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

    eop = kernel.File(currentfolder, "opo", "txt")
    eop.contents = b"Hi \x70\x64"
    files.append(eop)
    folders.append(kernel.Folder(currentfolder, "p"))

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
