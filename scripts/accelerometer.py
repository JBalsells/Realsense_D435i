import pyrealsense2 as rs
import numpy as np
import math

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.accel)
config.enable_stream(rs.stream.gyro)

pipeline.start(config)

def get_tilt_angle(accel_data):
    ax, ay, az = accel_data
    roll = math.atan2(ay, az) * 180.0 / math.pi  # Inclinación en el eje X
    pitch = math.atan2(-ax, math.sqrt(ay**2 + az**2)) * 180.0 / math.pi  # Inclinación en el eje Y
    return roll, pitch

try:
    while True:
        frames = pipeline.wait_for_frames()
        
        accel = frames.first_or_default(rs.stream.accel)
        if accel:
            accel_data = accel.as_motion_frame().get_motion_data()
            ax, ay, az = accel_data.x, accel_data.y, accel_data.z
            roll, pitch = get_tilt_angle((ax, ay, az))

            print(f"Roll: {roll:.2f}°, Pitch: {pitch:.2f}°")

except KeyboardInterrupt:
    print("Finalizando...")
    pipeline.stop()
