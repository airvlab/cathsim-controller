from cathsim_controller.camera import Camera
from cathsim_controller.controller import Controller


class RealEnv:
    def __init__(
        self,
        image_width: int = 1280,
        image_height: int = 720,
        fps: int = 15,
    ):
        self._controller = Controller()
        self._camera = Camera(width=image_width, height=image_height, fps=fps, use_square=True)
        self.width = image_width
        self.height = image_height

    def reset(self):
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
    env = RealEnv()
    env.reset()
    action = [1.0, 0.0]
    for i in range(10):
        observation, reward, terminated, truncated, info = env.step(action)
