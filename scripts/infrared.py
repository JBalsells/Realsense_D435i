import pyrealsense2 as rs
import numpy as np
import cv2

config = rs.config()

config.enable_stream(rs.stream.infrared, 1)  # IR izquierda
config.enable_stream(rs.stream.infrared, 2)  # IR derecha

pipeline = rs.pipeline()

pipeline.start(config)

try:
    while True:
        frames = pipeline.wait_for_frames()

        infrared_frame_left = frames.get_infrared_frame(1)  # Cámara IR izquierda
        infrared_frame_right = frames.get_infrared_frame(2)  # Cámara IR derecha

        infrared_image_left = np.asanyarray(infrared_frame_left.get_data())
        infrared_image_right = np.asanyarray(infrared_frame_right.get_data())

        cv2.imshow("Infrared Left", infrared_image_left)
        cv2.imshow("Infrared Right", infrared_image_right)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    pipeline.stop()
    cv2.destroyAllWindows()
