import os
import load,logger
import renderer,ultimateraylib as rl

cursors = []
current = 0
'''
0 = arrow
1 = pointing
2 = resize
'''

def draw():
    rl.draw_texture_ex(cursors[current], rl.Vector2(*renderer.get_mouse_pos()), 0, 0.45 if renderer.is_mouse_left_down() else 0.5, rl.WHITE)

def init():
    global cursors
    cursors = []
    
    for i in os.listdir(str(load.fold / 'assets/cursor')):
        if os.path.isfile((load.fold / f'assets/cursor/{i}')):
            cursors.append(load.load_texture(f"assets/cursor/{i}"))
            
    logger.info(cursors)
    
