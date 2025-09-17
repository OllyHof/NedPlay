import time
import pyniryo as bot
import inputs as control

for device in control.devices.gamepads:
    print(device)

if not control.devices.gamepads:
    print("No gamepad devices found")

while control.devices.gamepads:
    events = control.get_gamepad()
    for event in events:
       print(event.ev_type, event.code, event.state)