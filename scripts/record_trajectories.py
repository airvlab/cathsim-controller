import json
from pathlib import Path

import cv2
import numpy as np
import pygame
from cathsim_controller.joystick import Joystick
from cathsim_controller.real_env import RealEnv

FPS = 8
WIDTH = 1920
HEIGHT = 1080


TRAJECTORIES_DIR = Path("trajectories")
TRAJECTORIES_DIR.mkdir(exist_ok=True)


TRAJECTORY_PATH = TRAJECTORIES_DIR / "trajectories.json"

NUM_EPISODES = sum(1 for _ in TRAJECTORIES_DIR.glob("episode_*"))


JOYSTICK_PAUSE_BUTTON = 0  # cross (PS),
JOYSTICK_RESET_BUTTON = 1  # circle (PS)
JOYSTICK_QUIT_BUTTON = 2  # triangle (PS)


def init():
    joystick = Joystick(
        left_stick_vertical_axis=1,
        right_stick_horizontal_axis=2,
    )

    env = RealEnv(image_width=WIDTH, image_height=HEIGHT, fps=FPS)
    return joystick, env


def record_trajectory(env, joystick, path):
    while True:
        print("Press 'x/A' to unpause, 'circle/B' to reset, 'triangle/X' to quit")
        print("Game is paused")

        is_paused = True
        is_running = True

        obs, info = env.reset()

        actions = []
        while is_running:
            for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == JOYSTICK_PAUSE_BUTTON:
                        is_paused = not is_paused
                        status = "paused" if is_paused else "unpaused"
                        print(f"Recording {status}")
                    if event.button == JOYSTICK_RESET_BUTTON:
                        actions.append(None)
                        image = obs["pixels"]
                        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                        cv2.imwrite(path, image)
                        print(path / "actions.npy")
                        np.save(path / "actions.npy", actions)

                        is_running = False

            if is_paused:
                continue

            image = obs["pixels"]
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(path, image)

            cv2.imshow("Image", image)
            cv2.waitKey(1)

            action = joystick.get_input()

            actions.append(action)
            obs, _, _, _, _ = env.step(action)


def read_episodes(path):
    if path.exists():
        episodes = json.load(open(path))
        return episodes
    return []


def clean_trajectories(episodes):
    new_episodes = []
    for i, trajectory in enumerate(episodes):
        new_trajectory_path = TRAJECTORIES_DIR / f"episode_{i}"
        new_trajectory = []

        for step in trajectory:
            frame_path = Path(step["observation"])

            new_frame_path = new_trajectory_path / frame_path.name
            step["observation"] = str(new_frame_path)

            new_trajectory.append(step)

        new_episodes.append(new_trajectory)

    return new_episodes


def main():
    joystick, env = init()

    episodes = read_episodes(TRAJECTORY_PATH)
    clean_trajectories(episodes)
    exit()
    episode_id = len(episodes)
    try:
        while True:
            traj_dir = TRAJECTORIES_DIR / f"episode_{episode_id}"
            traj_dir.mkdir(exist_ok=True)

            episode, frames = record_trajectory(env, joystick)
            for i, frame in enumerate(frames):
                frame_path = traj_dir.joinpath(f"{i}.jpg")
                episode[i]["observation"] = frame_path.relative_to(TRAJECTORIES_DIR).as_posix()
                cv2.imwrite(frame_path, frame)
            episodes.append(episode)

            with open(TRAJECTORY_PATH, "w") as f:
                json.dump(episodes, f, indent=2)

            episode_id += 1

    except KeyboardInterrupt:
        print("KeyboardInterrupt:Exiting...")
        env.reset()
        cv2.destroyAllWindows()
        # json_path = trajectories_dir / f"episode_{episode_id}.json"
        # with open(json_path, "w") as f:
        #     json.dump(episode, f, indent=4)


if __name__ == "__main__":
    main()
