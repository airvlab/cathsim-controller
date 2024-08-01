import pygame
from pygame import joystick


class JoyStick:
    def __init__(
        self,
        controller_id: int = 0,
        left_stick_vertical_axis: int = 1,
        right_stick_horizontal_axis: int = 3,
    ):
        pygame.init()
        self.joystick = pygame.joystick.Joystick(controller_id)

        print(f"Joystick connected: {self.joystick.get_name()}")
        print(f"Number of axes: {self.joystick.get_numaxes()}")
        self._left_stick_axis = left_stick_vertical_axis
        self._right_stick_axis = right_stick_horizontal_axis

    def get_input(self):
        pygame.event.pump()
        vertical_position = self.joystick.get_axis(self._left_stick_axis)
        horizontal_position = self.joystick.get_axis(self._right_stick_axis)

        # Needs to be inverted as the axis returns -1 when pushed up
        vertical_position = -vertical_position
        return vertical_position, horizontal_position

    def __del__(self):
        pygame.quit()


if __name__ == "__main__":
    joystick = JoyStick()
    try:
        while True:
            print(joystick.get_input())
            pygame.time.wait(100)
    except KeyboardInterrupt:
        print("Exiting...")
        pygame.quit()
