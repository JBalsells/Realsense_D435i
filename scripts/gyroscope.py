import pyrealsense2 as rs
import numpy as np

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.accel)
config.enable_stream(rs.stream.gyro)

pipeline.start(config)

def get_gyro_data(gyro_data):
    gx, gy, gz = gyro_data
    return gx, gy, gz

try:
    while True:
        frames = pipeline.wait_for_frames()
        
        gyro = frames.first_or_default(rs.stream.gyro)
        if gyro:
            gyro_data = gyro.as_motion_frame().get_motion_data()
            gx, gy, gz = gyro_data.x, gyro_data.y, gyro_data.z

            print(f"Gyro X: {gx:.2f}°/s, Gyro Y: {gy:.2f}°/s, Gyro Z: {gz:.2f}°/s")

except KeyboardInterrupt:
    print("Finalizando...")
    pipeline.stop()
