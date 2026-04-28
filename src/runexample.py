import nebdist.renderer as ren
import nebdist.kernel as kern
import sys
import json

progs = [
    {
    "data": {
        "EXE_TYPE":"standalone"
    },
    "text": {
        "main": [
            {"mov": ["eax", 1]},
            {"cal": ["_print", "EAX value:"]},
            {"cal": ["_print", "eax"]}
        ]
    }
}

]

def main():
    global e
    args = sys.argv
    print(args)

    try:
        index = int(args[1])
        try:
            code = progs[index]
        except:
            print(f"No example with that number, latest example is example {len(progs)}")
            sys.exit(2)

    except:
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
