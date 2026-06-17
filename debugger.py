"NebAssembly Debugger"

import json

import kernel
import renderer
import ultimateraylib as rl
import style
import fileexplorer

x=0
y=0
w=500
h=300
isopen = False
currentprogram = None

filename = ""

isrunning = False
currentin = ["main", 0]

def draw():
    global w,h,isopen,x,y,currentprogram,currentin,isrunning

    if not isopen:
        return

    renderer.draw_rectangle(x,y,w- 50,50,*style.BRIGHT)
    renderer.draw_text("NSM DEBUG", x, y, 50, *style.DARKEST)
    
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
    
    if renderer.gui_button("Run", x, y + 50, 30, 20):
        currentin = ["main",0]
        isrunning = True

    if renderer.gui_button("Pause" if isrunning else "Resume", x + 30, y + 50, 50, 20):
        isrunning = not isrunning
    
    if renderer.gui_button("Select NSM File", x, y + 70, 100, 20):
        fileexplorer.isopen = True
    
    renderer.draw_text(f"Instruction {currentin[1]} in {currentin[0]}", x + 80, y+50, 20, *style.DARKEST)

    # Addresses GUI

    renderer.draw_rectangle(x + w, y + 50, 200, h, *style.BRIGHT)






    f=fileexplorer.draw()[1]
    if isinstance(f, kernel.File):
        er = json.loads(f.contents)
        currentprogram = kernel.Program(er)
        

def test_draw():
    renderer.begin_drawing()
    renderer.fill_bg_color(*style.BRIGHTEST)
    draw()
    renderer.end_drawing()

def test():
    global isopen
    isopen = True
    renderer.init("Debugger test")
    renderer.draw_event = test_draw
    renderer.run()

if __name__ == "__main__":
    test()
