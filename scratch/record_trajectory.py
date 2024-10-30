import sys
from pathlib import Path

import cv2
import numpy as np
from cathsim_controller.joystick import Joystick
from icra.env import RealEnv

FPS = 8
WIDTH = 1920
HEIGHT = 1080


trajectories_directory = Path.cwd() / "trajectories-simple"
if not trajectories_directory.exists():
    trajectories_directory.mkdir()


def record_trajectory(episode_id: int):
    trajectory_path = trajectories_directory / f"{episode_id}.npz"
    if trajectory_path.exists():
        retake_trajectory = input("Trajectory exists. Rewrite? y/N: ") == "y"
        if not retake_trajectory:
            exit()

    joystick = Joystick(
        left_stick_vertical_axis=1,
        right_stick_horizontal_axis=2,
    )

    env = RealEnv(image_width=WIDTH, image_height=HEIGHT, fps=FPS)

    try:
        step = 0
        obs, _ = env.reset()
        observations = []
        actions = []
        while True:
            cv2.imshow("Image", cv2.cvtColor(obs, cv2.COLOR_RGB2BGR))

            action = joystick.get_input()
            next_obs, _, _, _, _ = env.step(action)

            observations.append(obs)
            actions.append(action)

            obs = next_obs
            step += 1

            if cv2.waitKey(1) & 0xFF == ord("q"):
                observations.append(obs)

                np.savez(
                    trajectories_directory / f"{episode_id}.npz",
                    observations=observations,
                    actions=actions,
                )

                # trajectory = Trajectory(
                #     obs=observations, acts=actions, infos=None, terminal=True
                # )

                print(f"Episode {episode_id} ends")
                env.reset()
                cv2.destroyAllWindows()
                break

    except KeyboardInterrupt:
        print("KeyboardInterrupt:Exiting...")
        observations.append(obs)

        np.savez(
            trajectories_directory / f"{episode_id}.npz",
            observations=observations,
            actions=actions,
        )

        print(f"Episode {episode_id} ends")
        env.reset()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    episode_id = sys.argv[1]
    record_trajectory(episode_id=episode_id)
