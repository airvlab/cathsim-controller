import threading
from pathlib import Path

import cv2

from cathsim_controller.joystick import Joystick
from cathsim_controller.real_env import RealEnv

VIDEOS_PATH = Path.cwd() / "videos"

FPS = 8
WIDTH = 1920
HEIGHT = 1080

VIDEOS_PATH.mkdir(exist_ok=True)
FILE_NAME = "interactive.mp4"

joystick = Joystick(
    left_stick_vertical_axis=1,
    right_stick_horizontal_axis=2,
)

env = RealEnv(image_width=WIDTH, image_height=HEIGHT, fps=FPS)
env.reset()

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter(VIDEOS_PATH / FILE_NAME, fourcc, FPS, (WIDTH, HEIGHT))

try:
    while True:
        action = joystick.get_input()

        # Queue the next action while the current one is processing
        threading.Thread(target=env.step, args=(action,)).start()

        # Get the observation (camera image)
        observation, _, _, _, _ = env.step(action)
        image = observation["pixels"]
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        out.write(image)
        cv2.imshow("Image", image)
        cv2.waitKey(1)

except KeyboardInterrupt:
    print("Exiting...")
    env.reset()
    out.release()
    cv2.destroyAllWindows()
