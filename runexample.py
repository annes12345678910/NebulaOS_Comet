import nebdist.renderer as ren
import nebdist.kernel as kern
import sys
import json

def main():
    global e
    args = sys.argv
    print(args)

    try:
        with open(args[1]) as f:
            code = json.load(f)
    except IndexError:
        print("No program")
        sys.exit(1)
    
    ren.init("Run Example")

    e = kern.Program(code)
    e.run()
    print(e.output)
    
    ren.run()

def draw():
    global e
    ren.begin_drawing()
    e.buffer.draw(0,0)
    ren.end_drawing()

ren.draw_event = draw
if __name__ == "__main__":
    main()
