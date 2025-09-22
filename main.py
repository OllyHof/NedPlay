import math
import inputs as control
from pyniryo import NiryoRobot, JointsPosition

# -----------------------------
# Robot initial joint positions
# -----------------------------

# All joints start at 0°
Base = 0
Shoulder = 0
Arm = 0
Elbow = 0
Wrist = 0
Hand = 0

# Scale factor for joystick/triggers
# (joystick values are converted to % and multiplied by SCALE)
SCALE = 0.01


# Limit a value within given min/max joint boundaries
def lim(n, minn, maxn):
    return max(min(maxn, n), minn)


# -----------------------------
# Controller state containers
# -----------------------------

# Joystick values in percentage (-100% to +100%)
Joystick_State = {
    "ABS_RX": 0,  # Right stick horizontal (X-axis)
    "ABS_RY": 0,  # Right stick vertical (Y-axis)
    "ABS_X": 0,  # Left stick horizontal (X-axis)
    "ABS_Y": 0,  # Left stick vertical (Y-axis)
}

# Trigger values in percentage (0% to 100%)
Trigger_State = {
    "ABS_Z": 0,  # Left trigger
    "ABS_RZ": 0,  # Right trigger
}

# Button state (0 = released, 1 = pressed)
Button_State = {
    "BTN_NORTH": 0,
    "BTN_SOUTH": 0,
    "BTN_EAST": 0,
    "BTN_WEST": 0,
    "BTN_START": 0,
    "BTN_SELECT": 0,
    "BTN_TR": 0,  # Right bumper
    "BTN_TL": 0,  # Left bumper
    "BTN_THUMBL": 0,
    "BTN_THUMBR": 0,
}

# D-Pad state
D_Pad_State = {
    "ABS_HATOX": 0,  # Horizontal
    "ABS_HATOY": 0,  # Vertical
}

# -----------------------------
# Connect to robot
# -----------------------------

IP = "192.168.1.10"
bot = NiryoRobot(IP)
bot.calibrate_auto()
bot.update_tool()

Quit = False

# -----------------------------
# Gamepad detection
# -----------------------------

# Print connected gamepads
for device in control.devices.gamepads:
    print(device)

# Print if no gamepads found
if not control.devices.gamepads:
    print("No gamepad devices found")

# -----------------------------
# Main control loop
# -----------------------------

while control.devices.gamepads:
    events = control.get_gamepad()
    for event in events:
        if Quit:
            break

        # Joysticks / D-Pad input
        if "ABS_" in event.code:
            if not "Z" in event.code:  # Joysticks or D-Pad
                if event.code in Joystick_State:
                    # Joystick is converted to % (-100 to 100)
                    Joystick_State[event.code] = math.ceil(100 * event.state / 32786)
                else:
                    D_Pad_State[event.code] = event.state

            elif "Z" in event.code:  # Triggers
                # Trigger is converted to % (0 to 100)
                Trigger_State[event.code] = math.ceil(100 * event.state / 255)

        # Button input
        if "BTN" in event.code:
            Button_State[event.code] = event.state
            if event.code == "BTN_START" and event.state == 1:
                Quit = True

    # Send updated joint positions to robot
    bot.move(JointsPosition(Base, Shoulder, Arm, Elbow, Wrist, Hand))

    # Debug: print actual joint positions
    print(bot.get_joints())

    # Update joint values based on joystick/trigger input
    Base =     lim(Base     + Joystick_State["ABS_RX"] * SCALE, -170, 170)
    Shoulder = lim(Shoulder + Joystick_State["ABS_RY"] * SCALE, -120, 35)
    Arm =      lim(Arm      + Joystick_State["ABS_X"]  * SCALE, -77,  90)
    Elbow =    lim(Elbow    + Joystick_State["ABS_Y"]  * SCALE, -120, 120)
    Wrist =    lim(Wrist    + Trigger_State["ABS_RZ"]  * SCALE, -100, 55)
    Hand =     lim(Hand     + Trigger_State["ABS_Z"]   * SCALE, -145, 145)

    # Gripper control using bumpers
    if Button_State["BTN_TR"] == 1:
        bot.grasp_with_tool()
    if Button_State["BTN_TL"] == 1:
        bot.release_with_tool()

    if Quit:
        break

# -----------------------------
# Close connection when exiting
# -----------------------------
bot.close_connection()
