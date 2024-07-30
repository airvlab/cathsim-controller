from console import Console
from controller import RealEnv
import queue
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
def handle_input():
    # Initial console
    myconsole = Console()
    # get the axis that need to be track
    axis_id = [0, 3]
    if "Sony" in self.joystick_obj[self.track_id].get_name():
        axis_id = [0, 3]
    elif "Google" in self.joystick_obj[self.track_id].get_name():
        axis_id = [0, 2]
    
    # track the axis
    done = False
    while not done:
        for events in event.get():
            if events.type == QUIT:
                done = True  # Flag that we are done so we exit this loop.
            if events.type == JOYAXISMOTION:
                (new_left_control, new_right_control) = (
                    self.joystick_obj[id].get_axis(i) for i in axis_id
                )
                if abs(new_right_control - 0) > 1e-1 or abs(new_right_control - 0) > 1e-1:
                    print(new_right_control, new_right_control)
                    self.deal_data(translation=new_right_control, rotation=new_right_control, end=False)
                elif (
                    abs(self.left_control - new_left_control) < 1e-2
                    or abs(self.right_control - new_right_control) < 1e-2
                ):
                    self.deal_data(translation=new_right_control, rotation=new_right_control, end=True)
                (self.left_control, self.right_control) = (new_left_control, new_right_control)
            if events.type == JOYBUTTONDOWN:
                done = True
def deal_data(self, translation, rotation, end):
    cum_translation, cum_rotation += translation / 15., rotation / 15.
    if end or cum_translation > 1.0 or cum_rotation > 1.0 or cum_translation < -1.0 or self.cum_rotation < -1.0:
        action = [self.cum_translation, self.cum_rotation]
        self.env.step(action)
        self.cum_translation, self.cum_rotation = 0, 0
    return
    
