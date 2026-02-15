import os
import random
import sys
import ultimateraylib as rl
import json
from colorama import Fore
import load
from savesys import *
import renderer

icons:dict[str, rl.Texture2D] = {}

def initicons():
    global icons, sounds
    icons = {}
    for i in os.listdir(str(load.fold / 'assets/img')):
        #print(str(load.fold / f'assets/img/{i}'))
        if os.path.isfile((load.fold / f'assets/img/{i}')):
            icons[(load.fold / f'assets/img/{i}').stem] = load.load_texture(f"assets/img/{i}")
    
    sounds = {}
    for i in os.listdir(str(load.fold / 'assets/sound')):
        if os.path.isfile((load.fold / f'assets/sound/{i}')):
            sounds[(load.fold / f'assets/sound/{i}').stem] = load.load_sound(f"assets/sound/{i}")

def error(string: str):
    print(f"{Fore.RED}[ERROR] {string}{Fore.RESET}")

os.makedirs("nbc_cache", exist_ok=True)

def exit():
    savesys()
    sys.exit(0)

class Folder:
    def __init__(self, parent, name:str):
        self.parent = parent
        self.name = name

        self.protected = False # enter the protector's password to modify
        self.protector = ""

    def getvisual(self, trace):
        # If this folder's parent *is* the trace folder
        if self.parent is trace:
            return f"./{self.name}"

        # If the parent is another Folder, recurse upward
        if isinstance(self.parent, Folder):
            return f"{self.parent.getvisual(trace)}/{self.name}"

        # If nothing else matches, fallback to root formatting
        return f"/{self.name}"
    
    def get_absolute(self):
        if isinstance(self.parent, Folder):
            return f"{self.parent.get_absolute()}/{self.name}"
        return f"/{self.name}"

    def tojson(self) -> dict:
        return {
            "parent": self.parent.name,
            "name": self.name,
            "protected": self.protected,
            "protector": self.protector
        }
    
    @staticmethod
    def fromjson(thejson: dict):
        #thejson.get("name", "None"),
        
        zeparent = None
        for i in folders:
            if i.name == thejson.get("parent", None):
                zeparent = i

        e = Folder(zeparent, thejson.get("name", "None"))

        e.protected = thejson.get("protected", False)
        e.protector = thejson.get("protector", "")
        return e
    
    def __repr__(self) -> str:
        return f"Folder( Address: {hex(id(self))} Path: {self.get_absolute()} )"
    
class File:
    def __init__(self, parent: Folder, name, ext):
        self.name = name
        self.ext = ext
        self.parent = parent
        self.contents = b""

        self.protected = False # enter the protector's password to modify
        self.protector = ""

        for i in files:
            if i.get_absolute() == self.get_absolute():
                del self

    def getvisual(self, trace):
        folder_visual = self.parent.getvisual(trace)

        if self.parent is trace:
            return f"./{self.name}.{self.ext}"
        return folder_visual + f"/{self.name}.{self.ext}"
    
    def get_absolute(self):
        if isinstance(self.parent, Folder):
            return f"{self.parent.get_absolute()}/{self.name}.{self.ext}"
        return f"/{self.name}"
    
    def getreadable(self):
        try:
            return self.contents.decode()
        except:
            return None

    def getname(self):
        return f"{self.name}.{self.ext}"

    def __repr__(self) -> str:
        return f"File( Address: {hex(id(self))} Path: {self.get_absolute()} )"


def getfilebyname(name, parent: Folder) -> File | None:
    for file in files:
        if file.getvisual(parent) == name:
            return file
    return None

def getfolderbyname(name, parent: Folder):
    for folder in folders:
        if folder.getvisual(parent) == name:
            return folder
    return None

# example program
"""
{
    "data": {
        "EXE_TYPE": "standalone"
    },

    "text": {
        "draw": [
            {"cal": ["_drawcircle", [0, 0], 100, [255, 0, 0, 255]]}
        ],
        "main": [
            {"mov": ["WIN_WIDTH", 800]},
            {"cal": ["_setupdrawbuffer", 800, 600]},
            {"cal": ["_setloop", "_DRAWLOOP", "draw"]}
        ]
    }
}
"""

