import numpy as np
import pyrealsense2 as rs
import matplotlib.pyplot as plt

min_distance = 1000
max_distance = 3000
level_curves = 40

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
pipeline.start(config)

plt.ion()
fig, ax = plt.subplots()

depth_matrix = np.zeros((480, 640))
im = ax.imshow(depth_matrix, cmap='jet', interpolation='nearest', vmin=min_distance, vmax=max_distance)

cbar = fig.colorbar(im, ax=ax, label="Profundidad (mm)")

try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        
        if not depth_frame:
            continue
        
        depth_image = np.asanyarray(depth_frame.get_data())
        depth_image = np.clip(depth_image, min_distance, max_distance)

        im.set_data(depth_image)

        ax.collections.clear()
        levels = np.linspace(min_distance, max_distance, num=level_curves)
        ax.contour(depth_image, levels, colors='black', linewidths=0.7)

        plt.pause(0.02)

finally:
    pipeline.stop()
    plt.ioff()
    plt.show()
