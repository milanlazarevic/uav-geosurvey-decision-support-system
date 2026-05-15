class UAVTelemetry:
    def __init__(self,battery, signal, speed, hdop, satellites, fixType):
        self.data = {
            "battery": battery,
            "signal": signal,
            "speed": speed,
            "hdop": hdop,
            "satellites": satellites,
            "fixType": fixType
        }