root = Folder(None, "root")

class Program:
    def __init__(self, code:dict={}) -> None:
        self.code:dict = code
        self.exetype = self.code["data"]["EXE_TYPE"]
        self.text:dict = self.code["text"]
        self.buffer = rl.RenderTexture()
        self.currentfolder = root
        self.addresses = {
            "eax":0,
            "ebx":0,
            "ecx":0,
            "edx":0,
            "eex":0,
            "efx":0,

            "arg1":0,
            "arg2":0,
            "arg3":0,
            "arg4":0,
            "arg5":0,

            "_NEBVERSION": "0.1.0",
            "_NEBWIN": False,
            "_WINTITLE": "Program",
            "_WINX": 0,
            "_WINY": 0
        }
        self.consts: dict = {
            "_KEY_ONE": rl.KEY_ONE,
            "_KEY_TWO": rl.KEY_TWO,
        }
        self.output = ""
        self.loops = {
            "_DRAWLOOP": None,
        }
        self.errored = False
        self.funcs = []
        self.accesslevel = 0
        '''
        0 = basic level (no permission)
        1 = mild system level (Allow button - no admin) (Control other programs, control the mouse system-wide)
        2 = safe-breaking system level (Allows programs to breach privacy, record your computer and such) Requires the user's password to allow
        3 = full access (Can modify system files, unrestricted _py) - requires the root password to allow
        '''
    
    def _getvar(self, string):
        if self.addresses.__contains__(string):
            return self.addresses[string]
        if self.consts.__contains__(string):
            return self.consts[string]
        return string
    
    def call(self, func, args):
        if func == "_setupdrawbuffer":
            self.buffer = rl.load_render_texture(self._getvar(args[0]), self._getvar(args[1]))
            print(f"Init Buffer [{self._getvar(args[0])}, {self._getvar(args[1])}]")
        
        elif func == "_setloop":
            #_setloop [_DRAWLOOP, draw]
            self.loops[args[0]] = args[1]
        
        elif func == "_drawcircle":
            rl.begin_texture_mode(self.buffer)
            rl.draw_circle(self._getvar(args[0][0]), 
                           self._getvar(args[0][1]), 
                           self._getvar(args[1]), 
                           rl.make_color(
                               self._getvar(args[2][0]), 
                               self._getvar(args[2][1]), 
                               self._getvar(args[2][2]), 
                               self._getvar(args[2][3])
                            )
                        )
            rl.end_texture_mode()

        elif func == "_drawrect":
            rl.begin_texture_mode(self.buffer)
            rl.draw_rectangle(
                self._getvar(args[0][0]), 
                self._getvar(args[0][1]), 
                self._getvar(args[1][0]), 
                self._getvar(args[1][1]),
                rl.make_color(
                    self._getvar(args[2][0]), 
                    self._getvar(args[2][1]), 
                    self._getvar(args[2][2]), 
                    self._getvar(args[2][3])
                )
            )
            rl.end_texture_mode()

        elif func == "_clearbg":
            rl.begin_texture_mode(self.buffer)
            rl.clear_background(
                rl.make_color(
                    self._getvar(args[0]),
                    self._getvar(args[1]),
                    self._getvar(args[2]),
                    self._getvar(args[3])
                )
            )
            rl.end_texture_mode()
        
        elif func == "_startloop":
            if self.loops[args[0]]:
                opo = self.loops[args[0]]
                for line in self.text[opo]:
                    self.computeline(line)
        
        elif func == "_len":
            # _len [0, 0, 0]
            self.addresses["eax"] = len(self._getvar(args[0]))
        
        elif func == "_checkcollisionrecs":
            # _checkcollisionrecs, rec1: [[0, 0], [20, 20]] rec2: [[0,0], [30, 30]]
            self.addresses['eax'] = rl.check_collision_recs(
                rl.Rectangle(self._getvar(args[0][0][0]), self._getvar(args[0][0][1]), self._getvar(args[0][1][0]), self._getvar(args[0][1][1])), 
                rl.Rectangle(self._getvar(args[1][0][0]), self._getvar(args[1][0][1]), self._getvar(args[1][1][0]), self._getvar(args[1][1][1]))
            )
        
        elif func == "_rand":
            self.addresses['eax'] = random.randint(self._getvar(args[0]), self._getvar(args[1]))
        
        elif func == "_toint":
            self.addresses["eax"] = int(self._getvar(args[0]))
        
        elif func == "_tostr":
            self.addresses["eax"] = str(self._getvar(args[0]))
        
        elif func == "_getfilecontents":
            if len(args) < 1:
                print("Too few arguments for _getfilecontents, need 1 argument")
                return
            e = getfilebyname(self._getvar(args[0]), root)
            self.addresses['eax'] = e.contents if e else ""
        
        elif func == "_getfileext":
            if len(args) < 1:
                print("Too few arguments for _getfileext, need 1 argument")
                return
            e = getfilebyname(self._getvar(args[0]), root)
            self.addresses['eax'] = e.ext if e else ""

        elif func == "_getfilename":
            if len(args) < 1:
                print("Too few arguments for _getfilename, need 1 argument")
                return
            e = getfilebyname(self._getvar(args[0]), root)
            self.addresses['eax'] = e.name if e else ""

        elif func == "_createfile":
            if len(args) < 3:
                print("Too few arguments for _createfile, need 3 arguments")
                return
            
            if not type(self._getvar(args[2])) == str or type(self._getvar(args[2])) == bytes:
                return

            r = getfilebyname(f"./{self._getvar(args[0])}.{self._getvar(args[0])}", root)
            if r:
                r.contents = self._getvar(args[2]).decode()
                
            else:
                e = File(root, self._getvar(args[0]), self._getvar(args[1]))
                e.contents = self._getvar(args[2]).decode()
                files.append(e)

        elif func == "_loadtexture":
            # loadtexture 'dad.png'
            fad = getfilebyname(args[0], self.currentfolder)
            if isinstance(fad, File):
                print(f"loading {fad.getvisual(self.currentfolder)}")
                iop = fad.contents
                #print(iop)
                with open(f"nbc_cache/{args[0]}", 'wb') as f:
                    f.write(iop)
                self.addresses['eax'] = rl.load_texture(f"nbc_cache/{args[0]}")
                print(self.addresses['eax'])

        elif func == "_drawtexture":
            #drawtexture tex[Texture] x y tint[r g b]
            rl.begin_texture_mode(self.buffer)

            rl.draw_texture(self._getvar(args[0]), self._getvar(args[1]), self._getvar(args[2]), rl.make_color(
                self._getvar(args[3][0]),
                self._getvar(args[3][1]),
                self._getvar(args[3][2]),
                self._getvar(args[3][3])
            ))

            rl.end_texture_mode()
        
        elif func == "_guibutton":
            if len(args) < 5:
                print("Too few arguments for _guibutton, need 5 arguments")
                return
            rl.begin_texture_mode(self.buffer)
            self.addresses['eax'] = renderer.gui_button(self._getvar(args[0]), self._getvar(args[1]), self._getvar(args[2]), self._getvar(args[3]), self._getvar(args[4]))
            rl.end_texture_mode()
        
        elif func == "_drawtext":
            if len(args) < 8:
                print("Too few arguments for _drawtext, need 8 arguments")
                return
            rl.begin_texture_mode(self.buffer)
            renderer.draw_text(self._getvar(args[0]), self._getvar(args[1]), self._getvar(args[2]), self._getvar(args[3]), self._getvar(args[4]), self._getvar(args[5]), self._getvar(args[6]), self._getvar(args[7]))
            rl.end_texture_mode()

        elif func == "_guitextbox":
            if len(args) < 6:
                print("Too few arguments for _guitextbox, need 6 arguments")
                return
            rl.begin_texture_mode(self.buffer)
            self.addresses['eax'] = renderer.gui_textbox(self._getvar(args[0]), self._getvar(args[1]), self._getvar(args[2]), self._getvar(args[3]), self._getvar(args[4]), self._getvar(args[5]))
            rl.end_texture_mode()
        
        elif func == "_guimultitextbox":
            if len(args) < 6:
                print("Too few arguments for _guimultitextbox, need 8 arguments")
                return
            rl.begin_texture_mode(self.buffer)
            self.addresses['eax'] = renderer.gui_multitextbox(self._getvar(args[0]), self._getvar(args[1]), self._getvar(args[2]), self._getvar(args[3]), self._getvar(args[4]), self._getvar(args[5]), self._getvar(args[6]), self._getvar(args[7]))
            rl.end_texture_mode()

        elif func == "_getattr":
            self.addresses['eax'] = getattr(self._getvar(args[0]), self._getvar(args[1]))
        
        elif func == "_print":
            self.output += str(self._getvar(args[0]))

        elif func == "_println":
            self.output += str(self._getvar(args[0])) + "\n"
        
        elif func == "_iskeypressed":
            self.addresses['eax'] = rl.is_key_pressed(self._getvar(args[0]))
        
        elif func == "_geticon":
            self.addresses['eax'] = icons[args[0]] if icons.__contains__(args[0]) else icons['null']
        
        elif func == "_py":
            try:
                self.addresses['eax'] = eval(self._getvar(args[0]), self.addresses)
            except Exception as e:
                print(f"Python internally errored with {e} with the code {self._getvar(args[0])}")

        elif self.funcs.__contains__(func):
            for i in range(len(args)):
                print(f"Computing Arg {i} Into {args[i]}")
                self.addresses[f'arg{i}'] = args[i]

            for line in self.text[func]:
                self.computeline(line)
        else:
            error(f"Undefined Error: Invalid function {func}")
            self.errored = True
    
    def computeline(self, line: dict):
        for key in line.keys():
            #print(key)
            opo:list = line[key]

            if key == "mov":
                self.addresses[opo[0]] = self._getvar(opo[1])
                #print(self.addresses)

            elif key == "add":
                self.addresses[opo[0]] += self._getvar(opo[1])
                #print(self.addresses)

            elif key == "mns":
                self.addresses[opo[0]] -= self._getvar(opo[1])
                #print(self.addresses)

            elif key == "mlt":
                self.addresses[opo[0]] *= self._getvar(opo[1])
                #print(self.addresses)

            elif key == "div":
                try:
                    self.addresses[opo[0]] /= self._getvar(opo[1])
                except ZeroDivisionError as e:
                    print(f"Divided by 0! {line}: {e}")
                #print(self.addresses)

            elif key == "pow":
                self.addresses[opo[0]] **= self._getvar(opo[1])
                #print(self.addresses)

            elif key == "mod":
                self.addresses[opo[0]] %= self._getvar(opo[1])
                #print(self.addresses)

            elif key == "cal":
                #print(f"Calling {opo[0]}, with args {opo[1:]}")
                self.call(opo[0], opo[1:])
            
            elif key == "if":
                if self._getvar(opo[0]):
                    for line in opo[1]:
                        self.computeline(line)
            
            elif key == "whl":
                while self._getvar(opo[0]):
                    for line in opo[1]:
                        self.computeline(line)
            
            elif key == "for":
                for i in self._getvar(opo[0]):
                    self.addresses['eax'] = i
                    for line in opo[1]:
                        self.computeline(line)

            elif key == "rep":
                for i in range(self._getvar(opo[0])):
                    self.addresses['eax'] = i
                    for line in opo[1]:
                        self.computeline(line)
            
            elif key == "comment":
                pass

            else:
                error(f"Undefined Error: Invalid key {key}")
                self.errored = True
    
    def run(self):
        for i in self.text.keys():
            if i != "main":
                self.funcs.append(i)
        print(self.funcs)
        for line in self.text["main"]:
            self.computeline(line)
            if self.errored:
                break
        self.errored = False

