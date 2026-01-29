import kernel
import renderer
#import ultimateraylib as rl
import welcome
import savesys
import style
import menu

scene = 0
'''
0 = Welcome
1 = password 
2 = stufs
'''

# saved settings
dock_size = 70
programs: list[kernel.Program] = []

# unsaved stuff
show_sysdock = False
show_insdock = False

def draw():
    global scene
    renderer.begin_drawing()
    renderer.fill_bg_color(*style.BRIGHTEST)

    winw, winh = renderer.get_window_size()

    if scene == 0: # welcome
        welcome.draw_welcome()
        if welcome.is_done:
            scene = 1
            print(type(savesys.users))
            savesys.users.append(welcome.newuser)
            savesys.savesys()
    
    if scene == 1: # user box
        kernel.draw_usr_password_box((winw // 2, winh // 2), savesys.users[0], *style.DARKEST)

        if renderer.gui_button("->", winw - 110, 10, 100, 100):
            if kernel.curpass == savesys.users[0].password:
                scene = 2

    if scene == 2: # main
        if menu.showdock: # dock
            renderer.draw_rectangle(0, winh - dock_size, winw, dock_size, *style.DARK)

            renderer.gui_button("/\\", 10, winh + 10 - dock_size, dock_size - 20, dock_size - 20) # system apps button

            renderer.gui_button("/\\", winw // 2, winh + 10 - dock_size, dock_size - 20, dock_size - 20) # installed apps button

        menu.draw_menu(*style.DARKEST)

    renderer.end_drawing()

renderer.draw_event = draw

def main():
    global scene

    savesys.loadsys()
    if len(savesys.users) > 0:
        scene = 1

    renderer.init()
    kernel.initicons()
    renderer.run()

if __name__ == "__main__":
    main()
