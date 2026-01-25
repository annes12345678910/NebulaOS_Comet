import kernel
import renderer
import ultimateraylib as rl
import welcome
import savesys
import style
import menu

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
            print(type(savesys.users))
            savesys.users.append(welcome.newuser)
            savesys.savesys()
    
    if scene == 1:
        menu.draw_menu()

    renderer.end_drawing()

renderer.draw_event = draw

def main():
    savesys.loadsys()

    renderer.init()
    kernel.initicons()
    renderer.run()

if __name__ == "__main__":
    main()
