import pyrealsense2 as rs
import cv2
import numpy as np

# start pipeline
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1280,720, rs.format.bgr8, 15)  # 配置RGB流

# start streaming
pipeline.start(config)

# video write
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 15.0, (1280,720))

try:
    while True:
        # get frames
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # change to array
        color_image = np.asanyarray(color_frame.get_data())

        # write the frame
        out.write(color_image)

        # show the frame
        cv2.imshow('RealSense', color_image)
        
        # q to qiut
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # stop pipeline
    pipeline.stop()
    # release object
    out.release()
    # close the windows
    cv2.destroyAllWindows()