class User:
    def __init__(self, icon, codename="username", name="Name", password='P4ssw0rd', pastebindevkey="mydevkey") -> None:
        self.icon = icon
        self.codename = codename
        self.name = name
        self.password = password
        self.devkey = pastebindevkey
    
    def tojson(self) -> dict:
        return {
            "codename": self.codename,
            "name": self.name,
            "password": self.password,
            "devkey": self.devkey
        }
    
    @staticmethod
    def fromjson(thejson: dict):
        return User(None, 
                        thejson.get("codename", "null"),
                        thejson.get("name", "None"),
                        thejson.get("password", "null"),
                        thejson.get("devkey", "null")
                    )
    
curpass = ''
def draw_usr_password_box(pos: tuple[int, int], user: User, r: int, g: int, b: int):
    global curpass
    curpass = renderer.gui_textbox(curpass, 64, int(pos[0]) - 100, int(pos[1]), 200, 60)
    renderer.draw_text(f"{user.name} ({user.codename})", int(pos[0]) - 100, int(pos[1]) - 40, 40, r, g, b, 255) 

def draw_window(prog: Program) -> bool:
    'Returns True when the window should be closed'
    pos = rl.Vector2(
        prog.addresses["_WINX"],
        prog.addresses["_WINY"]
    )
    toprect = rl.make_rect(
        pos.x - 10,
        pos.y - 60,
        prog.buffer.texture.width - 30,
        50
    )
    mousepos = rl.get_mouse_position()

    if prog.addresses['_NEBWIN'] and rl.is_render_texture_valid(prog.buffer):
        if rl.is_mouse_button_down(rl.MOUSE_BUTTON_LEFT):
            if rl.check_collision_point_rec(mousepos, toprect):
                prog.addresses['_WINX'] = (mousepos.x - (toprect.width /2))
                prog.addresses['_WINY'] = (mousepos.y + (toprect.height /2))

        rl.draw_rectangle_v(rl.vector2_subtract(pos, rl.Vector2(10, 10)), 
                         
                            rl.Vector2(prog.buffer.texture.width + 20, 
                                       prog.buffer.texture.height + 20
                                    ), 
        
                            rl.GRAY
                        )
        
        rl.draw_texture_rec(prog.buffer.texture, rl.make_rect(0,0,prog.buffer.texture.width, -prog.buffer.texture.height), pos, rl.WHITE)

        rl.draw_rectangle_rec(toprect, rl.DARKGRAY)

        rl.draw_text(
            str(prog.addresses['_WINTITLE']), 
            int(pos.x - 5),
            int(pos.y - 50),
            20, 
            rl.BLACK
        )

        if rl.gui_button(
            rl.make_rect(
                int(pos.x + (prog.buffer.texture.width - 40)),
                int(pos.y - 60),
                50,50
            ),
            "x"
        ):
            prog.addresses['_NEBWIN'] = False
            return True
    return False


def test():
    import menu
    #with open("assets/logomeow.png", 'rb') as f:
    #    data = f.read()
    #dfe = File(root, "dad", 'png')
    #dfe.contents = data

    rl.set_config_flags(rl.FLAG_WINDOW_RESIZABLE)
    rl.init_window()
    rl.init_audio_device()
    rl.set_target_fps(60)
    initicons()
    menu.kernel.initicons()
    with open("program.nsm") as f:
        code = json.load(f)
    
    programs:list[Program] = [Program(code), Program(code)]
    for i in programs:
        i.run()
    programs[0].addresses['_WINX'] = 400
    #opo = Program(code)
    #opo.run()

    while not rl.window_should_close():
        for opo in programs:
            if opo.loops["_DRAWLOOP"]:
               opo.call(opo.loops["_DRAWLOOP"], ["e"])
            
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)
        for opo in programs:
            draw_window(opo)
        menu.draw_menu(255, 0, 0)
        rl.end_drawing()
    rl.close_audio_device()
    rl.close_window()

if __name__ == "__main__":
    test()