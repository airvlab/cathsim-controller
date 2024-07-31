import pyrealsense2 as rs

pipeline = rs.pipeline()
config = rs.config()
# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))
# Start streaming
# pipeline.start(config)
for sensor in device.sensors:
    print(f"Sensor: {sensor.get_info(rs.camera_info.name)}")
    for profile in sensor.profiles:
        print(profile)

