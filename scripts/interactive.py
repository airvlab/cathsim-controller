from cathsim_controller.joystick import Joystick
from cathsim_controller.real_env import RealEnv
from moviepy.editor import ImageSequenceClip
from pathlib import Path
import cv2
import time

FPS = 30
FILE_PATH = Path.cwd() / "movies"
FILE_PATH.mkdir(exist_ok=True)
FILE_NAME = "interactive.mp4"
joystick = Joystick(left_stick_vertical_axis= 1, right_stick_horizontal_axis= 2,)
env = RealEnv()
env.reset()

frames_directory = Path("frames")
if not frames_directory.exists():
    frames_directory.mkdir()

frames = []    
try:
    # cur_time = time.time()
    # req_time = 60
    # time.time()-cur_time<req_time
    while True:
        action=joystick.get_input()
        observation,_,_,_,_ = env.step(action)
        # frames.append(observation)
        # observation = cv2.cvtColor(observation, cv2.COLOR_RGB2BGR)
        # cv2.imshow("Image", observation)
        # cv2.waitKey(.1)
        # pygame.time.wait(100)
# except KeyboardInterrupt:
finally:
    print("Exiting...")
    # cv2.destroyAllWindows()
    clip = ImageSequenceClip(frames, fps=FPS)
    clip.write_videofile((FILE_PATH / FILE_NAME).as_posix(), codec="libx264")
