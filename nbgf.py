import renderer

def draw_nbgf(data: list, x: int, y: int):
    ln = 1
    for line in data:
        ln += 1
        if isinstance(line, dict):
            for key in line.keys():
                args = line[key]

                if key == "line":
                    if len(args) < 9:
                        print(f"Function draw_line does not have enough arguments at line {ln} ({line})")
                        return
                    renderer.draw_line(x + args[0], y + args[1], x + args[2], y + args[3], args[4], args[5], args[6], args[7], args[8])
                else:
                    print(f"Invalid Drawable {key} at line {ln}")
        else:
            print(f"Can't display NBGF properly, the line {line} is not of dict value at line {ln}")

def test_draw():
    global dat
    renderer.begin_drawing()
    renderer.fill_bg_color(0, 0, 0)
    draw_nbgf(dat, 100, 100)
    renderer.end_drawing()

def test():
    global dat
    import json

    with open("example.nbgf", "r") as f:
        dat = json.load(f)
    
    renderer.draw_event = test_draw
    renderer.init(title="NBGF Test")
    renderer.run()


if __name__ == "__main__":
    test()