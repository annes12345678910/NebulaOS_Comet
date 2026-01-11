import ultimateraylib as rl
import kernel,style

def censor(string: str, char = '*'):
    "Censor an entire string, can be used to hide passwords"
    return char * len(string)

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



def test():
    print(censor("Meow"))

if __name__ == "__main__":
    test()
