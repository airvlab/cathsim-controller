from console import Console
from pygame import (
    joystick,
    event,
    time,
    JOYAXISMOTION,
    JOYBALLMOTION,
    JOYBUTTONDOWN,
    JOYBUTTONUP,
    JOYHATMOTION,
    JOYDEVICEADDED,
    JOYDEVICEREMOVED,
    QUIT,
)


# Initial console
myconsole = Console()
# track the axis
(left_control, right_control) =(0,0)
done = False
while not done:
    for events in event.get():
        if events.type == QUIT:
            done = True  # Flag that we are done so we exit this loop.
        if events.type == JOYAXISMOTION:
            (new_left_control, new_right_control) = myconsole.track_axis()
            print(new_left_control, new_right_control)
            # if abs(new_right_control - 0) > 1e-1 or abs(new_right_control - 0) > 1e-1:
            #     print(new_right_control, new_right_control)
            # elif (
            #     abs(left_control - new_left_control) < 1e-2
            #     or abs(right_control - new_right_control) < 1e-2
            # ):
            #     print(new_right_control, new_right_control)
            # (left_control, right_control) = (new_left_control, new_right_control)
        if events.type == JOYBUTTONDOWN:
            done = True

