import cv2
import pygame

from cathsim_controller.joystick import Joystick
from cathsim_controller.real_env import RealEnv

FPS = 8
WIDTH = 1920
HEIGHT = 1080

JOYSTICK_PAUSE_BUTTON = 0  # cross (PS),
JOYSTICK_RESET_BUTTON = 1  # circle (PS)
JOYSTICK_QUIT_BUTTON = 2  # triangle (PS)


def main():
    joystick = Joystick(
        left_stick_vertical_axis=1,
        right_stick_horizontal_axis=2,
    )

    env = RealEnv(image_width=WIDTH, image_height=HEIGHT, fps=FPS)

    while True:
        print("Press 'x/A' to unpause, 'circle/B' to reset, 'triangle/X' to quit")
        print("Game is paused")

        is_paused = True
        is_running = True

        obs, info = env.reset()

        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == JOYSTICK_PAUSE_BUTTON:
                        is_paused = not is_paused
                        status = "paused" if is_paused else "unpaused"
                        print(f"Recording {status}")
                    if event.button == JOYSTICK_RESET_BUTTON:
                        image = obs["pixels"]
                        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                        is_running = False
                    if event.button == JOYSTICK_QUIT_BUTTON:
                        exit()

            if is_paused:
                continue

            image = obs["pixels"]
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            cv2.imshow("Image", image)
            cv2.waitKey(1)

            action = joystick.get_input()
            obs, _, _, _, _ = env.step(action)


if __name__ == "__main__":
    main()
