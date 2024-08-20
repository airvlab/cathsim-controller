from pathlib import Path

frames_directory = Path("frames")
data_directory=frames_directory/"data"

def read(num=num,start_id=start_id):
    episodes={}
    for i in range(start_id,start_id+num):
        


if __name__ == "__main__":
    num = sys.argv[1]
    start_id = sys.argv[2]
    read(num=num,start_id=start_id)