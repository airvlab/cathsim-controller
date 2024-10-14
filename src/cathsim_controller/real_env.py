import gymnasium as gym
import numpy as np
from cathsim_controller.camera import Camera
from cathsim_controller.controller import Controller


class RealEnv(gym.Env):
    def __init__(
        self,
        image_width: int = 1920,
        image_height: int = 1080,
        fps: int = 8,
    ):
        self._controller = Controller()
        self._camera = Camera(width=image_width, height=image_height, fps=fps, use_square=True)
        self.image_width = image_width
        self.image_height = image_height

        self._init_observation_space()
        self.action_space = gym.spaces.Box(low=-1, high=1, shape=(2,), dtype=np.float32)

    def _init_observation_space(self):
        self.observation_space = gym.spaces.Box(
            low=0,
            high=255,
            shape=(self.image_width, self.image_width, 3),
            dtype=np.int16,
        )

    def _init_action_space(self):
        self.action_space = gym.spaces.Box(low=-1, high=1, shape=(2,), dtype=np.float32)

    def reset(self):
        print("Environment resetting...")
        self._controller.move(translation=0.0, rotation=0.0, relative=False)
        observation = self._get_obs()
        return observation, {}

    def step(self, action):
        translation, rotation = action
        self._controller.move(translation=translation, rotation=rotation)
        observation = self._get_obs()
        terminated = False
        truncated = False
        reward = self._get_reward()
        info = self._get_info()
        return observation, reward, terminated, truncated, info

    def _get_obs(self):
        observation = dict(
            pixels=self._camera.get_image(),
        )
        return observation

    def _get_reward(self):
        return None

    def _get_info(self):
        current_position = self._controller.get_info()
        return dict(
            current_position=current_position,
        )


if __name__ == "__main__":
    import cv2

    env = RealEnv()
    env.reset()
    action = [1.0, 0.0]
    for i in range(10):
        observation, reward, terminated, truncated, info = env.step(action)
        image = observation["pixels"]
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imshow("Image", image)
        cv2.waitKey(1)

    env.reset()
