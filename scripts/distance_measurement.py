import pyrealsense2 as rs
import numpy as np
import cv2

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

pipeline.start(config)

try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()

        if not depth_frame:
            continue

        depth_image = np.asanyarray(depth_frame.get_data())

        height, width = depth_image.shape
        center_x, center_y = width // 2, height // 2
        distance = depth_frame.get_distance(center_x, center_y)

        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        cv2.circle(depth_colormap, (center_x, center_y), 5, (0, 255, 0), -1)
        cv2.putText(depth_colormap, f"{distance:.2f} m", (center_x + 10, center_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv2.imshow('RealSense Depth', depth_colormap)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    pipeline.stop()
    cv2.destroyAllWindows()
    