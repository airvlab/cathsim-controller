from pathlib import Path

import sys
import cv2
import json
import numpy as np
from cathsim_controller.joystick import Joystick
from cathsim_controller.real_env import RealEnv

FPS = 15
WIDTH = 1280
HEIGHT = 720
# FPS = 8
# WIDTH = 1920
# HEIGHT = 1080
        

frames_directory = Path("frames")
if not frames_directory.exists():
    frames_directory.mkdir()
data_directory=frames_directory/"data"
data_directory.mkdir(exist_ok=True)

def init():
    joystick = Joystick(
        left_stick_vertical_axis=1,
        right_stick_horizontal_axis=2,
    )

    env = RealEnv(image_width=WIDTH, image_height=HEIGHT, fps=FPS)
    env.reset()
    return joystick, env

def run(joystick: Joystick, env: RealEnv, episode_id: int):
    # fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    # out = cv2.VideoWriter(data_directory / FILE_NAME, fourcc, FPS, (WIDTH, HEIGHT))
    step = 1
    episode = {}
    data_path = frames_directory / f"episode_{episode_id}"
    data_path.mkdir(exist_ok=True)
    try:
        while True:
            
            action = joystick.get_input()
            observation, reward, terminated, truncated, info  = env.step(action)
            
            image = observation["pixels"]
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            #show 
            cv2.imshow("Image", image)
        
            # image file
            image_filename = f"step_{step}.jpg"
            info_filename = f"step_{step}.npz"
            cv2.imwrite(data_path / image_filename, image)
            np.savez(data_path / info_filename,action=action,reward=reward, terminated=terminated, truncated=truncated, info=info)
            
            step_data={"image_path": f"{data_path}/{image_filename}", "info_path":f"{data_path}/{info_filename}"}
            # episode add
            episode[f"step_{step}"]=step_data
            
            step += 1
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print(f"Episode {episode_id} ends")
                env.reset()
                cv2.destroyAllWindows()
                return episode
            
    except KeyboardInterrupt:
        print("KeyboardInterrupt:Exiting...")
        env.reset()
        cv2.destroyAllWindows()
        return episode

def write(episode_id: int):
    joystick = Joystick(
        left_stick_vertical_axis=1,
        right_stick_horizontal_axis=2,
    )

    env = RealEnv(image_width=WIDTH, image_height=HEIGHT, fps=FPS)
    env.reset()

    step = 1
    episode = {}

    data_path = data_directory / f"episode_{episode_id}"
    data_path.mkdir(exist_ok=True)
    try:
        while True:
            
            action = joystick.get_input()
            observation, reward, terminated, truncated, info  = env.step(action)
            
            image = observation["pixels"]
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            #show 
            cv2.imshow("Image", image)
        
            # image file
            image_filename = f"step_{step}.jpg"
            info_filename = f"step_{step}.npz"
            cv2.imwrite(data_path / image_filename, image)
            np.savez(data_path / info_filename,action=action,reward=reward, terminated=terminated, truncated=truncated, info=info)
            
            step_data={"image_path": f"{data_path}/{image_filename}", "info_path":f"{data_path}/{info_filename}"}
            # episode add
            episode[f"step_{step}"]=step_data
            
            step += 1
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print(f"Episode {episode_id} ends")
                env.reset()
                sleep(1)
                cv2.destroyAllWindows()
                json_path=frames_directory/f"episode_{episode_id}.json"
                with open(json_path,'w') as f:
                    json.dump(episode,f,indent=4)
                break
            
    except KeyboardInterrupt:
        print("KeyboardInterrupt:Exiting...")
        env.reset()
        cv2.destroyAllWindows()
        json_path=frames_directory/f"episode_{episode_id}.json"
        with open(json_path,'w') as f:
            json.dump(episode,f,indent=4)


# if __name__ == "__main__":
#     joystick, env = init()
#     episode_num = 2
#     episodes={}
#     for i in range(episode_num):   
#         print(f"Episode {i} begins")
#         episodes[f"episode_{i}"]=run(joystick, env, i)
#     json_path=data_directory/"episodes.json"
#     with open(json_path,'w') as f:
#         json.dump(episodes,f,indent=4)
if __name__ == "__main__":
    episode_id = sys.argv[1]
    write(episode_id=episode_id)