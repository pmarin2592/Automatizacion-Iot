class Sensores:
    """
    Modelo de datos para representar un sensor.

    Atributos:
        id_sensor (int): Identificador único del sensor.
        tipo (str): Tipo de sensor (ej. temperatura, humedad, etc.).
        ubicacion (str): Ubicación física del sensor.
        fec_instalacion (str): Fecha de instalación del sensor.
        estado (str): Estado actual del sensor (activo, inactivo, etc.).
    """

    def __init__(self, id_sensor, tipo, ubicacion, fec_instalacion, estado):
        """
        Inicializa un objeto de la clase Sensores.

        Parámetros:
            id_sensor (int): ID único del sensor.
            tipo (str): Tipo de sensor.
            ubicacion (str): Ubicación del sensor.
            fec_instalacion (str): Fecha de instalación.
            estado (str): Estado del sensor.
        """
        self.id_sensor = id_sensor
        self.tipo= tipo
        self.ubicacion = ubicacion
        self.fec_instalacion = fec_instalacion
        self.estado = estado
    
    def to_dict(self):
        """
        Convierte el objeto del sensor a un diccionario.

        Retorna:
            dict: Representación en formato diccionario del sensor.
        """
        return {"Id Sensor": self.id_sensor, "Tipo ": self.tipo, "Ubicacion":self.ubicacion,
                 "Fecha instalacion": self.fec_instalacion, "Estado":self.estado }