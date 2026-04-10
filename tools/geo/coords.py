import time
import pyperclip
def join(inp:list)->float:
    end = ""
    for n in inp:
        end+=n

    end = end.replace(".","")
    end = "0."+end
    return round(float(end), ndigits=5)

def handle_copy(text:str)->None:
    #tst = 2'607'311.74, 1'126'776.02
    try:
        xy = [float(n) for n in text.replace("'","").split(", ")]
        xy = (xy[0] - 2000000, xy[1]-1000000)
        string_x = list(str(xy[0]))
        string_y = list(str(xy[1]))
        start_x = string_x[0]
        start_y = string_y[0]
        end_x = join(string_x[1:-1])
        end_y = join(string_y[1:-1])

        end_x = round(end_x*13,ndigits=1)
        end_y = round(end_y*13,ndigits=1)

        print(f"x: {start_x}00 km : {end_x}   :   {13-end_x}")
        print(f"y: {start_y}00 km : {end_y}   :   {13-end_y}")
    except ValueError:
        print(text)
    print("-"*40)

def monitor_clipboard(interval=.5):
    last_text = pyperclip.paste()

    while True:
        time.sleep(interval)
        current_text = pyperclip.paste()

        if current_text != last_text:
            handle_copy(current_text)
            last_text = current_text


if __name__ == "__main__":
    monitor_clipboard()