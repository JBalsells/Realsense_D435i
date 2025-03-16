import numpy as np
import pyrealsense2 as rs
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

min_distance = 700
max_distance = 1300
level_curves = 40

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
pipeline.start(config)

# Crear un colormap personalizado con gris claro para los valores por debajo de min_distance
# y gris oscuro para los valores por encima de max_distance
cmap = plt.cm.jet
cmap.set_under('#d3d3d3')  # Gris claro para los valores menores que min_distance
cmap.set_over('#505050')   # Gris oscuro para los valores mayores que max_distance

plt.ion()
fig, ax = plt.subplots()

depth_matrix = np.zeros((480, 640))

# Crear una máscara para los valores fuera del rango
masked_depth_image = np.ma.masked_less(depth_matrix, min_distance)  # Enmascara los valores menores que min_distance
masked_depth_image = np.ma.masked_greater(masked_depth_image, max_distance)  # Enmascara los valores mayores que max_distance

# Mostrar la imagen enmascarada
im = ax.imshow(masked_depth_image, cmap=cmap, interpolation='nearest', vmin=min_distance, vmax=max_distance)

cbar = fig.colorbar(im, ax=ax, label="Profundidad (mm)")

try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        
        if not depth_frame:
            continue
        
        depth_image = np.asanyarray(depth_frame.get_data())
        
        # Aplicar la máscara
        masked_depth_image = np.ma.masked_less(depth_image, min_distance)
        masked_depth_image = np.ma.masked_greater(masked_depth_image, max_distance)

        im.set_data(masked_depth_image)

        ax.collections.clear()
        levels = np.linspace(min_distance, max_distance, num=level_curves)
        ax.contour(masked_depth_image, levels, colors='black', linewidths=0.7)

        plt.pause(0.02)

finally:
    pipeline.stop()
    plt.ioff()
    plt.show()
