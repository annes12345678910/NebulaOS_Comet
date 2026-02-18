
import kernel
#import ultimateraylib as rl
import style, savesys
import lang
import renderer

scene = 0
'''
0 = welcome!

1 = language

2 = timezone

3 = theme

4 = root password

5 = user creation (user, icon, password)

6 = optional and ready?
'''

opo = 0

current_text = ""
newuser = kernel.User(None)

is_done = False
timezone = "US/Central"

def draw_welcome():
    global scene, opo, is_done,timezone
    #icon_button('toby', 0, 0)
    winw, winh = renderer.get_window_size()

    skibidi = 10
    skimult = 8

    renderer.draw_rectangle(int(winw / skibidi), int(winh / skibidi), int(winw / skibidi) * skimult, int(winh / skibidi) * skimult, *style.BRIGHTBRIGHT)

    skiend = int(winw / skibidi) + int(winw / skibidi) * skimult
    skihend = int(winh / skibidi) + int(winh / skibidi) * skimult

    # welcome!
    if scene == 0:
        renderer.draw_text(lang.langkey("start-intro"), int(winw / skibidi) + 10, int(winh / skibidi) + 10, int(winw / skibidi / 3), *style.DARKEST)

        renderer.draw_text(lang.langkey("start-desc"), int(winw / skibidi) + 10, int(winh / skibidi) + 80, int(winw / skibidi / 8), *style.DARKEST)

    # languages
    elif scene == 1:
        renderer.draw_rectangle(int(winw / 3 - 10), 0, int(winw / 3 + 20), winh, *style.BRIGHTEST) # that strip you see on meat packages

        opo += renderer.get_mouse_scroll()

        ere = opo

        for i in lang.langs.keys():
            ere += 60

            if renderer.gui_button(f"{lang.langs[i]['lang-desc']} ({i})", int(winw / 3), int(ere), int(winw / 3), 50):
                lang.lang = i
        
        renderer.draw_text(lang.langkey("start-langchoice"), int(winw / skibidi + 10), int(winh / skibidi + 10), 30, *style.DARKEST)

        renderer.draw_text(lang.langkey("lang-desc"), int(winw / skibidi + 10), int(winh / skibidi + 50), 20, *style.DARKEST)
    
    elif scene == 2: # timezone
        renderer.draw_rectangle(int(winw / 3 - 10), 0, int(winw / 3 + 20), winh, *style.BRIGHTEST) # that strip you see on meat packages

        opo += renderer.get_mouse_scroll()

        ere = opo

        for i in kernel.pytz.all_timezones:
            ere += 60

            if renderer.gui_button(f"{i}", int(winw / 3), int(ere), int(winw / 3), 50):
                timezone = i
                kernel.pytz.timezone(i)

        renderer.draw_text(lang.langkey("start-timezone"), int(winw / skibidi + 10), int(winh / skibidi + 10), 30, *style.DARKEST)

        renderer.draw_text(timezone, int(winw / skibidi + 10), int(winh / skibidi + 50), 20, *style.DARKEST)

    elif scene == 3: # theme thingy
        renderer.draw_text(lang.langkey("start-choosetheme"), int(winw / skibidi + 10), int(winh / skibidi + 10), 30, *style.DARKEST)

        # light button
        if renderer.gui_button(lang.langkey("mode-light"), (winw // 2) - 140, winh // 2, 70, 40):
            style.changeblack(False)

        if renderer.gui_button(lang.langkey("mode-dark"), (winw // 2), winh // 2, 70, 40):
            style.changeblack(True)
    
    elif scene == 4: # rootpass
        renderer.draw_text(lang.langkey("enter-rpass"), int(winw / skibidi + 10), int(winh / skibidi + 10), 30, *style.DARKEST)
        
        savesys.rootpass = renderer.gui_textbox(savesys.rootpass, 255, winw // 2, winh // 2, 200, 50)
    
    elif scene == 5:
        renderer.draw_text(lang.langkey("enter-userinfo"), int(winw / skibidi + 10), int(winh / skibidi + 10), 30, *style.DARKEST)

        newuser.name = renderer.gui_textbox(newuser.name, 255, int(winw / skibidi + 10), int(winh / skibidi + 40), 300, 50)
        newuser.codename = renderer.gui_textbox(newuser.codename, 255, int(winw / skibidi + 10), int(winh / skibidi + 100), 300, 50)
        newuser.password = renderer.gui_textbox(newuser.password, 255, int(winw / skibidi + 10), int(winh / skibidi + 160), 300, 50)

    elif scene == 6:
        renderer.draw_text("Optional", int(winw / skibidi + 10), int(winh / skibidi + 10), 30, *style.DARKEST)

        newuser.devkey = renderer.gui_textbox(newuser.devkey, 64, int(winw / skibidi + 10), int(winh / skibidi + 50), 300, 50)

        if renderer.gui_button("Finish", int(winw / skibidi + 10), (winh // 2) + 50, 100, 50):
            is_done = True

    # previous and next
    if renderer.gui_button("Previous", skiend - 210, skihend - 60, 100, 50) and not scene <= 0:
        scene -= 1

    if renderer.gui_button("Next", skiend - 100, skihend - 60, 100, 50) and scene <= 5:
        scene += 1

def test_draw():
    renderer.begin_drawing()

    renderer.fill_bg_color(245, 245, 245)

    draw_welcome()
    renderer.end_drawing()

    if is_done:
        sys.exit(0)

renderer.draw_event = test_draw

def test():
    renderer.init("Welcome")

    #rl.set_window_min_size(600, 400)
    
    style.changeblack(True)
    #kernel.initicons()
    #print(kernel.icons)
    
    renderer.run()

if __name__ == "__main__":
    import sys
    test()
