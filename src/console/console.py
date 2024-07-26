import pygame
from pygame import joystick, event, time, JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED, QUIT



class Console:

    def __init__(self) -> None:
        # Init the  Joystick module
        if not joystick.get_init():
            joystick.init()
        self._num_joystick = joystick.get_count()
        self.joystick_obj = [
            joystick.Joystick(i) for i in range(self._num_joystick)
        ]

    def __del__(self) -> None:
        for i in range(self._num_joystick):
            ## quit the joystick object.
            if self.joystick_obj[i].get_init():
                self.joystick_obj[i].quit()
        if joystick.get_init():
            # uninstall the module.
            joystick.quit()

    def track_axis(self, id) -> None:
        done = False
        Axis_id = [0, 3]
        if "Sony" in self.joystick_obj[id].get_name():
            Axis_id = [0, 3]
        elif "Google" in self.joystick_obj[id].get_name():
            Axis_id = [0, 2]
        while not done:
            for events in event.get():
                if events.type == QUIT:
                    done = True  # Flag that we are done so we exit this loop.
                if events.type == JOYAXISMOTION:
                    (left_control,
                     right_control) = (self.joystick_obj[id].get_axis(i)
                                       for i in Axis_id)
                    if abs(left_control-0)>1e-1 or abs(right_control-0)>1e-1:
                        print(left_control, right_control)
                if events.type == JOYBUTTONDOWN:
                    done = True

    def get_info(self) -> dict:
        joysticks = []
        for i in range(self._num_joystick):
            joysticks.append(dict(id=i, name=self.joystick_obj[i].get_name()))
        return dict(num=self._num_joystick, joysticks=joysticks)


if __name__ == "__main__":
    pygame.init()
    # Used to manage how fast the screen updates.
    clock = time.Clock()

    my_console = Console()
    print(my_console.get_info())
    my_console.track_axis(0)
    pygame.quit()
