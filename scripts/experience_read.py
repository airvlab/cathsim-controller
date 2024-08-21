from pathlib import Path
import json
import sys
import cv2
import numpy as np
from imitation.data.types import Trajectory

frames_directory = Path("frames")
data_directory=frames_directory/"data"

def read(num:int,start_id:int)->dict:
    episodes={}
    for i in range(start_id,start_id+num):
        file_path = frames_directory/f"episode_{i}.json"
        with open(file_path, 'r') as f:
            episodes[f"episode_{i}"] = json.load(f)
    return episodes

def read_as_trajatory(num:int,start_id:int)->Trajectory:
    episodes=read(num=num,start_id=start_id)
    trajectories = []
    for episode in episodes.values():
        actions=[]
        images=[]
        for step in episode.values():
            info_path=step.get("info_path")
            if info_path is not None: 
                action=np.load(info_path)['action']
                actions.append(action)
            image_path=step.get("image_path")
            image=cv2.imread(image_path)
            # print(f"action {action}, image {image}")
            images.append(image)
        trajectory = Trajectory(
            obs=np.array(images),
            acts=np.array(actions),
            infos=None,
            terminal=True
            )
        trajectories.append(trajectory)
    return trajectories

# def read_flattened_episodes(num:int,start_id:int)->dict:
#     episodes=read(num=num,start_id=start_id)
#     actions=[]
#     images=[]
#     for episode in episodes.values():
#         for step in episode.values():
#             info_path=step["info_path"]
#             image_path=step["image_path"]
#             action=np.load(info_path)['action']
#             image=cv2.imread(image_path)
#             # print(f"action {action}, image {image}")
#             actions.append(action)
#             images.append(image)
            
#     # print(f"actions {actions}, images {images}")
#     observation=np.array(images)
#     actions=np.array(actions)
#     return {'observation':observation,'actions':actions}

if __name__ == "__main__":
    # num = int(sys.argv[1])
    # start_id = int(sys.argv[2])
    # read(num=num,start_id=start_id)
    from imitation.data import rollout

    # Flatten the trajectories into transitions
    episodes=read_as_trajatory(num=1,start_id=1)
    print(episodes)
    transitions = rollout.flatten_trajectories(episodes)
    print(transitions)
