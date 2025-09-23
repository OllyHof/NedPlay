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
prev_state = (Base, Shoulder, Arm, Elbow, Wrist, Hand)

# Encoder factor for joystick/triggers
joystick_encoder_bits = 16
trigger_encoder_bits = 8

joystick_encoder_bit = math.ceil(math.pow(2, joystick_encoder_bits)/2)
trigger_encoder_bit = math.pow(2, trigger_encoder_bits)-1

# Limit a value within given min/max joint boundaries
def lim(n, minn, maxn):
    return max(min(maxn, n), minn)

# Make robot move
def update_Joint(joystick_state, joint, limitmin, limitmax):
    if 25 < joystick_state< 50:
        joint = joint + 0.0296
    elif 50 < joystick_state < 75:
        joint = joint + 0.0592
    elif 75 < joystick_state < 100:
        joint = joint + 0.0888
    elif joystick_state == 100:
        joint = joint + 0.1184
    elif -50 < joystick_state < -25:
        joint = joint - 0.0296
    elif -75 < joystick_state < -50:
        joint = joint - 0.0592
    elif -100 < joystick_state < -75:
        joint = joint - 0.0888
    elif joystick_state == -100:
        joint = joint - 0.1184
    joint = lim(joint, limitmin, limitmax)
    return joint

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
prev_button_state = Button_State.copy()

# -----------------------------
# Connect to robot
# -----------------------------

IP = "169.254.200.200"
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
        if event.code in Joystick_State:  # Joysticks or D-Pad
            # Joystick is converted to % (-100 to 100)
            Joystick_State[event.code] = math.ceil(100 * event.state / joystick_encoder_bit)
        if event.code in D_Pad_State:
            D_Pad_State[event.code] = event.state
        if event.code in Trigger_State:  # Triggers
            # Trigger is converted to % (0 to 100)
            Trigger_State[event.code] = math.ceil(100 * event.state / trigger_encoder_bit)

        # Button input
        if "BTN" in event.code:
            Button_State[event.code] = event.state
            if event.code == "BTN_START":
                Quit = True




    # Debug: print actual joint positions
    #print(bot.get_joints())

    # Update joint values based on joystick/trigger input
    #Base
    Base = update_Joint(Joystick_State["ABS_RX"], Base, -2.96, 2.96)
    #Shoulder
    Shoulder = update_Joint(-Joystick_State["ABS_RY"], Shoulder, -2.09, 0.61)
    #Arm
    Arm = update_Joint(Joystick_State["ABS_Y"], Arm, -1.34, 1.57)
    #Elbow
    Elbow = update_Joint(Joystick_State["ABS_X"], Elbow, -2.09, 2.09)
    #Wrist
    Wrist = update_Joint(Trigger_State["ABS_Z"], Wrist, -1.92, 1.57)
    Wrist = update_Joint(-Trigger_State["ABS_RZ"], Wrist, -1.92, 1.57)


    # Gripper control using bumpers
    if Button_State["BTN_TR"] == 1:
        bot.grasp_with_tool()
    if Button_State["BTN_TL"] == 1:
        bot.release_with_tool()
    if Button_State["BTN_SELECT"] == 1:
        Base = 0
        Shoulder = 0
        Arm = 0
        Elbow = 0
        Wrist = 0
        Hand = 0
    if Button_State["BTN_NORTH"] == 1:
        Hand = 0
    if Button_State["BTN_SOUTH"] == 1 and prev_button_state["BTN_SOUTH"] == 0:
        Hand = Hand/2
    if Button_State["BTN_EAST"] == 1:
        Hand = math.pi/2
    if Button_State["BTN_WEST"] == 1:
        Hand = math.pi/2


    if Quit:
        break

    prev_button_state = Button_State.copy()
    # Send updated joint positions to robot
    new_state = (Base, Shoulder, Arm, Elbow, Wrist, Hand)
    if new_state != prev_state:
        bot.move_joints(JointsPosition(*new_state))
        prev_state = new_state  # save update
        print("Base: ", Base)
        print("Shoulder: ", Shoulder)
        print("Arm: ", Arm)
        print("Elbow: ", Elbow)
        print("Wrist: ", Wrist)
# -----------------------------
# Close connection when exiting
# -----------------------------
bot.close_connection()
