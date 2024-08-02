from pathlib import Path

from cathsim_controller.joystick import Joystick
from cathsim_controller.real_env import RealEnv
from cathsim_controller.utils import videos_path
import cv2

FPS = 15
FILE_PATH = videos_path
FILE_PATH.mkdir(exist_ok=True)
FILE_NAME = "interactive.mp4"
joystick = Joystick(
    left_stick_vertical_axis=1,
    right_stick_horizontal_axis=2,
)
env = RealEnv(image_width=1280, image_height=720, fps=FPS)
env.reset()

frames_directory = Path("frames")
if not frames_directory.exists():
    frames_directory.mkdir()

fourcc=cv2.VideoWriter_fourcc(*'mp4v')
out=cv2.VideoWriter(FILE_PATH/FILE_NAME,fourcc,FPS,(1280,720))

try:
    while True:
        action = joystick.get_input()
        observation, _, _, _, _ = env.step(action)
        if observation is not None:
                out.write(observation)
                cv2.imshow('Image',observation)
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break
        # pygame.time.wait(1000)
except KeyboardInterrupt:
    print("Exiting...")
    # cv2.destroyAllWindows()