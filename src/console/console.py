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
        pass
        
    def get_info(self) -> dict:
        joystick_items = []
        for i in range(self._num_joystick):
            joystick_items.append({
                "id": i,
                "name": self.joystick_obj[i].get_name()
            })
        return dict(num=self._num_joystick, joystick_items=joystick_items)

    def deal_data(self, translation, rotation, end):
        cum_translation, cum_rotation += translation / 15., rotation / 15.
        if end or cum_translation > 1.0 or cum_rotation > 1.0 or cum_translation < -1.0 or self.cum_rotation < -1.0:
            action = [self.cum_translation, self.cum_rotation]
            self.env.step(action)
            self.cum_translation, self.cum_rotation = 0, 0
        return 

if __name__ == "__main__":
    my_console = Console()
    # print(my_console.get_info())
