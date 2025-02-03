class Sensores:
    def __init__(self, id_sensor, tipo, ubicacion, fec_instalacion, estado):
        self.id_sensor = id_sensor
        self.tipo= tipo
        self.ubicacion = ubicacion
        self.fec_instalacion = fec_instalacion
        self.estado = estado
    
    def to_dict(self):
        return {"Id Sensor": self.id_sensor, "Tipo ": self.tipo, "Ubicacion":self.ubicacion,
                 "Fecha instalacion": self.fec_instalacion, "Estado":self.estado }