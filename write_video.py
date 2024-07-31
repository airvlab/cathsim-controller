import pyrealsense2 as rs
import cv2
import numpy as np

# 配置并启用RealSense管道
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)  # 配置RGB流

# 开始流
pipeline.start(config)

# 创建VideoWriter对象，定义视频的输出文件、编码器、帧率和分辨率
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, 30.0, (640, 480))

try:
    while True:
        # 获取帧
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # 将帧转换为numpy数组
        color_image = np.asanyarray(color_frame.get_data())

        # 将帧写入视频
        out.write(color_image)

        # 显示当前帧（可选）
        cv2.imshow('RealSense', color_image)
        
        # 按下 'q' 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # 停止管道
    pipeline.stop()
    # 释放VideoWriter对象
    out.release()
    # 关闭所有OpenCV窗口
    cv2.destroyAllWindows()
