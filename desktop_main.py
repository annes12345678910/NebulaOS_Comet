import kernel
import renderer
import ultimateraylib as rl
import welcome

scene = 0
'''
0 = Welcome
'''

def draw():
    renderer.begin_drawing()
    renderer.fill_bg_color(245, 245, 245)

    renderer.end_drawing()

renderer.draw_event = draw

def main():
    renderer.init()
    renderer.run()

if __name__ == "__main__":
    main()
