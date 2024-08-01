import cv2
import pygame
from cathsim_controller.camera import Camera
from cathsim_controller.joystick import Joystick


class RealEnv:
    def __init__(
        self,
        image_width: int = 640,
        image_height: int = 480,
    ):
        self._camera = Camera(width=image_width, height=image_height)

        self.width = image_width
        self.height = image_height

    def reset(self):
        observation = self._get_obs()
        return observation, {}

    def step(self, action):
        observation = self._get_obs()

        info = self._get_info()
        info["action"] = action

        return observation, 0, False, False, info

    def _get_obs(self):
        observation = self._camera.get_image()
        return observation

    def _get_info(self):
        return {}


if __name__ == "__main__":
    env = RealEnv(image_width=640, image_height=480)
    joystick = Joystick()
    obs, info = env.reset()
    while True:
        action = joystick.get_input()
        print(action)
        observation, reward, terminated, truncated, info = env.step(action)
        pygame.time.wait(100)
        observation = cv2.cvtColor(observation, cv2.COLOR_RGB2BGR)
        cv2.imshow("obs", observation)
        cv2.waitKey(1)
        # cv2.imwrite(f"samples/{i}.jpg",observation)
    # env.

    # sleep(2)
    # observation=env._get_obs()
