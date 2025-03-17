import pyrealsense2 as rs
import numpy as np
import open3d as o3d
import time

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

pipeline.start(config)

# Configurar alineación de profundidad y color
align = rs.align(rs.stream.color)

# Cantidad de capturas desde distintos ángulos
num_captures = 6  
angle_step = 30

print("Coloca la cámara en la primera posición y presiona Enter para empezar.")
input()

try:
    for i in range(num_captures):
        print(f"Capturando vista {i+1}/{num_captures}...")

        # Esperar a que el frame esté listo
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)

        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        if not depth_frame or not color_frame:
            print("Error al capturar los frames.")
            continue

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        pc = rs.pointcloud()
        pc.map_to(color_frame)
        points = pc.calculate(depth_frame)
        
        # Guardar nube de puntos en PLY
        filename = f"scan_{i}.ply"
        points.export_to_ply(filename, color_frame)
        print(f"Vista {i+1} guardada en {filename}")

        if i < num_captures - 1:
            print(f"Mueve la cámara {angle_step} grados y presiona Enter para la siguiente captura.")
            input()

finally:
    pipeline.stop()
    print("Escaneo completado.")

print("Usa MeshLab o Open3D para alinear y fusionar las nubes de puntos.")
