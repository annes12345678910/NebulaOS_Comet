import kernel
import renderer
import ultimateraylib as rl
import welcome
import savesys
import style

scene = 0
'''
0 = Welcome
'''

def draw():
    global scene
    renderer.begin_drawing()
    renderer.fill_bg_color(*style.BRIGHTEST)

    if scene == 0:
        welcome.draw_welcome()
        if welcome.is_done:
            scene = 1

    renderer.end_drawing()

renderer.draw_event = draw

def main():
    savesys.loadsys()

    renderer.init()
    renderer.run()

if __name__ == "__main__":
    main()
