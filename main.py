import time
import pyniryo as bot
import inputs as control

Quit = False

for device in control.devices.gamepads:
    print(device)

if not control.devices.gamepads:
    print("No gamepad devices found")

while control.devices.gamepads:
    events = control.get_gamepad()
    for event in events:
        if Quit:
            break
        if "ABS_" in event.code:
            if "RX" in event.code:
                print("Right Stick L/R")
            elif "RY" in event.code:
                print("Right Stick U/D")
            elif "X" in event.code:
                print("Left Stick L/R")
            elif "Y" in event.code:
                print("Left Stick U/D")
        if "BTN" in event.code:
            if "NORTH" in event.code:
                print("Y")
            elif "SOUTH" in event.code:
                print("A")
            elif "WEST" in event.code:
                print("X")
            elif "EAST" in event.code:
                print("B")
            elif "TL" in event.code:
                print("LB")
            elif "TR" in event.code:
                print("RB")
            elif "START" in event.code:
                print("BACK")
                Quit = True
            elif "SELECT" in event.code:
                print("START")
    if Quit:
        break




