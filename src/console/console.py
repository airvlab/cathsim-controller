import pygame
from pygame import joystick


class Console:
    def __init__(self) -> None:
        pygame.init()
        # Init the  Joystick module
        if not joystick.get_init():
            joystick.init()
        self.num_joystick = joystick.get_count()
        self.joystick_obj = [
            joystick.Joystick(i) for i in range(self.num_joystick)
        ]
        self.track_id = 0

    def __del__(self) -> None:
        for i in range(self.num_joystick):
            ## quit the joystick object.
            if self.joystick_obj[i].get_init():
                self.joystick_obj[i].quit()
        if joystick.get_init():
            # uninstall the module.
            joystick.quit()
        pygame.quit()

    def choose_joystick(self):
        print(
            f"You have {self._num_joystick } consoles; {self.get_info().joystick_items()}"
        )
        input_user = input("which console are you gonna to use(default 0):")
        if not input_user.strip():
            self.track_id = 0
        try:
            self.track_id = int(input_user)
        except ValueError:
            print("Not a valid integer value, will be set as default 0")
            self.track_id = 0
        if self.track_id < 0 or self.track_id >= self.num_joystick:
            print("Value out of ranges, will be set as default 0")
            self.track_id = 0
        # update the axis
        self.get_axis()
    def get_info(self) -> dict:
        joystick_items = []
        for i in range(self.num_joystick):
            joystick_items.append({
                "id": i,
                "name": self.joystick_obj[i].get_name()
            })
        return dict(num=self.num_joystick, joystick_items=joystick_items)
    def get_axis(self):
        # get the axis that need to be track
        self.axis_id=[0, 3]
        if "Sony" in self.joystick_obj[self.track_id].get_name():
            self.axis_id= [0, 3]
        elif "Google" in self.joystick_obj[self.track_id].get_name():
            self.axis_id=[0, 2]
    def track_axis(self):
        return (
                    self.joystick_obj[id].get_axis(i) for i in self.axis_id
                )
        pass
    def track_axis(self):
        pass


if __name__ == "__main__":
    my_console = Console()
    # print(my_console.get_info())
