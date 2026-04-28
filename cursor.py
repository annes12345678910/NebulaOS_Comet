import os
try:
    import load,logger
    import renderer
except:
    from . import load,logger,renderer
    
import ultimateraylib as rl

cursors:list[renderer.Image] = []
current = 0
'''
0 = arrow
1 = pointing
2 = resize horizantal
'''

def draw():
    #rl.draw_texture_ex(cursors[current], rl.Vector2(*renderer.get_mouse_pos()), 0, 0.45 if renderer.is_mouse_left_down() else 0.5, rl.WHITE)
    e = renderer.get_mouse_pos()
    cursors[current].draw(e[0],e[1], 255,255,255,255, 0.45 if renderer.is_mouse_left_down() else 0.5)

def init():
    global cursors
    cursors = []
    
    for i in os.listdir(str(load.fold / 'assets/cursor')):
        if os.path.isfile((load.fold / f'assets/cursor/{i}')):
            cursors.append(renderer.Image(f"assets/cursor/{i}"))
            
    logger.info(cursors)
