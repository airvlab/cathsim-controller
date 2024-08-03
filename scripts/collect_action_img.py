from pathlib import Path

import cv2
import numpy as np
from cathsim_controller.joystick import Joystick
from cathsim_controller.real_env import RealEnv

from .utils import videos_path as VIDEOS_PATH
from .utils import img_path as IMG_PATH

FPS = 15
WIDTH = 1280
HEIGHT = 720

VIDEOS_PATH.mkdir(exist_ok=True)
IMG_PATH.mkdir(exist_ok=True)


def init():
    joystick = Joystick(
        left_stick_vertical_axis=1,
        right_stick_horizontal_axis=2,
    )

    env = RealEnv(image_width=WIDTH, image_height=HEIGHT, fps=FPS)
    env.reset()

    frames_directory = Path("frames")
    if not frames_directory.exists():
        frames_directory.mkdir()
    return joystick, env


def resize_image(image, new_width: int = 1024, new_height=1024):
    a = 0.5
    if a < 1:
        resized_image = cv2.resize(image, (new_width, new_height))
        return resized_image
    else:
        # keep the same shape
        # original size
        original_height, original_width = image.shape[:2]
        black_pudding_image = np.zeros((new_width, new_height, 3), dtype=np.uint8)
        scale = min(new_width / original_width, new_height / original_height)
        same_ratio_image = cv2.resize(
            image, (original_width * scale, original_height * scale)
        )
        height_pudding = (new_height - original_height * scale) // 2
        width_pudding = (new_width - original_width * scale) // 2
        black_pudding_image[
            height_pudding : height_pudding + new_height,
            width_pudding : width_pudding + new_width,
        ] = same_ratio_image
        return black_pudding_image


def run(joystick: Joystick, env: RealEnv, episode_id: int):
    video_filename = f"interactive{episode_id}.mp4"

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(VIDEOS_PATH / video_filename, fourcc, FPS, (WIDTH, HEIGHT))
    step = 1
    episode = []
    path = IMG_PATH / episode_id
    path.mkdir(exist_ok=True)
    try:
        while True:
            action = joystick.get_input()
            observation, _, _, _, _ = env.step(action)
            image = observation["pixels"]
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            out.write(image)
            cv2.imshow("Image", image)
            # resize it
            image = resize_image(image=image)
            # save the img after action
            image_filename = f"step_{step}.jpg"
            cv2.imwrite(path / image_filename, image)
            episode.append({"step": step, "action": action, "image": image_filename})
            step += 1
    except KeyboardInterrupt:
        print("Exiting...")
        cv2.destroyAllWindows()


if __name__ == "__main__":
    joystick, env = init()
    episode_num = 10
    for i in episode_num:
        run(joystick, env, i)
