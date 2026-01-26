import kernel
import ultimateraylib as rl
import time
import lang

menu_pos = rl.Vector2(0, 0)
is_dragging = False
drag_offset = rl.Vector2(0, 0)
draw_options = False

showdock = True

def draw_menu(r: int, g: int, b: int):
    global menu_pos, is_dragging, drag_offset, draw_options
    global showdock

    MENU_RADIUS = 50
    mouse_pos = rl.get_mouse_position()

    # Start dragging
    if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
        if rl.check_collision_point_circle(mouse_pos, menu_pos, MENU_RADIUS):
            is_dragging = True
            drag_offset = rl.vector2_subtract(mouse_pos, menu_pos)

    # Stop dragging
    if rl.is_mouse_button_released(rl.MOUSE_BUTTON_LEFT):
        is_dragging = False

    # Drag while held
    if is_dragging:
        menu_pos = rl.vector2_subtract(mouse_pos, drag_offset)

    # toggle options
    if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_RIGHT):
        if rl.check_collision_point_circle(mouse_pos, menu_pos, MENU_RADIUS):
            draw_options = not draw_options
            rl.play_sound(kernel.sounds['tap'])
    
    # drawing
    rl.draw_circle_v(menu_pos, MENU_RADIUS, rl.make_color(r, g, b))
    rl.draw_texture_ex(kernel.icons['logowhite'], rl.vector2_subtract(menu_pos, rl.Vector2(45,45)), 0, 0.39, rl.make_color(255 - r, 255 - g, 255 - b))

    # draw options
    if draw_options:

        # exit button draw
        rl.draw_circle_v(rl.vector2_add(menu_pos, rl.Vector2(MENU_RADIUS + ((MENU_RADIUS / 2) + 10), 0)), MENU_RADIUS / 2, rl.make_color(r, g, b))

        rl.draw_texture_ex(
            kernel.icons['power'], 
            rl.vector2_add(menu_pos, rl.Vector2(MENU_RADIUS + ((MENU_RADIUS / 2) + -5), -20)), 
            0, 0.4, rl.WHITE
        )

        # showhide dock button draw
        rl.draw_circle_v(rl.vector2_add(menu_pos, rl.Vector2(0, (MENU_RADIUS + ((MENU_RADIUS / 2))) * -1 - 10)), MENU_RADIUS / 2, rl.make_color(r, g, b))

        # clicky
        if rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):

            # exit button event
            if rl.check_collision_point_circle(mouse_pos, 
                                               rl.vector2_add(menu_pos, rl.Vector2(MENU_RADIUS + ((MENU_RADIUS / 2) + 10), 0)),
                                               MENU_RADIUS / 2):
                rl.draw_text(lang.langkey("exit"), 0, 0, 100, rl.make_color(r, g, b))
                rl.end_drawing()
                time.sleep(1)
                kernel.exit()
            
            # showhide dock button event
            if rl.check_collision_point_circle(mouse_pos, 
                                               rl.vector2_add(menu_pos, rl.Vector2(0, (MENU_RADIUS + ((MENU_RADIUS / 2))) * -1 - 10)),
                                               MENU_RADIUS / 2):
                showdock = not showdock
                
def test():
    rl.set_config_flags(rl.FLAG_WINDOW_RESIZABLE)
    rl.init_window(title="nbc")
    rl.init_audio_device()
    rl.set_target_fps(60)
    kernel.initicons()
    rl.hide_cursor()
    #print(kernel.icons)
    while not rl.window_should_close():
        rl.begin_drawing()
        rl.clear_background(rl.RAYWHITE)
        #rl.draw_rectangle(0,0,200,100, rl.RED)

        draw_menu(255, 0, 0)

        rl.draw_texture_ex(kernel.icons['cursor'], rl.get_mouse_position(), 0, 0.45 if rl.is_mouse_button_down(rl.MOUSE_BUTTON_LEFT) else 0.5, rl.WHITE)
        
        rl.end_drawing()
    rl.close_audio_device()
    rl.close_window()

if __name__ == "__main__":
    test()
