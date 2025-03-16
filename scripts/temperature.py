import pyrealsense2 as rs

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth)
pipeline.start(config)

device = pipeline.get_active_profile().get_device()

depth_sensor = device.first_depth_sensor()

try:
    asic_temp = depth_sensor.get_option(rs.option.asic_temperature)
    projector_temp = depth_sensor.get_option(rs.option.projector_temperature)

    print(f"Temperatura del ASIC: {asic_temp} °C")
    print(f"Temperatura del proyector: {projector_temp} °C")

except Exception as e:
    print(f"No se pudo obtener la temperatura del sensor: {e}")

finally:
    pipeline.stop()
