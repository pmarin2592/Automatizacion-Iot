class Lecturas:
    """
    Clase que representa una lectura de un sensor.

    Atributos:
    - id_lectura (int): Identificador único de la lectura.
    - id_sensor (int): Identificador del sensor asociado a la lectura.
    - fecha_hora (str): Fecha y hora en que se realizó la lectura.
    - valor (float): Valor registrado por el sensor.
    """
        
    def __init__(self, id_lectura, id_sensor, fecha_hora, valor):
        """
        Constructor de la clase Lecturas.

        Parámetros:
        - id_lectura (int): Identificador único de la lectura.
        - id_sensor (int): Identificador del sensor asociado a la lectura.
        - fecha_hora (str): Fecha y hora en que se realizó la lectura.
        - valor (float): Valor registrado por el sensor.
        """
        self.id_lectura = id_lectura
        self.id_sensor = id_sensor
        self.fecha_hora = fecha_hora
        self.valor = valor
    
    def to_dict(self):
        """
        Convierte la instancia de la clase en un diccionario.

        Retorna:
        - dict: Un diccionario con los atributos de la lectura.
        """
        return {"Id lectura": self.id_lectura, "Id sensor":self.id_sensor, "Fecha Hora": self.fecha_hora, "Valor":self.valor}
        