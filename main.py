import math
import inputs as control
from pyniryo import NiryoRobot, JointsPosition

# Setting Startup joint positions
Base = 0
Shoulder = 0
Arm = 0
Elbow = 0
Wrist = 0
Hand = 0

# Starting Controller Readout Sets
Joystick_State = {
    "ABS_RX": 0,
    "ABS_RY": 0,
    "ABS_X": 0,
    "ABS_Y": 0,
}

Trigger_State = {
    "ABS_Z": 0,
    "ABS_RZ": 0,
}

Button_State = {
    "BTN_NORTH": 0,
    "BTN_SOUTH": 0,
    "BTN_EAST": 0,
    "BTN_WEST": 0,
    "BTN_START": 0,
    "BTN_SELECT": 0,
    "BTN_TR": 0,
    "BTN_TL": 0,
    "BTN_THUMBL": 0,
    "BTN_THUMBR": 0,
}
D_Pad_State = {
    "ABS_HATOX": 0,
    "ABS_HATOY": 0,
}
# Connecting to ro#bot
IP = "192.168.1.10"
#bot = NiryoRo#bot(IP)
#bot.calibrate_auto()
#bot.update_tool()

# 
Quit = False

#Printing Found Gamepads
for device in control.devices.gamepads:
    print(device)
#Printing Not found Gamepads
if not control.devices.gamepads:
    print("No gamepad devices found")

#Main
while control.devices.gamepads:
    events = control.get_gamepad()
    for event in events:
        if Quit:
            break
        #bot.move(JointsPosition(Base, Shoulder, Arm, Elbow, Wrist, Hand))
        if "ABS_" in event.code:
            if not "Z" in event.code:
                if event.code in Joystick_State :
                    Joystick_State[event.code] = math.ceil(100*event.state/32786)
                else :
                    D_Pad_State[event.code] = event.state

            elif "Z" in event.code:
                Trigger_State[event.code] = math.ceil(100*event.state/255)

        if "BTN" in event.code:
            Button_State[event.code] = event.state
            if "START" in event.code:
                Quit = True
    for i in range(100):
        print("")

    print("Joystick State: ", Joystick_State)
    print("Trigger State: ", Trigger_State)
    print("Button State: ", Button_State)


    if Quit:
        break

#bot.close_connection()



