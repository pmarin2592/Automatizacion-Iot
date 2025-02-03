class Lecturas:
    def __init__(self, id_lectura, id_sensor, fecha_hora, valor):
        self.id_lectura = id_lectura
        self.id_sensor = id_sensor
        self.fecha_hora = fecha_hora
        self.valor = valor
    
    def to_dict(self):
        return {"Id lectura": self.id_lectura, "Id sensor":self.id_sensor, "Fecha Hora": self.fecha_hora, "Valor":self.valor}
        