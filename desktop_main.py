import kernel
import renderer
import ultimateraylib as rl
import welcome

def draw():
    renderer.begin_drawing()
    renderer.fill_bg_color(100, 100, 100)

    renderer.draw_rectangle(10, 10, 200, 100, 100, 200, 200)

    renderer.end_drawing()

renderer.draw_event = draw

def main():
    renderer.init()
    renderer.run()

if __name__ == "__main__":
    main()
