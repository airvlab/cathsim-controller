# from src.controller.wrapper.controller import Controller
# from src.controller.wrapper.camera import Camera
from wrapper import Camera
from wrapper import Controller
import cv2

class RealEnv:
    _controller = None
    _camera = None
    _motorPort = "/dev/ttyUSB0"
    width = None
    height = None

    def __init__(self, width, height):
        self._controller = Controller(self._motorPort)
        self._camera = Camera()
        self.width = width
        self.height = height

    def reset(self):
        # move back to the initial pos
        self._controller.move(translation=0.0, rotation=0.0, relative=False)
        observation = self._get_obs()
        return observation, {}

    def step(self, action):
        [translation,rotation] = action
        self._controller.move(translation=translation, rotation=rotation)
        observation = self._get_obs()
        terminated = False
        truncated = False
        reward = self._get_reward()
        info = self._get_info()
        return observation, reward, terminated, truncated, info

    def _get_obs(self):
        observation = self._camera.get_image(self.width, self.height)
        # apply segmentation
        # apply ...observation, reward, terminated, truncated, info
        return observation

    def _get_reward(self):
        return None

    def _get_info(self):
        # original_image = self._camera.get_image(width=80, height=80)
        current_position, right_bound,left_bound = self._controller.get_inf()  # get position infomation
        return dict(current_position=current_position, right_bound=right_bound,left_bound=left_bound)
if __name__=="__main__":
    env=RealEnv(width=2048,height=2048)
    env.reset()
    action=[0.0,1.0]
    for i in range(10):
        observation, reward, terminated, truncated, info=env.step(action)
        cv2.imwrite(f"{i}.jpg",observation)
    # env.



        # sleep(2)
        # observation=env._get_obs()
