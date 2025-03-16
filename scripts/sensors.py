import pyrealsense2 as rs

pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth)
pipeline.start(config)

device = pipeline.get_active_profile().get_device()

try:
    print(f"Dispositivo: {device.get_info(rs.camera_info.name)}")
    print(f"Serial: {device.get_info(rs.camera_info.serial_number)}")
    print(f"Firmware: {device.get_info(rs.camera_info.firmware_version)}")
    
    for sensor in device.sensors:
        print(f"Sensor: {sensor.get_info(rs.camera_info.name)}")
        for option in sensor.get_supported_options():
            try:
                value = sensor.get_option(option)
                print(f"  Opción {option}: {value}")
            except Exception as e:
                print(f"  No se pudo obtener el valor de la opción {option}: {e}")

except Exception as e:
    print(f"No se pudo obtener la información del dispositivo: {e}")

finally:
    pipeline.stop()
