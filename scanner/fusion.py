import open3d as o3d
import numpy as np

# Lista de archivos PLY generados
ply_files = ["scan_0.ply", "scan_1.ply", "scan_2.ply", "scan_3.ply", "scan_4.ply", "scan_5.ply"]

# Cargar las nubes de puntos
point_clouds = [o3d.io.read_point_cloud(file) for file in ply_files]

# Inicializar la nube de referencia con la primera nube
global_pcd = point_clouds[0]

# Configuración de ICP (Iterative Closest Point)
threshold = 0.02  # Distancia de correspondencia en metros
transformation_init = np.identity(4)

# Fusionar todas las nubes usando ICP
for i in range(1, len(point_clouds)):
    print(f"Registrando nube {i} con la nube base...")
    
    # Ejecutar ICP para alinear la nube actual con la acumulada
    reg_p2p = o3d.pipelines.registration.registration_icp(
        point_clouds[i], global_pcd, threshold, transformation_init,
        o3d.pipelines.registration.TransformationEstimationPointToPoint()
    )

    # Transformar la nube actual para alinearla
    point_clouds[i].transform(reg_p2p.transformation)

    # Unir la nube transformada a la global
    global_pcd += point_clouds[i]

# Opcional: Filtrar la nube fusionada para reducir ruido
print("Filtrando nube final...")
global_pcd = global_pcd.voxel_down_sample(voxel_size=0.005)

# Guardar la nube fusionada
o3d.io.write_point_cloud("merged_scan.ply", global_pcd)
print("Nube de puntos fusionada guardada en 'merged_scan.ply'")

# Visualizar la nube fusionada
o3d.visualization.draw_geometries([global_pcd])
