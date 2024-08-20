from pathlib import Path
import json
import sys
import cv2
import numpy as np

frames_directory = Path("frames")
data_directory=frames_directory/"data"

def read(num:int,start_id:int):
    episodes={}
    for i in range(start_id,start_id+num):
        file_path = frames_directory/f"episode_{i}.json"
        with open(file_path, 'r') as f:
            episodes[f"episode_{i}"] = json.load(f)
    info_path=episodes[f"episode_{start_id}"][f"step_{1}"]["info_path"]
    image_path=episodes[f"episode_{start_id}"][f"step_{1}"]["image_path"]
    data=np.load(info_path)
    # data['action']
    # data['reward']
    # data['terminated']
    # print(data['action'],data['reward'],data['terminated'],data['truncated'],data['info'])
    # data['action']
    print(data['reward'])
    image=cv2.imread(image_path)
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    num = int(sys.argv[1])
    start_id = int(sys.argv[2])
    read(num=num,start_id=start_id)