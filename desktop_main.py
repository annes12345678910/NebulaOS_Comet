import sys
import kernel
import renderer
import ultimateraylib as rl
import welcome
import savesys
import style
import menu
import cbinds
import pathlib
import json

import nbgf

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

nebfiles = cbinds.library_path.parent / "nebfiles"

kernel.files = savesys.files
kernel.folders = savesys.folders

def draw():
    global scene, show_sysdock, show_insdock
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

            if renderer.gui_button("\\/" if show_sysdock else "/\\", 10, winh + 10 - dock_size, dock_size - 20, dock_size - 20): # system apps button
                show_sysdock = not show_sysdock
                rl.play_sound(kernel.sounds['open'])
                if show_sysdock: # subdock sys
                    show_insdock = not show_sysdock

            if renderer.gui_button("\\/" if show_insdock else "/\\", winw // 2, winh + 10 - dock_size, dock_size - 20, dock_size - 20): # installed apps button
                show_insdock = not show_insdock
                rl.play_sound(kernel.sounds['open'])
                if show_insdock: # subdock ins
                    show_sysdock = not show_insdock
            
            if show_insdock or show_sysdock: # second dock
                renderer.draw_rectangle(0, winh - (dock_size * 2 + 10), winw, dock_size, *style.DARK)
                if show_sysdock: # sysapps
                    apin = 10
                    for fl in savesys.files:
                        if fl.parent == sysprogs:
                            if renderer.gui_button(fl.name, apin, winh - (dock_size * 2), dock_size - 20, dock_size - 20):
                                try:
                                    prodat = json.loads(fl.contents)
                                except json.JSONDecodeError as e:
                                    print(f"Error jsoning the {fl.name} system app's code, please reinstall NebulaOS: {e}")
                                    sys.exit(40)

                                launched = kernel.Program(prodat)

                                launched.addresses['_WINX'] = winw // 2
                                launched.addresses['_WINY'] = winh // 2

                                launched.run()
                                programs.append(launched)
                                
                            apin += dock_size - 10
        for prog in programs:
            if kernel.draw_window(prog):
                programs.remove(prog)

        menu.draw_menu(*style.DARKEST)

    renderer.end_drawing()

    for prog in programs: #update programs
        if prog.loops["_DRAWLOOP"]:
            prog.call(prog.loops["_DRAWLOOP"], [])

renderer.draw_event = draw

currentfolder = nebfiles
def import_path(path: pathlib.Path):
    if path.is_dir():
        if path.parent.name == 'nebfiles':
            print(f"Added dir {path}")
            savesys.folders.append(kernel.Folder(kernel.root, path.name))

def loadnebfiles(folder: pathlib.Path):
    dosyalar = list(folder.glob("*")) # why did i write the turkish for 'files'
    print(f"files loading: {dosyalar}")
    for i in dosyalar:
        import_path(i)

        if i.is_dir():
            currentfolder = i
            loadnebfiles(i)
            
systemf = kernel.Folder(kernel.root, "system")
sysprogs = kernel.Folder(systemf, "programs")

def main():
    global scene

    savesys.loadsys()
    if len(savesys.users) > 0:
        scene = 1
    
    savesys.folders.append(systemf)
    savesys.folders.append(sysprogs)
    
    for i in list((nebfiles / "system/programs").glob("*")):
        if i.is_file():
            with open(str(i), "rb") as f:
                e = kernel.File(sysprogs, i.name.split('.')[0], "nsm")
                e.contents = f.read()
                savesys.files.append(e)

    print("folders")
    print(savesys.folders)
    print("files")
    print(savesys.files)
    
    renderer.init()
    kernel.initicons()
    renderer.run()

if __name__ == "__main__":
    main()
