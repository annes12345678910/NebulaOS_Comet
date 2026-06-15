import kernel
import renderer
import ultimateraylib as rl
import style
import typeentries

x=0
y=0
w=500
h=300
isopen = False
currentfolder=kernel.root
scroll = 0

def draw():
    global w,h,isopen,x,y,currentfolder,scroll

    if not isopen:
        return None,None

    renderer.draw_rectangle(x,y,w- 50,50,*style.BRIGHT)
    # close
    if renderer.gui_button("x", x + w - 50, y, 50, 50):
        isopen = False

    renderer.draw_rectangle(x,y+50,w,h,*style.BRIGHTBRIGHT)

    # resizing
    #renderer.draw_circle(x + w, y + 50 + h, 20, 255,0,0)

    if rl.check_collision_point_circle(rl.get_mouse_position(), rl.Vector2(x + w, y + 50 + h), 20) and renderer.is_mouse_left_down():
        w += int(rl.get_mouse_delta().x)
        h += int(rl.get_mouse_delta().y)
    
    if renderer.Rect(x,y,w-50,50).collidepoint(renderer.get_mouse_point()) and renderer.is_mouse_left_down():
        x+=int(rl.get_mouse_delta().x)
        y+=int(rl.get_mouse_delta().y)

    # items
    scroll += renderer.get_mouse_scroll()
    ind = 0
    for i in currentfolder.glob():
        if renderer.gui_button("", x, y + 100 + (30 * ind) + int(scroll), w, 20):
            if type(i) is kernel.Folder:
                currentfolder = i
            if type(i) is kernel.File:
                return typeentries.entries[typeentries.getextgroup(i.ext)], i
            
        renderer.draw_text(i.name if type(i) is kernel.Folder else f"{i.name}.{i.ext}", x, y + 100 + (30 * ind) + int(scroll), 20, *style.DARKEST) # pyright: ignore[reportAttributeAccessIssue]
        ind += 1

    # extra widgets
    # up button
    if renderer.gui_button("^", x,y + 50,50,50):
        if currentfolder.parent:
            currentfolder = currentfolder.parent

    #current path
    renderer.draw_text(currentfolder.get_absolute(), x + 60, y + 60, 20, *style.DARKEST)
    return (None,None)

def test_draw():
    renderer.begin_drawing()
    renderer.fill_bg_color(*style.BRIGHTEST)
    draw()
    renderer.end_drawing()

def main():
    global isopen,currentfolder
    isopen = True
    pop = kernel.Folder(kernel.root, "test")
    kernel.folders.append(pop)
    kernel.writetofile("./file.txt", b"Hello!")
    currentfolder = kernel.root
    print(kernel.folders)
    print(kernel.root.glob())
    renderer.init("File Explorer Test")
    renderer.draw_event = test_draw
    renderer.run()

if __name__ == "__main__":
    main()
