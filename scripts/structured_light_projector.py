import pyrealsense2 as rs

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

pipeline_profile = pipeline.start(config)

device = pipeline_profile.get_device()
depth_sensor = device.first_depth_sensor()

if depth_sensor.supports(rs.option.laser_power):
    depth_sensor.set_option(rs.option.laser_power, 360)

print(f"Potencia del proyector: {depth_sensor.get_option(rs.option.laser_power)}")

try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        if not depth_frame:
            continue
finally:
    pipeline.stop()
    