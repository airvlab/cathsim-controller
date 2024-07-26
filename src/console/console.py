import pygame
from pygame import joystick, event, time, JOYAXISMOTION, JOYBALLMOTION, JOYBUTTONDOWN, JOYBUTTONUP, JOYHATMOTION, JOYDEVICEADDED, JOYDEVICEREMOVED, QUIT
from src.controller import RealEnv


class Console:

    def __init__(self) -> None:
        pygame.init()
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
        pygame.quit()

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
                    if abs(left_control - 0) > 1e-1 or abs(right_control -
                                                           0) > 1e-1:
                        print(left_control, right_control)
                if events.type == JOYBUTTONDOWN:
                    done = True

    def get_info(self) -> dict:
        joystick_items = []
        for i in range(self._num_joystick):
            joystick_items.append({
                "id": i,
                "name": self.joystick_obj[i].get_name()
            })
        return dict(num=self._num_joystick, joystick_items=joystick_items)


class Link_console_controller:
    def __init__(self) -> None:
        self.env = RealEnv(width=80, height=80)
        self.env.reset()
        self.console = Console()
        console_info = self.console.get_info()
        print(
            f"You have {console_info.get(num) } consoles; {console_info.get(joystick_items)}"
        )
        input_user = input("which console are you gonna to use(default 0):")
        if not input_user.strip():
            id = 0
        try:
            id = int(input_user)
        except ValueError:
            print("Not a valid integer value, will be set as default 0")
            id = 0
        if id < 0 or id >= console_info.get(num):
            print("Value out of ranges, will be set as default 0")
            id = 0

    def begin(self):
        self.console.track_axis(id)

    def deal_data(self, translation, rotation, end):
        self.cum_translation, self.cum_rotation += translation / 15., rotation / 15.
        if end or self.cum_translation > 1.0 or self.cum_rotation > 1.0 or self.cum_translation < -1.0 or self.cum_rotation < -1.0:
            action = [self.cum_translation, self.cum_rotation]
            self.env.step(action)
            self.cum_translation, self.cum_rotation = 0, 0

if __name__ == "__main__":
    # Used to manage how fast the screen updates.
    # clock = time.Clock()
    my_console = Console()
    # print(my_console.get_info())
