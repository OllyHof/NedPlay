import math

import pyniryo
import inputs as control
from pyniryo import NiryoRobot

IP = "192.168.1.10"
bot = NiryoRobot(IP)

bot.calibrate_auto()
bot.update_tool()
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
                if event.state < 0:
                    print("Right Stick Left", math.ceil((event.state/32768)*-100), "%")
                else:
                    print("Right Stick Right", math.ceil((event.state/32768)*100), "%")

            elif "RY" in event.code:
                if event.state > 0:
                    print("Right Stick Up", math.ceil((event.state/32768)*100), "%")
                else:
                    print("Right Stick Down", math.ceil((event.state/32768)*-100), "%")

            elif "X" in event.code:
                if event.state == -1:
                    print("D-Pad Left")
                elif event.state == 1:
                    print("D-Pad Right")
                elif event.state == 0:
                    ()
                else:
                    if event.state > 0:
                        print("Left Stick Right", math.ceil((event.state/32768)*100), "%")
                    else:
                        print("Left Stick Left", math.ceil((event.state/32768)*-100), "%")

            elif "Y" in event.code:
                if event.state == 1:
                    print("D-Pad Down")
                elif event.state == -1:
                    print("D-Pad Up")
                elif event.state == 0:
                    ()
                else:
                    if event.state > 0:
                        print("Left Stick Up", math.ceil((event.state/32768)*100), "%")
                    else:
                        print("Left Stick Down", math.ceil((event.state/32768)*-100), "%")

            elif "_RZ" in event.code:
                print("Right Trigger", math.ceil((event.state/255)*100), "%")

            elif "_Z" in event.code:
                print("Left Trigger", math.ceil((event.state/255)*100), "%")

        if "BTN" in event.code:
            if event.state == 1:
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

bot.close_connection()



