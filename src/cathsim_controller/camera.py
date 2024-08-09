import cv2
import numpy as np
import pyrealsense2 as rs


class Camera:
    def __init__(
        self, width: int = 640, height: int = 480, fps: int = 30, square=False
    ):
        config = rs.config()
        config.enable_stream(rs.stream.color, width, height, rs.format.rgb8, fps)

        self.square = square

        self._pipeline = rs.pipeline()
        self._pipeline_wrapper = rs.pipeline_wrapper(self._pipeline)
        self._pipeline_profile = config.resolve(self._pipeline_wrapper)
        self._device = self._pipeline_profile.get_device()
        self._profiles = self.get_profiles(self._device)
        self._validate_profile(fps, width, height, self._profiles)

        if not self._has_rgb_sensor(self._device):
            raise Exception("The demo requires Depth camera with Color sensor")

        self._pipeline.start(config)

    @staticmethod
    def _validate_profile(fps, width, height, profiles):
        for profile in profiles:
            if profile[0] == fps and profile[1] == width and profile[2] == height:
                return True
        raise Exception(f"Invalid resolution: {width}x{height} @ {fps}fps")

    @staticmethod
    def _has_rgb_sensor(device):
        for sensor in device.sensors:
            if sensor.get_info(rs.camera_info.name) == "RGB Camera":
                return True
        return False

    def __del__(self):
        self._pipeline.stop()

    def make_square(self, image):
        height, width, _ = image.shape
        # crop the image to a square
        image = image[
            (height - min(height, width)) // 2 : (height + min(height, width)) // 2,
            (width - min(height, width)) // 2 : (width + min(height, width)) // 2,
        ]
        return image

    def get_image(self):
        frames = self._pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        image = np.asanyarray(color_frame.get_data())
        if self.square:
            image = self.make_square(image)
        return image

    def get_profiles(self, device):
        profiles = []
        rgb_sensor = None
        for sensor in device.sensors:
            if sensor.get_info(rs.camera_info.name) == "RGB Camera":
                rgb_sensor = sensor

        for profile in rgb_sensor.profiles:
            profile = profile.as_video_stream_profile()
            profiles.append((profile.fps(), profile.width(), profile.height()))

        return profiles


if __name__ == "__main__":
    camera = Camera(width=1920, height=1080, fps=8, square=True)
    # print(camera._profiles)
    while True:
        image = camera.get_image()
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        print(image.shape)
        cv2.imshow("RealSense", image)
        cv2.waitKey(1)
