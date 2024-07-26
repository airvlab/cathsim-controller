import pyrealsense2 as rs
import numpy as np
import cv2


class Camera:
    _pipeline = None
    _images = None

    def __init__(self):
        # Configure depth and color streams
        self._pipeline = rs.pipeline()
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self._pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(rs.camera_info.product_line))

        found_rgb = False
        for s in device.sensors:
            if s.get_info(rs.camera_info.name) == "RGB Camera":
                found_rgb = True
                break
        if not found_rgb:
            print("The demo requires Depth camera with Color sensor")
            exit(0)

        # config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

        # Start streaming
        self._pipeline.start(config)
        # Wait for a coherent pair of frames: depth and color
        while True:
            frames = self._pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            if color_frame:
                break
        # Convert images to numpy arrays

        color_image = np.asanyarray(color_frame.get_data())

        color_colormap_dim = color_image.shape

        self._images = color_image

    def __del__(self):
        # Stop streaming
        self._pipeline.stop()

    def get_image(self, width, height):
        image = self._images
        return image
   

if __name__ == "main":
    test = Camera()
    img = test.get_image()
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    cv2.destroyAllWindows()

#  def write_img(self, filename):
#         # save image
#         cv2.imwrite(filename, self._images)
#         img = cv2.imread(filename)
#         img = cv2.resize(img, (80, 80))
#         # If the image data type is np.float64, convert it to np.float32
#         # if img.dtype == np.float64:
#         #     img = img.astype(np.float32)
#         return img
