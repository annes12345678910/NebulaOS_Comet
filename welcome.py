
import kernel
import ultimateraylib as rl
import style
import lang

scene = 0
'''
0 = welcome!
1 = language
2 = theme
3 = ready?
'''

def icon_button(icon: str, pos_x: int, pos_y: int):
    e = kernel.icons[icon]
    #rl.draw_rectangle(pos_x, pos_y, e.width + 20, e.height + 20, style.BRIGHT)
    opo: rl.Rectangle = rl.make_rect(pos_x, pos_y, e.width + 20, e.height + 20)

    clr = style.BRIGHT
    if rl.check_collision_point_rec(rl.get_mouse_position(), opo):
        if rl.is_mouse_button_down(rl.MOUSE_BUTTON_LEFT):
            clr = style.BRIGHTEST
            rl.draw_rectangle_rounded(opo, 0.4, 2, clr)

            rl.draw_texture(e, pos_x + 10, pos_y + 10, rl.WHITE)
            return True
        else:
            clr = style.BRIGHTBRIGHT
    
    rl.draw_rectangle_rounded(opo, 0.4, 2, clr)

    rl.draw_texture(e, pos_x + 10, pos_y + 10, rl.WHITE)
    return False

opo = 0
def draw_welcome():
    global scene, opo
    #icon_button('toby', 0, 0)
    winw = rl.get_screen_width()
    winh = rl.get_screen_height()

    skibidi = 10
    skimult = 8

    rl.draw_rectangle(int(winw / skibidi), int(winh / skibidi), int(winw / skibidi) * skimult, int(winh / skibidi) * skimult, style.BRIGHT)

    skiend = int(winw / skibidi) + int(winw / skibidi) * skimult
    skihend = int(winh / skibidi) + int(winh / skibidi) * skimult

    # welcome!
    if scene == 0:
        rl.draw_text(lang.langkey("start-intro"), int(winw / skibidi) + 10, int(winh / skibidi) + 10, int(winw / skibidi / 3), style.BRIGHTEST)

        rl.draw_text(lang.langkey("start-desc"), int(winw / skibidi) + 10, int(winh / skibidi) + 80, int(winw / skibidi / 8), style.BRIGHTEST)

    # languages
    elif scene == 1:
        rl.draw_rectangle(int(winw / 3 - 10), 0, int(winw / 3 + 20), winh, style.BRIGHTBRIGHT)

        opo += rl.get_mouse_wheel_move()

        ere = opo

        for i in lang.langs.keys():
            ere += 60

            if rl.gui_button(rl.make_rect(winw / 3, ere, winw / 3, 50), f"{lang.langs[i]['lang-desc']} ({i})"):
                lang.lang = i
        
        rl.draw_text(lang.langkey("start-langchoice"), int(winw / skibidi + 10), int(winh / skibidi + 10), 30, style.BRIGHTEST)

        rl.draw_text(lang.langkey("lang-desc"), int(winw / skibidi + 10), int(winh / skibidi + 50), 20, style.BRIGHTEST)
        

    # previous and next
    if rl.gui_button(rl.make_rect(skiend - 210, skihend - 60, 100, 50), "Previous") and not scene <= 0:
        scene -= 1

    if rl.gui_button(rl.make_rect(skiend - 100, skihend - 60, 100, 50), "Next") and scene <= 3:
        scene += 1

def test():
    rl.set_config_flags(rl.FLAG_WINDOW_RESIZABLE)
    rl.init_window(title="Welcome")
    rl.init_audio_device()

    rl.set_window_min_size(600, 400)
    
    style.changeblack(True)
    kernel.initicons()
    print(kernel.icons)
    rl.set_target_fps(60)
    while not rl.window_should_close():
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)
        draw_welcome()
        rl.end_drawing()
    
    rl.close_audio_device()
    rl.close_window()

if __name__ == "__main__":
    test()
