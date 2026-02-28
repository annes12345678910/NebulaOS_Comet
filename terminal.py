text = ""
inpt = ""
width = 400
height = 300
opened = False

history = [""]
hisdex = 0

import kernel
import ultimateraylib as rl
import renderer
import style
from savesys import *
import filedialogs
import textwrap

x = 10
y = 70
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
    kernel.writetofile(f"./{args[0]}.{args[1]}", args[2].encode(), currentfolder)
    return f"Written to {args[0]}.{args[1]}"
    #r = kernel.getfilebyname(f"./{args[0]}.{args[1]}", currentfolder)
    #if r:
    #    r.contents = args[2].encode()
    #    return f"{r.name}.{r.ext} Written!"
    #else:
    #    e = kernel.File(currentfolder, args[0], args[1])
    #    e.contents = args[2].encode()
    #    files.append(
    #        e # this e is too lonely so im here
    #    )
    #    return f"{e.name}.{e.ext} Written!"

def ls(*args):
    print(folders, files)
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
    return ""

def importt(*args):
    fs = filedialogs.askfiles(title="Import to NebOS")
    if fs:
        for i in fs:
            with open(str(i), "rb") as f:
                kernel.writetofile(f"./{i.name}", f.read(), currentfolder)
                printtxt(f"Wrote {i.name}")
    return "Canceled."

def export(*args):
    f = filedialogs.asksave(title="Export File", initial_file=args[0].removeprefix('./'))
    e = kernel.getfilebyname(args[0], currentfolder)
    if f:
        with open(str(f), "wb") as s:
            if e:
                s.write(e.contents)
                s.close()
                return "File written"
            s.close()
            return f"Invalid File {args[0]}"
    return "Canceled"

def cd(*args):
    global currentfolder
    if len(args) < 1:
        return "Usage: cd <folderpath>"

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
    if len(args) < 1:
        return "Usage: cat <filepath>"
    
    e = kernel.getfilebyname(args[0], currentfolder)
    if e:
        try:
            return e.contents.decode()
        except UnicodeDecodeError:
            if '-force' in args:
                return textwrap.fill(str(e.contents), width)
            return "File not unicode. Use catraw or provide argument -force"
    return "Invalid File"

def clear(*args):
    global text,scrolly
    text = ""
    scrolly = 0
    return ""

def delete(*args): # del is reserved bruh
    if len(args) < 1:
        return "Usage: del <path>"
    
    e = kernel.getfilebyname(args[0], currentfolder)
    r = kernel.getfolderbyname(args[0], currentfolder)

    if e:
        files.remove(e)

    elif r:
        folders.remove(r)

    else:
        return "Invalid path"

    return "Path deleted"

def record(*args):
    if len(args) < 2:
        return "Usage: record (or rec) <filename> <extension>"
    kernel.writetofile(f"./{args[0]}.{args[1]}", text.encode(), currentfolder)

def help(*args):
    return """
System commands:

meow - MEOW MEOWW

ls (or dir) <optional folderpath> - list files and folders

import - import a file to here
export - export a file to the parent OS

write <filename> <extension> <contents> - write new file 
cd <folderpath> - change current folder
cat (or type) <filepath> - print out the contents of the filepath provided

clear (or cls) - clear all output

del (or rm) - delete a file or folder

record (or rec) <filename> <extension> - record your terminal history into a file

help - Display this message

pwd - Print current directory

version - Version and copyright stuff

-- If you want to report any bugs, visit https://forms.gle/1N9vyiRtAMXobLFA9 .
"""

def pwd(*args):
    return currentfolder.get_absolute()

def version(*args):
    return """
Copyright © Annes Widow and contributors
NebulaOS Comet (0.2.0)
"""

# follow list_of_cmd.txt and maybee more!
cmds = {
    "meow":meow,

    "ls":ls,
    "dir":ls,

    "import":importt,
    "export":export,

    "write":write,

    "cd":cd,

    "cat":cat,
    "type":cat,

    "clear":clear,
    "cls":clear,

    "del":delete,
    "rm":delete,

    "record":record,
    "rec":record,

    "help":help,

    "pwd":pwd,

    "version":version
}

