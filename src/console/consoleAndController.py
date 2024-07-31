import sys
import os

# Add the src directory to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../cathsim_controller"))
)

from cathsim_controller.real_env import RealEnv
from console import Console
import queue
import threading
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


action_queue = queue.Queue()


# set the function (will be controlled by the thread) that can store and deal with the data. In the meanwhile that it can be set the machine move when the condition satisfy the need
def operate_motor():
    # initial the env
    env = RealEnv(width=80, height=80)
    env.reset()

    # get the action queue
    while True:
        if not action_queue.empty():
            action = action_queue.get()
            print(f"{action} from motor")
            env.step(action)


# set the function that get the input from console
def console_getinput():
    # Initial console
    myconsole = Console()

    # track the axis
    (left_control, right_control) = (0, 0)
    done = False
    while not done:
        for events in event.get():
            if events.type == QUIT:
                done = True  # Flag that we are done so we exit this loop.
            if events.type == JOYAXISMOTION:
                (left_control, right_control) = myconsole.track_axis()
                action = [left_control, right_control]
                action_queue.put(action)
                print(f"{action} from console")
            if events.type == JOYBUTTONDOWN:
                done = True


thread_console = threading.Thread(target=console_getinput)
thread_console.start()
thread_controller = threading.Thread(target=operate_motor)
thread_controller.start()
