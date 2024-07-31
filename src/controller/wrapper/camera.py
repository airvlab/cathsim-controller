import pyrealsense2 as rs
import numpy as np
import cv2
import matplotlib.pyplot as plt



class Camera:
    _pipeline = None
    _image = None

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
        config.enable_stream(rs.stream.color, 1280 720, rs.format.bgr8, 15)

        # Start streaming
        self._pipeline.start(config)
        

    def __del__(self):
        # Stop streaming
        self._pipeline.stop()

    def get_image(self, width, height):
        # Wait for a coherent pair of frames: depth and color
        frames = self._pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        # Convert images to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())
        # color_colormap_dim = color_image.shape
        self._image = color_image
        return self._image
    # def get_video(self, width, height):
    #     # 创建VideoWriter对象，定义视频的输出文件、编码器、帧率和分辨率
    #     fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #     out = cv2.VideoWriter('output.avi', fourcc, 30.0, (1024, 1024))
    #     while True:
    #         # Wait for a coherent pair of frames: depth and color
    #         frames = self._pipeline.wait_for_frames()
    #         color_frame = frames.get_color_frame()
    #         # Convert images to numpy arrays
    #         color_image = np.asanyarray(color_frame.get_data())
    #         out.write(color_image)
    #         # 按下 'q' 键退出
    #         if cv2.waitKey(1) & 0xFF == ord('q'):
    #             break
    #     out.release()
   

if __name__ == "main":
    test = Camera()
    img = test.get_image()
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    cv2.destroyAllWindows()

