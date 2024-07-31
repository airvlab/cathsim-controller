from console import Console
from controller import RealEnv
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
            action=action_queue.get()
            env.step(action)

# set the function that get the input from console
def console_getinput():
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
                if abs(new_right_control - 0) > 1e-1 or abs(new_right_control - 0) > 1e-1:
                    # print(new_right_control, new_right_control)
                    deal_data(translation=new_right_control, rotation=new_right_control, end=False)
                elif (
                    abs(left_control - new_left_control) < 1e-2
                    or abs(right_control - new_right_control) < 1e-2
                ):
                    deal_data(translation=new_right_control, rotation=new_right_control, end=True)
                (left_control, right_control) = (new_left_control, new_right_control)
            if events.type == JOYBUTTONDOWN:
                done = True
def deal_data(translation, rotation, end):
    (cum_translation, cum_rotation) = (cum_translation+translation / 15. , cum_rotation + rotation / 15.)
    if cum_translation > 1.0 or cum_rotation > 1.0 or cum_translation < -1.0 or cum_rotation < -1.0 or (end and  (abs(cum_translation - 0) > 1e-1 or abs(cum_rotation - 0) > 1e-1)):
        action = [cum_translation, cum_rotation]
        action_queue.put(action)
        cum_translation, cum_rotation = 0, 0

thread_console=threading.Thread(target=console_getinput)
thread_console.start()
thread_controller=threading.Thread(target=operate_motor)
thread_controller.start()