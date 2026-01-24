
import kernel
#import ultimateraylib as rl
import style
import lang,util
import renderer

scene = 0
'''
0 = welcome!

1 = language

2 = theme

3 = root password

4 = user creation (user, icon, password)

5 = ready?
'''

opo = 0
def draw_welcome():
    global scene, opo
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
    
    elif scene == 2: # theme thingy
        renderer.draw_text(lang.langkey("start-choosetheme"), int(winw / skibidi + 10), int(winh / skibidi + 10), 30, *style.DARKEST)

        # light button
        if renderer.gui_button(lang.langkey("mode-light"), (winw // 2) - 140, winh // 2, 70, 40):
            style.changeblack(False)

        if renderer.gui_button(lang.langkey("mode-dark"), (winw // 2), winh // 2, 70, 40):
            style.changeblack(True)

    # previous and next
    if renderer.gui_button("Previous", skiend - 210, skihend - 60, 100, 50) and not scene <= 0:
        scene -= 1

    if renderer.gui_button("Next", skiend - 100, skihend - 60, 100, 50) and scene <= 3:
        scene += 1

def test_draw():
    renderer.begin_drawing()

    renderer.fill_bg_color(245, 245, 245)

    draw_welcome()
    renderer.end_drawing()

renderer.draw_event = test_draw

def test():
    renderer.init("Welcome")

    #rl.set_window_min_size(600, 400)
    
    style.changeblack(True)
    #kernel.initicons()
    #print(kernel.icons)
    
    renderer.run()

if __name__ == "__main__":
    test()
