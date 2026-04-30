import ultimateraylib as rl
try:
    import kernel,style
except:
    from . import kernel,style

def censor(string: str, char = '*'):
    "Censor an entire string, can be used to hide passwords"
    return char * len(string)

def icon_button(icon: str, pos_x: int, pos_y: int):
    e = kernel.icons[icon]
    #rl.draw_rectangle(pos_x, pos_y, e.width + 20, e.height + 20, style.BRIGHT)
    opo: rl.Rectangle = rl.make_rect(pos_x, pos_y, 40 + 20, 40 + 20)

    clr = style.BRIGHT
    if rl.check_collision_point_rec(rl.get_mouse_position(), opo):
        if rl.is_mouse_button_down(rl.MOUSE_BUTTON_LEFT):
            clr = style.BRIGHTEST
            rl.draw_rectangle_rounded(opo, 0.4, 2, rl.make_color(clr[0], clr[1], clr[2]))

            e.draw(pos_x + 10, pos_y + 10, 255,255,255,255)
            return True
        else:
            clr = style.BRIGHTBRIGHT
    
    rl.draw_rectangle_rounded(opo, 0.4, 2, rl.make_color(clr[0], clr[1], clr[2]))

    #rl.draw_texture(e, pos_x + 10, pos_y + 10, rl.WHITE)
    e.draw(pos_x + 10, pos_y + 10, 255,255,255,255)
    return False

def test():
    print(censor("Meow"))

if __name__ == "__main__":
    test()