def printtxt(*args, sep=" ", endl="\n"):
    global text
    string = sep.join(str(arg) for arg in args)
    text = text + string + endl

def computecmd(string: str):
    cmd = string.split(" ")
    eo = cmd[0]
    if cmd == []:
        return ""
    if cmds.get(eo):
        return cmds[eo](*cmd[1:])
    else:
        return f"Invalid command {eo}"

def get_collision():
    return renderer.Rect(x, y, int(width), int(height)).collidepoint(renderer.Point(*renderer.get_mouse_pos()))

def draw_terminal():
    global text, inpt, rtex, scrolly,width,height, opened, x , y, hisdex

    if rtex.texture.width != width or rtex.texture.height != height:
        rl.lib.UnloadRenderTexture(rtex)
        rtex = rl.load_render_texture(width, height)

    renderer.draw_rectangle(x, y, width, height, *style.BRIGHT)

    rl.draw_texture_rec(rtex.texture, rl.Rectangle(0, 0, width, -height), rl.Vector2(x,y), rl.WHITE)

    inpt = renderer.gui_textbox(inpt, 1024, x + 10, y + 10, width - 70, 50)
    prs = renderer.gui_button("Run", x + width - 55, y + 10, 50, 50)

    # resizer
    rec = renderer.Rect(x + width - 25, y + height - 25, 50, 50)
    #renderer.draw_rectangle(rec.x, rec.y, rec.width, rec.height, 255, 0, 0)
    if rec.collidepoint(renderer.Point(*renderer.get_mouse_pos())) and renderer.is_mouse_left_down():
        opo:rl.Vector2 = rl.get_mouse_delta()
        width += int(opo.x)
        height += int(opo.y)

    # top bar
    eop = renderer.Rect(x, y - 50, width, 50)
    renderer.draw_rectangle(eop.x, eop.y, eop.width, eop.height, *style.BRIGHTEST)
    if eop.collidepoint(renderer.Point(*renderer.get_mouse_pos())) and renderer.is_mouse_left_down():
        x = int(renderer.get_mouse_pos()[0] - (width // 2))
        y = int(renderer.get_mouse_pos()[1] + 25)

    renderer.gui_button("Command Line", x, y - 50, 100, 50)
    renderer.gui_button("Nebassembly", x + 110, y - 50, 100, 50)

    if renderer.gui_button("x", x + width - 50, y - 50, 50, 50):
        opened = False

    rl.begin_texture_mode(rtex)
    renderer.fill_bg_color(0, 0, 0, 0)
    renderer.draw_text(text, 10, int(scrolly), int(height / 20), *style.DARKEST)
    rl.end_texture_mode()

    if get_collision():
        scrolly -= renderer.get_mouse_scroll()

    # enter command
    if prs or get_collision() and rl.is_key_pressed(rl.KEY_ENTER):
        printtxt(f"{currentfolder.get_absolute()}> {inpt}")
        printtxt(computecmd(inpt))
        history.append(inpt)
        history[0] = ""
        inpt = ""
    
    # history
    if -1 - hisdex == -1:
        history[-1] = inpt
    
    if rl.is_key_pressed(rl.KEY_UP):
        hisdex += 1 if len(history) - 1 > hisdex else 0
        inpt = history[-1 - hisdex]
        print(hisdex)

    if rl.is_key_pressed(rl.KEY_DOWN):
        hisdex -= 1 if 0 < hisdex else 0
        inpt = history[-1 - hisdex]
        print(hisdex)

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
    x = 100
    y = 100
    while not rl.window_should_close():
        rl.begin_drawing()
        rl.clear_background(rl.BLUE)
        draw_terminal()
        rl.end_drawing()
    rl.close_audio_device()
    rl.close_window()

if __name__ == "__main__":
    test()
